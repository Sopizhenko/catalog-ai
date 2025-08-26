import React from 'react';

const Filters = ({ categories, selectedCategory, onCategoryFilter }) => {
  return (
    <div className="filters">
      <button
        className={`filter-btn ${selectedCategory === 'all' ? 'active' : ''}`}
        onClick={() => onCategoryFilter('all')}
      >
        All Products
      </button>
      
      {categories.map((category) => (
        <button
          key={category}
          className={`filter-btn ${selectedCategory === category ? 'active' : ''}`}
          onClick={() => onCategoryFilter(category)}
        >
          {category}
        </button>
      ))}
    </div>
  );
};

export default Filters;
