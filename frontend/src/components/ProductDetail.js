import React from 'react';
import { ArrowLeft, CheckCircle, Users, Tag } from 'lucide-react';

const ProductDetail = ({ product, onBackToProducts }) => {
  if (!product) {
    return (
      <div className="no-results">
        <h3>Product not found</h3>
        <p>The requested product could not be found.</p>
      </div>
    );
  }

  return (
    <div className="product-detail">
      <div className="product-detail-content">
        <div className="product-detail-main">
          <div className="product-description-section">
            <h2>Description</h2>
            <p className="product-description-full">{product.description}</p>
          </div>

          <div className="product-features-section">
            <h2>
              <CheckCircle size={24} />
              Features
            </h2>
            <div className="features-grid">
              {product.features.map((feature, index) => (
                <div key={index} className="feature-item-full">
                  <CheckCircle size={16} className="feature-icon" />
                  <span>{feature}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="product-audience-section">
            <h2>
              <Users size={24} />
              Target Audience
            </h2>
            <div className="audience-grid">
              {product.targetAudience.map((audience, index) => (
                <div key={index} className="audience-item-full">
                  <Users size={16} className="audience-icon" />
                  <span>{audience}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="product-detail-sidebar">
          <div className="product-info-card">
            <h3>Product Information</h3>
            <div className="info-item">
              <span className="info-label">Category:</span>
              <span className="info-value">{product.category}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Company:</span>
              <span className="info-value">{product.company}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Features:</span>
              <span className="info-value">{product.features.length}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Target Audiences:</span>
              <span className="info-value">{product.targetAudience.length}</span>
            </div>
          </div>

          {product.pricing && (
            <div className="product-pricing-card">
              <h3>Pricing</h3>
              <div className="pricing-info">
                <div className="pricing-model">
                  {product.pricing.model}
                </div>
                {product.pricing.startingPrice && (
                  <div className="pricing-price">
                    Starting from {product.pricing.currency} {product.pricing.startingPrice}
                  </div>
                )}
              </div>
            </div>
          )}

          <div className="product-actions">
            <button className="contact-button">
              Contact Company
            </button>
            <button className="learn-more-button">
              Learn More
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;
