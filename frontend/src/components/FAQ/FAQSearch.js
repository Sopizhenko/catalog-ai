import React from 'react';
import { Search, X } from 'lucide-react';

const FAQSearch = ({ searchQuery, onSearch, onClear }) => {
  const handleInputChange = (e) => {
    onSearch(e.target.value);
  };

  const handleClear = () => {
    onClear();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      handleClear();
    }
  };

  return (
    <div className="faq-search">
      <div className="faq-search-container">
        <div className="faq-search-input-wrapper">
          <Search className="faq-search-icon" size={20} />
          <input
            type="text"
            className="faq-search-input"
            placeholder="Search FAQs, topics, or keywords..."
            value={searchQuery}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            autoComplete="off"
          />
          {searchQuery && (
            <button
              className="faq-search-clear"
              onClick={handleClear}
              aria-label="Clear search"
            >
              <X size={16} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default FAQSearch;
