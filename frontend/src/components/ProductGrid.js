import React from 'react';
import ProductCard from './ProductCard';

const ProductGrid = ({ products, onProductClick }) => {
  if (products.length === 0) {
    return (
      <div className="no-results">
        <h3>No products found</h3>
        <p>Try adjusting your search criteria or filters.</p>
      </div>
    );
  }

  return (
    <div className="products-grid">
      {products.map((product) => (
        <ProductCard
          key={product.id}
          product={product}
          onClick={() => onProductClick(product)}
        />
      ))}
    </div>
  );
};

export default ProductGrid;
