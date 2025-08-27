import React from 'react';
import { Filter, X } from 'lucide-react';

const FAQFilters = ({ 
  categories, 
  selectedCategory, 
  onCategoryChange, 
  hasActiveFilters,
  onClearFilters 
}) => {
  return (
    <div className="faq-filters">
      <div className="faq-filters-header">
        <div className="faq-filters-title">
          <Filter size={16} />
          <span>Filter by Category</span>
        </div>
        {hasActiveFilters && (
          <button 
            className="faq-filters-clear"
            onClick={onClearFilters}
          >
            <X size={14} />
            Clear Filters
          </button>
        )}
      </div>

      <div className="faq-filters-categories">
        <button
          className={`faq-category-filter ${selectedCategory === '' ? 'active' : ''}`}
          onClick={() => onCategoryChange('')}
        >
          All Categories
        </button>
        
        {categories.map((category) => (
          <button
            key={category.id}
            className={`faq-category-filter ${selectedCategory === category.id ? 'active' : ''}`}
            onClick={() => onCategoryChange(category.id)}
          >
            {category.name}
            <span className="faq-category-count">
              {category.faqCount}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default FAQFilters;
