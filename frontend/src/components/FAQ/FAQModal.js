import React, { useEffect } from 'react';
import { X, Tag, Info } from 'lucide-react';

const FAQModal = ({ faq, onClose }) => {
  // Close modal on escape key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    document.body.style.overflow = 'hidden';

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [onClose]);

  // Close modal on backdrop click
  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="faq-modal-backdrop" onClick={handleBackdropClick}>
      <div className="faq-modal">
        <div className="faq-modal-header">
          <div className="faq-modal-title">
            <Info size={20} />
            <h2>FAQ Details</h2>
          </div>
          <button 
            className="faq-modal-close"
            onClick={onClose}
            aria-label="Close modal"
          >
            <X size={20} />
          </button>
        </div>

        <div className="faq-modal-content">
          {faq.categoryName && (
            <div className="faq-modal-category">
              {faq.categoryName}
            </div>
          )}

          <h3 className="faq-modal-question">
            {faq.question}
          </h3>

          <div className="faq-modal-answer">
            {faq.answer}
          </div>

          {faq.keywords && faq.keywords.length > 0 && (
            <div className="faq-modal-keywords">
              <div className="faq-modal-keywords-title">
                <Tag size={16} />
                <span>Related Topics</span>
              </div>
              <div className="faq-modal-keywords-list">
                {faq.keywords.map((keyword, index) => (
                  <span key={index} className="faq-modal-keyword">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}

          {faq.searchTerms && faq.searchTerms.length > 0 && (
            <div className="faq-modal-search-terms">
              <strong>Also searched as:</strong>
              <p>{faq.searchTerms.join(', ')}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FAQModal;
