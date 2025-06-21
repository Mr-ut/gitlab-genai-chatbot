#!/usr/bin/env python3
"""
Test script for Groq API integration
Run this after setting up your Groq API key
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

# Available Groq models (free tier)
GROQ_MODELS = [
    "llama3-8b-8192",        # Llama 3 8B (recommended)
    "llama3-70b-8192",       # Llama 3 70B (more powerful but slower)
    "mixtral-8x7b-32768",    # Mixtral 8x7B
    "gemma-7b-it",           # Gemma 7B
]

async def test_groq_model(api_key: str, model: str):
    """Test a specific Groq model"""
    try:
        print(f"\n🧪 Testing {model}...")

        llm = ChatGroq(
            model=model,
            temperature=0.7,
            max_tokens=100,
            groq_api_key=api_key
        )

        response = await llm.ainvoke([
            HumanMessage(content="What is GitLab? Answer in 2 sentences.")
        ])

        print(f"✅ {model}: {response.content}")
        return True

    except Exception as e:
        print(f"❌ {model}: {str(e)}")
        return False

async def main():
    """Main test function"""
    print("🚀 Testing Groq API Integration\n")

    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your-groq-api-key-here":
        print("❌ Please set your GROQ_API_KEY in the .env file")
        print("Get your free API key from: https://console.groq.com/")
        return

    print(f"🔑 API Key found: {api_key[:10]}...")

    # Test each model
    successful_models = []
    for model in GROQ_MODELS:
        success = await test_groq_model(api_key, model)
        if success:
            successful_models.append(model)

    print(f"\n📊 Summary:")
    print(f"✅ Working models: {len(successful_models)}")
    print(f"❌ Failed models: {len(GROQ_MODELS) - len(successful_models)}")

    if successful_models:
        print(f"\n💡 Recommended model: {successful_models[0]}")
        print("You can use any of these models by updating DEFAULT_MODEL in config.py")

if __name__ == "__main__":
    asyncio.run(main())
