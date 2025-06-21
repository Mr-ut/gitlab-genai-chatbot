"""
GitLab Content Scraper

This module scrapes content from GitLab's Handbook and Direction pages
for use in the RAG (Retrieval Augmented Generation) system.
"""

import asyncio
import aiohttp
import logging
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Set
import json
import os
from datetime import datetime
import time
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitLabScraper:
    """Scraper for GitLab Handbook and Direction pages"""

    def __init__(self):
        self.base_urls = [
            settings.GITLAB_HANDBOOK_URL,
            settings.GITLAB_DIRECTION_URL
        ]
        self.visited_urls: Set[str] = set()
        self.scraped_data: List[Dict[str, Any]] = []
        self.max_pages = settings.MAX_PAGES
        self.delay = settings.SCRAPING_DELAY

    async def scrape_all(self) -> List[Dict[str, Any]]:
        """Scrape all GitLab pages"""
        logger.info("Starting GitLab content scraping...")

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'GitLab-Chatbot-Scraper/1.0 (Educational Purpose)'
            }
        ) as session:

            # Scrape each base URL
            for base_url in self.base_urls:
                await self._scrape_site_section(session, base_url)

        logger.info(f"Scraping completed. Total pages scraped: {len(self.scraped_data)}")
        return self.scraped_data

    async def _scrape_site_section(self, session: aiohttp.ClientSession, base_url: str):
        """Scrape a specific section of the GitLab site"""
        try:
            # Start with the main page
            urls_to_visit = [base_url]

            while urls_to_visit and len(self.scraped_data) < self.max_pages:
                current_url = urls_to_visit.pop(0)

                if current_url in self.visited_urls:
                    continue

                self.visited_urls.add(current_url)

                try:
                    page_data = await self._scrape_page(session, current_url)
                    if page_data:
                        self.scraped_data.append(page_data)

                        # Find new URLs to scrape
                        new_urls = await self._extract_links(session, current_url, base_url)
                        urls_to_visit.extend(new_urls)

                    # Respect rate limiting
                    await asyncio.sleep(self.delay)

                except Exception as e:
                    logger.error(f"Error scraping {current_url}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error scraping site section {base_url}: {e}")

    async def _scrape_page(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """Scrape a single page"""
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    logger.warning(f"Failed to fetch {url}: HTTP {response.status}")
                    return None

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # Extract title
                title = self._extract_title(soup)

                # Extract main content
                content = self._extract_content(soup)

                if not content.strip():
                    return None

                # Extract metadata
                metadata = self._extract_metadata(soup, url)

                logger.info(f"Scraped: {title} ({len(content)} chars)")

                return {
                    "url": url,
                    "title": title,
                    "content": content,
                    "metadata": metadata,
                    "scraped_at": datetime.utcnow().isoformat()
                }

        except Exception as e:
            logger.error(f"Error scraping page {url}: {e}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        # Try different title selectors
        title_selectors = ['h1', 'title', '.page-title', '#title']

        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                return title_elem.get_text().strip()

        return "Untitled Page"

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from the page"""
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()

        # Try to find main content area
        content_selectors = [
            'main',
            '.content',
            '.main-content',
            '#content',
            '.handbook-content',
            '.direction-content',
            'article',
            '.post-content'
        ]

        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                return self._clean_text(content_elem.get_text())

        # Fallback to body content
        body = soup.select_one('body')
        if body:
            return self._clean_text(body.get_text())

        return ""

    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]

        # Join and clean up
        cleaned = '\n'.join(lines)

        # Remove excessive whitespace
        import re
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        cleaned = re.sub(r' {2,}', ' ', cleaned)

        return cleaned.strip()

    def _extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract metadata from the page"""
        metadata = {
            "source_type": "handbook" if "handbook" in url else "direction",
            "url": url,
            "domain": urlparse(url).netloc
        }

        # Extract meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                metadata[name] = content

        # Extract headings structure
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            headings.append({
                'level': int(h.name[1]),
                'text': h.get_text().strip()
            })

        if headings:
            metadata['headings'] = headings

        return metadata

    async def _extract_links(self, session: aiohttp.ClientSession, current_url: str, base_url: str) -> List[str]:
        """Extract relevant links from a page"""
        try:
            async with session.get(current_url) as response:
                if response.status != 200:
                    return []

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']

                    # Convert relative URLs to absolute
                    full_url = urljoin(current_url, href)

                    # Filter relevant links
                    if self._is_relevant_link(full_url, base_url):
                        links.append(full_url)

                return links[:10]  # Limit links per page

        except Exception as e:
            logger.error(f"Error extracting links from {current_url}: {e}")
            return []

    def _is_relevant_link(self, url: str, base_url: str) -> bool:
        """Check if a link is relevant for scraping"""
        parsed_url = urlparse(url)
        parsed_base = urlparse(base_url)

        # Must be same domain
        if parsed_url.netloc != parsed_base.netloc:
            return False

        # Must start with base path
        if not url.startswith(base_url):
            return False

        # Skip certain file types
        skip_extensions = {'.pdf', '.doc', '.docx', '.zip', '.tar', '.gz'}
        if any(url.lower().endswith(ext) for ext in skip_extensions):
            return False

        # Skip certain paths
        skip_paths = {'#', 'javascript:', 'mailto:', 'tel:'}
        if any(url.lower().startswith(path) for path in skip_paths):
            return False

        return True

    def save_to_file(self, filename: str = None):
        """Save scraped data to a JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"gitlab_scraped_data_{timestamp}.json"

        filepath = os.path.join("../data", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Scraped data saved to {filepath}")
        return filepath

async def main():
    """Main function to run the scraper"""
    scraper = GitLabScraper()

    try:
        # Scrape all content
        data = await scraper.scrape_all()

        # Save to file
        filepath = scraper.save_to_file()

        print(f"\nScraping completed!")
        print(f"Pages scraped: {len(data)}")
        print(f"Data saved to: {filepath}")

        # Print sample data
        if data:
            print(f"\nSample page:")
            sample = data[0]
            print(f"Title: {sample['title']}")
            print(f"URL: {sample['url']}")
            print(f"Content length: {len(sample['content'])} characters")

    except Exception as e:
        logger.error(f"Scraping failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
