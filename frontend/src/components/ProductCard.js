import React from 'react';

const ProductCard = ({ product, onClick }) => {
  const {
    name,
    description,
    company,
    category,
    features = [],
    targetAudience = [],
    pricing = {}
  } = product;

  return (
    <div className="product-card fade-in" onClick={onClick}>
      <div className="product-header">
        <h3 className="product-name">{name}</h3>
        <span className="company-badge">{company}</span>
      </div>
      
      <p className="product-description">{description}</p>
      
      <div className="features-section">
        <div className="section-title">Key Features</div>
        <div className="features-list">
          {features.slice(0, 4).map((feature, index) => (
            <div key={index} className="feature-item">
              {feature}
            </div>
          ))}
          {features.length > 4 && (
            <div className="feature-item">
              +{features.length - 4} more features
            </div>
          )}
        </div>
      </div>
      
      <div className="audience-section">
        <div className="section-title">Target Audience</div>
        <div className="audience-tags">
          {targetAudience.slice(0, 3).map((audience, index) => (
            <span key={index} className="audience-tag">
              {audience}
            </span>
          ))}
          {targetAudience.length > 3 && (
            <span className="audience-tag">
              +{targetAudience.length - 3} more
            </span>
          )}
        </div>
      </div>
      
      <button className="expand-btn">View Details</button>
    </div>
  );
};

export default ProductCard;
