import React from "react";
import { ArrowRight, Star, Users } from "lucide-react";

const ProductCard = ({ product, onClick }) => {
  const {
    name,
    description,
    company,
    category,
    features = [],
    targetAudience = [],
    pricing = {},
  } = product;

  return (
    <div className="product-card fade-in" onClick={onClick}>
      <div className="product-header">
        <div className="product-title-section">
          <h3 className="product-name">{name}</h3>
          <span className="product-category">{category}</span>
        </div>
        <span className="company-badge">{company}</span>
      </div>

      <p className="product-description">{description}</p>

      <div className="product-stats">
        <div className="stat-item icon-text-container">
          <Star size={16} className="icon" />
          <span>{features.length} Features</span>
        </div>
        <div className="stat-item icon-text-container">
          <Users size={16} className="icon" />
          <span>{targetAudience.length} Target Audiences</span>
        </div>
      </div>

      <div className="features-section">
        <div className="section-title">Key Features</div>
        <div className="features-list">
          {features.slice(0, 3).map((feature, index) => (
            <div key={index} className="feature-item">
              {feature}
            </div>
          ))}
          {features.length > 3 && (
            <div className="feature-item more-features">
              +{features.length - 3} more
            </div>
          )}
        </div>
      </div>

      <div className="audience-section">
        <div className="section-title">Target Audience</div>
        <div className="audience-tags">
          {targetAudience.slice(0, 2).map((audience, index) => (
            <span key={index} className="audience-tag">
              {audience}
            </span>
          ))}
          {targetAudience.length > 2 && (
            <span className="audience-tag more-audience">
              +{targetAudience.length - 2} more
            </span>
          )}
        </div>
      </div>

      <button className="expand-btn icon-text-container">
        View Details
        <ArrowRight size={16} className="icon" />
      </button>
    </div>
  );
};

export default ProductCard;
