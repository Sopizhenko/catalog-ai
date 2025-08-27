import React from 'react';

const ProductGrid = ({ products, onProductClick }) => {
  if (products.length === 0) {
    return (
      <div className="no-results">
        <h3>No products found</h3>
        <p>Try adjusting your search terms or filters.</p>
      </div>
    );
  }

  return (
    <div className="products-grid">
      {products.map((product) => (
        <div
          key={product.id}
          className="product-card"
          onClick={() => onProductClick(product)}
        >
          <div className="product-header">
            <h3 className="product-name">{product.name}</h3>
            <span className="product-category">{product.category}</span>
          </div>
          
          <p className="product-description">{product.description}</p>
          
          <div className="product-features-preview">
            <div className="section-title">Key Features</div>
            <div className="features-preview">
              {product.features.slice(0, 3).map((feature, index) => (
                <span key={index} className="feature-tag">
                  {feature}
                </span>
              ))}
              {product.features.length > 3 && (
                <span className="feature-more">
                  +{product.features.length - 3} more
                </span>
              )}
            </div>
          </div>
          
          <div className="product-audience-preview">
            <div className="section-title">Target Audience</div>
            <div className="audience-preview">
              {product.targetAudience.slice(0, 2).map((audience, index) => (
                <span key={index} className="audience-tag">
                  {audience}
                </span>
              ))}
              {product.targetAudience.length > 2 && (
                <span className="audience-more">
                  +{product.targetAudience.length - 2} more
                </span>
              )}
            </div>
          </div>
          
          <div className="product-footer">
            <span className="view-details">View Details →</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProductGrid;