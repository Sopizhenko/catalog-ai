import React, { useEffect } from "react";
import { X, Building2, Package, Calendar, Code } from "lucide-react";

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
    lastUpdated,
  } = product;

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === "Escape") {
        onClose();
      }
    };

    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [onClose]);

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="modal-overlay" onClick={handleBackdropClick}>
      <div className="modal-content">
        <div className="modal-header">
          <h2>{name}</h2>
          <button
            className="close-button"
            onClick={onClose}
            aria-label="Close modal"
          >
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          <div className="modal-info-section">
            <div className="info-header icon-text-container">
              <Building2 size={20} className="icon" />
              <h3>Company Information</h3>
            </div>
            <div className="info-content">
              <p className="company-name">{company}</p>
              {parentCompany && (
                <p className="parent-company-info">
                  Parent Company: {parentCompany}
                </p>
              )}
            </div>
          </div>

          <div className="modal-info-section">
            <div className="info-header icon-text-container">
              <Package size={20} className="icon" />
              <h3>Product Details</h3>
            </div>
            <div className="info-content">
              <div className="info-item">
                <span className="info-label">Category:</span>
                <span className="info-value">{category}</span>
              </div>
              {version && (
                <div className="info-item">
                  <span className="info-label">Version:</span>
                  <span className="info-value">{version}</span>
                </div>
              )}
              {lastUpdated && (
                <div className="info-item">
                  <span className="info-label">Last Updated:</span>
                  <span className="info-value">{lastUpdated}</span>
                </div>
              )}
            </div>
          </div>

          <div className="modal-section">
            <div className="section-title">Complete Feature List</div>
            <div className="features-grid">
              {features.map((feature, index) => (
                <div key={index} className="feature-card">
                  {feature}
                </div>
              ))}
            </div>
          </div>

          <div className="modal-section">
            <div className="section-title">Target Audience</div>
            <div className="audience-grid">
              {targetAudience.map((audience, index) => (
                <span key={index} className="audience-item">
                  {audience}
                </span>
              ))}
            </div>
          </div>

          {pricing && Object.keys(pricing).length > 0 && (
            <div className="modal-section">
              <div className="section-title">Pricing Information</div>
              <div className="pricing-section">
                <h3>Pricing Model</h3>
                <div className="pricing-info">
                  {pricing.model && (
                    <p>
                      <strong>Model:</strong> {pricing.model}
                    </p>
                  )}
                  {pricing.price && (
                    <p>
                      <strong>Price:</strong> {pricing.price}
                    </p>
                  )}
                  {pricing.currency && (
                    <p>
                      <strong>Currency:</strong> {pricing.currency}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}

          {integrations && integrations.length > 0 && (
            <div className="modal-section">
              <div className="section-title">Integrations</div>
              <div className="integrations-grid">
                {integrations.map((integration, index) => (
                  <div key={index} className="integration-item">
                    {integration}
                  </div>
                ))}
              </div>
            </div>
          )}

          {supportedPlatforms && supportedPlatforms.length > 0 && (
            <div className="modal-section">
              <div className="section-title">Supported Platforms</div>
              <div className="platforms-grid">
                {supportedPlatforms.map((platform, index) => (
                  <div key={index} className="platform-item">
                    {platform}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductModal;
