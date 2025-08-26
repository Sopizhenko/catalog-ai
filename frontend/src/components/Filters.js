import React from 'react';

const Filters = ({
  categories,
  audiences,
  selectedCategory,
  selectedAudience,
  onCategoryFilter,
  onAudienceFilter
}) => {
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
      
      <div style={{ width: '100%', height: '1px', margin: '10px 0' }}></div>
      
      <button
        className={`filter-btn ${selectedAudience === 'all' ? 'active' : ''}`}
        onClick={() => onAudienceFilter('all')}
      >
        All Audiences
      </button>
      
      {audiences.slice(0, 8).map((audience) => (
        <button
          key={audience}
          className={`filter-btn ${selectedAudience === audience ? 'active' : ''}`}
          onClick={() => onAudienceFilter(audience)}
        >
          {audience}
        </button>
      ))}
    </div>
  );
};

export default Filters;
