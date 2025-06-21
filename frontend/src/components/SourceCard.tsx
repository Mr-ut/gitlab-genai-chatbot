import React from 'react';
import { Source } from '../types';

interface SourceCardProps {
  source: Source;
}

export const SourceCard: React.FC<SourceCardProps> = ({ source }) => {
  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <h4 className="font-medium text-gray-900 text-sm line-clamp-2">
          {source.title}
        </h4>
        <div className="flex items-center ml-2">
          <div className="w-2 h-2 bg-green-500 rounded-full mr-1"></div>
          <span className="text-xs text-gray-500">
            {Math.round(source.similarity_score * 100)}%
          </span>
        </div>
      </div>

      <p className="text-sm text-gray-600 mb-3 line-clamp-3">
        {source.excerpt}
      </p>

      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
          {source.url.includes('handbook') ? '📚 Handbook' : '🎯 Direction'}
        </span>

        <a
          href={source.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center"
        >
          View Source
          <svg className="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>
      </div>
    </div>
  );
};
