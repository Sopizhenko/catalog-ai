import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Tag, ExternalLink } from 'lucide-react';

const FAQItem = ({ faq, searchQuery, onClick }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  const handleViewDetails = (e) => {
    e.stopPropagation();
    onClick(faq);
  };

  // Highlight search terms in text
  const highlightText = (text, query) => {
    if (!query) return text;
    
    const regex = new RegExp(`(${query})`, 'gi');
    const parts = text.split(regex);
    
    return parts.map((part, index) => 
      regex.test(part) ? 
        <mark key={index} className="faq-highlight">{part}</mark> : 
        part
    );
  };

  return (
    <div className={`faq-item ${isExpanded ? 'expanded' : ''}`}>
      <div className="faq-item-header" onClick={toggleExpanded}>
        <div className="faq-item-title">
          <h3>{highlightText(faq.question, searchQuery)}</h3>
          {faq.categoryName && (
            <span className="faq-item-category">
              {faq.categoryName}
            </span>
          )}
        </div>
        <button className="faq-item-toggle">
          {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
      </div>

      <div className={`faq-item-content ${isExpanded ? 'expanded' : ''}`}>
        <div className="faq-item-answer">
          {highlightText(faq.answer, searchQuery)}
        </div>

        {faq.keywords && faq.keywords.length > 0 && (
          <div className="faq-item-keywords">
            <Tag size={14} />
            <div className="faq-keywords-list">
              {faq.keywords.map((keyword, index) => (
                <span key={index} className="faq-keyword">
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="faq-item-actions">
          <button 
            className="faq-item-detail-btn"
            onClick={handleViewDetails}
          >
            <ExternalLink size={14} />
            View Details
          </button>
        </div>
      </div>
    </div>
  );
};

export default FAQItem;
