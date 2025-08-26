import React, { useEffect } from 'react';
import { X } from 'lucide-react';

const ProductModal = ({ product, onClose }) => {
  const {
    name,
    description,
    company,
    parentCompany,
    category,
    version,
    features = [],
    targetAudience = [],
    pricing = {},
    integrations = [],
    supportedPlatforms = [],
    lastUpdated
  } = product;

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="modal" onClick={handleBackdropClick}>
      <div className="modal-content">
        <div className="modal-header">
          <button className="close-btn" onClick={onClose}>
            <X size={24} />
          </button>
          <h2>{name}</h2>
          <p>{description}</p>
        </div>
        
        <div className="modal-body">
          <div style={{
            background: 'rgba(102, 126, 234, 0.1)',
            padding: '15px',
            borderRadius: '10px',
            marginBottom: '20px'
          }}>
            <div className="section-title" style={{ marginBottom: '5px' }}>
              Company Information
            </div>
            <p style={{ fontSize: '1.1rem', fontWeight: '600', color: '#667eea' }}>
              {company}
            </p>
            {parentCompany && (
              <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '5px' }}>
                Parent Company: {parentCompany}
              </p>
            )}
            <div className="section-title" style={{ marginBottom: '5px', marginTop: '10px' }}>
              Category
            </div>
            <p style={{ fontSize: '1rem', color: '#666' }}>{category}</p>
            {version && (
              <div className="section-title" style={{ marginBottom: '5px', marginTop: '10px' }}>
                Version
              </div>
            )}
            {version && (
              <p style={{ fontSize: '1rem', color: '#666' }}>{version}</p>
            )}
          </div>
          
          <div className="features-section">
            <div className="section-title">Complete Feature List</div>
            <div className="features-list">
              {features.map((feature, index) => (
                <div key={index} className="feature-item">
                  {feature}
                </div>
              ))}
            </div>
          </div>
          
          <div className="audience-section">
            <div className="section-title">Target Audience</div>
            <div className="audience-tags">
              {targetAudience.map((audience, index) => (
                <span key={index} className="audience-tag">
                  {audience}
                </span>
              ))}
            </div>
          </div>

          {pricing.model && (
            <div className="features-section">
              <div className="section-title">Pricing</div>
              <div style={{
                background: 'rgba(102, 126, 234, 0.1)',
                padding: '15px',
                borderRadius: '10px'
              }}>
                <p><strong>Model:</strong> {pricing.model}</p>
                {pricing.startingPrice && (
                  <p><strong>Starting Price:</strong> {pricing.startingPrice} {pricing.currency || 'EUR'}</p>
                )}
              </div>
            </div>
          )}

          {integrations.length > 0 && (
            <div className="features-section">
              <div className="section-title">Integrations</div>
              <div className="audience-tags">
                {integrations.map((integration, index) => (
                  <span key={index} className="audience-tag">
                    {integration}
                  </span>
                ))}
              </div>
            </div>
          )}

          {supportedPlatforms.length > 0 && (
            <div className="features-section">
              <div className="section-title">Supported Platforms</div>
              <div className="audience-tags">
                {supportedPlatforms.map((platform, index) => (
                  <span key={index} className="audience-tag">
                    {platform}
                  </span>
                ))}
              </div>
            </div>
          )}

          {lastUpdated && (
            <div className="features-section">
              <div className="section-title">Last Updated</div>
              <p style={{ color: '#666' }}>{lastUpdated}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductModal;
