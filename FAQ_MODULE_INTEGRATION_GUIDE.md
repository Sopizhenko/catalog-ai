# FAQ System Integration Guide
# Catalog AI - Core FAQ System Integration

## Overview

This guide provides comprehensive instructions for integrating the FAQ system as a **core component** of the Catalog AI application. The FAQ system is not an add-on or separate module, but rather an essential part of the catalog experience that seamlessly integrates with the existing product and company data.

**Key Integration Principles:**
- FAQ is a **native feature** of the catalog system, not an optional plugin
- Maintains complete **visual and functional consistency** with existing components
- Leverages **shared data relationships** between FAQs, companies, and products
- Provides **unified user experience** across catalog browsing and FAQ sections
- Follows **identical patterns** for API design, component architecture, and styling

The integration ensures users experience FAQ as a natural extension of the catalog functionality, with seamless navigation, consistent design language, and intelligent cross-referencing between product information and FAQ content.

## Table of Contents

1. [Module Architecture](#module-architecture)
2. [Backend Implementation](#backend-implementation)
3. [Frontend Implementation](#frontend-implementation)
4. [Data Structure](#data-structure)
5. [API Endpoints](#api-endpoints)
6. [Component Architecture](#component-architecture)
7. [Styling Integration](#styling-integration)
8. [Security Considerations](#security-considerations)
9. [Performance Optimization](#performance-optimization)
10. [Testing Guidelines](#testing-guidelines)
11. [Deployment Instructions](#deployment-instructions)

## System Architecture Integration

The FAQ system is architected as a **core system component** that integrates directly into the existing catalog-ai infrastructure. It shares the same architectural patterns, follows identical conventions, and leverages the same underlying services and data structures as the product catalog functionality.

### Core Integration Points:
- **Unified Navigation**: FAQ and catalog share the same header and navigation system
- **Consistent API Design**: FAQ endpoints follow identical patterns to product/company APIs
- **Shared Service Layer**: FAQ service follows the same patterns as existing services
- **Common Component Architecture**: FAQ components use the same React patterns and hooks
- **Integrated Styling System**: FAQ styles extend the existing CSS variable system
- **Cross-Referenced Data**: FAQs can reference specific companies and products from catalog data

### Backend (Flask)
```
backend/
├── app.py                      # Updated with FAQ routes
├── data/
│   ├── companies.json         # Existing company data
│   └── faqs.json             # New FAQ data
├── services/
│   ├── market_analysis_service.py  # Existing service
│   └── faq_service.py        # New FAQ service
└── requirements.txt           # Updated dependencies
```

### Frontend (React)
```
frontend/src/
├── components/
│   ├── [existing components]
│   ├── FAQ/
│   │   ├── FAQContainer.js     # Main FAQ component
│   │   ├── FAQSearch.js        # Search functionality
│   │   ├── FAQFilters.js       # Category filters
│   │   ├── FAQItem.js          # Individual FAQ item
│   │   └── FAQModal.js         # FAQ detail modal
├── services/
│   └── api.js                 # Updated with FAQ endpoints
└── styles/
    ├── index.css              # Updated with FAQ variables
    └── faq.css                # FAQ-specific styles
```

## Backend Implementation

### 1. Update Flask Application (`backend/app.py`)

**IMPORTANT**: The FAQ routes are added directly to the main Flask application as core system endpoints, not as a separate blueprint or module. This ensures they are treated as first-class citizens in the API architecture.

Add the following FAQ routes to the existing Flask application:

```python
# Add to imports
from services.faq_service import FAQService

# Initialize FAQ service
faq_service = FAQService()

# FAQ Routes
@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    """
    Get all FAQs with optional filtering
    Query parameters:
    - search: Search query string
    - category: Category ID filter
    - limit: Number of results to return
    """
    try:
        search_query = request.args.get('search', '')
        category_id = request.args.get('category', '')
        limit = request.args.get('limit', type=int)
        
        faqs = faq_service.get_faqs(
            search_query=search_query,
            category_id=category_id,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'data': faqs,
            'total': len(faqs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faqs/<faq_id>', methods=['GET'])
def get_faq(faq_id):
    """Get specific FAQ by ID"""
    try:
        faq = faq_service.get_faq_by_id(faq_id)
        if not faq:
            return jsonify({'error': 'FAQ not found'}), 404
            
        return jsonify({
            'success': True,
            'data': faq
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faq-categories', methods=['GET'])
def get_faq_categories():
    """Get all FAQ categories"""
    try:
        categories = faq_service.get_categories()
        return jsonify({
            'success': True,
            'data': categories
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faq-search', methods=['POST'])
def search_faqs():
    """Advanced FAQ search with analytics tracking"""
    try:
        data = request.get_json()
        search_query = data.get('query', '')
        filters = data.get('filters', {})
        
        results = faq_service.advanced_search(search_query, filters)
        
        # Track search analytics (optional)
        faq_service.track_search(search_query, len(results))
        
        return jsonify({
            'success': True,
            'data': results,
            'query': search_query,
            'total': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faqs/<faq_id>/related', methods=['GET'])
def get_faq_related_content(faq_id):
    """Get companies and products related to specific FAQ - demonstrates catalog integration"""
    try:
        related_content = faq_service.get_related_content(faq_id)
        return jsonify({
            'success': True,
            'data': related_content,
            'faq_id': faq_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 2. Create FAQ Service (`backend/services/faq_service.py`)

```python
import json
import os
from typing import List, Dict, Optional

class FAQService:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faqs.json')
        self._load_data()
    
    def _load_data(self):
        """Load FAQ data from JSON file"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.faqs = data.get('faqs', [])
                self.categories = data.get('categories', [])
        except FileNotFoundError:
            self.faqs = []
            self.categories = []
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in FAQ data file: {e}")
    
    def get_faqs(self, search_query: str = '', category_id: str = '', limit: Optional[int] = None) -> List[Dict]:
        """Get filtered FAQs"""
        results = self.faqs.copy()
        
        # Filter by category
        if category_id:
            results = [faq for faq in results if faq.get('categoryId') == category_id]
        
        # Filter by search query
        if search_query:
            query_lower = search_query.lower()
            filtered_results = []
            
            for faq in results:
                # Search in question, answer, keywords, and search terms
                searchable_text = ' '.join([
                    faq.get('question', ''),
                    faq.get('answer', ''),
                    ' '.join(faq.get('keywords', [])),
                    ' '.join(faq.get('searchTerms', []))
                ]).lower()
                
                if query_lower in searchable_text:
                    filtered_results.append(faq)
            
            results = filtered_results
        
        # Apply limit
        if limit:
            results = results[:limit]
        
        # Enrich with category information
        for faq in results:
            category = next((cat for cat in self.categories if cat['id'] == faq.get('categoryId')), None)
            if category:
                faq['categoryName'] = category['name']
        
        return results
    
    def get_faq_by_id(self, faq_id: str) -> Optional[Dict]:
        """Get specific FAQ by ID"""
        faq = next((f for f in self.faqs if f['id'] == faq_id), None)
        
        if faq:
            # Enrich with category information
            category = next((cat for cat in self.categories if cat['id'] == faq.get('categoryId')), None)
            if category:
                faq['categoryName'] = category['name']
        
        return faq
    
    def get_categories(self) -> List[Dict]:
        """Get all categories with FAQ counts"""
        categories_with_counts = []
        
        for category in self.categories:
            faq_count = len([faq for faq in self.faqs if faq.get('categoryId') == category['id']])
            category_with_count = category.copy()
            category_with_count['faqCount'] = faq_count
            categories_with_counts.append(category_with_count)
        
        return categories_with_counts
    
    def advanced_search(self, query: str, filters: Dict) -> List[Dict]:
        """Advanced search with multiple filters"""
        results = self.faqs.copy()
        
        # Apply category filter
        if filters.get('category'):
            results = [faq for faq in results if faq.get('categoryId') == filters['category']]
        
        # Apply keyword filter
        if filters.get('keywords'):
            keyword_filter = [kw.lower() for kw in filters['keywords']]
            results = [
                faq for faq in results 
                if any(kw in ' '.join(faq.get('keywords', [])).lower() for kw in keyword_filter)
            ]
        
        # Apply text search
        if query:
            query_lower = query.lower()
            scored_results = []
            
            for faq in results:
                score = 0
                
                # Score based on query location
                if query_lower in faq.get('question', '').lower():
                    score += 10
                if query_lower in faq.get('answer', '').lower():
                    score += 5
                if any(query_lower in kw.lower() for kw in faq.get('keywords', [])):
                    score += 8
                if any(query_lower in term.lower() for term in faq.get('searchTerms', [])):
                    score += 6
                
                if score > 0:
                    faq_copy = faq.copy()
                    faq_copy['searchScore'] = score
                    scored_results.append(faq_copy)
            
            # Sort by score descending
            results = sorted(scored_results, key=lambda x: x['searchScore'], reverse=True)
        
        return results
    
    def get_related_content(self, faq_id: str) -> Dict:
        """Get related companies and products for FAQ cross-referencing"""
        faq = self.get_faq_by_id(faq_id)
        if not faq:
            return {}
        
        # This method demonstrates how FAQ integrates with catalog data
        # Load company data (reusing existing data loading patterns)
        from services.company_service import load_data as load_company_data
        
        try:
            company_data = load_company_data()
            companies = company_data.get('companies', [])
            
            related_companies = []
            related_products = []
            
            # Find companies/products mentioned in FAQ keywords
            faq_keywords = [kw.lower() for kw in faq.get('keywords', [])]
            
            for company in companies:
                # Check if company is mentioned in FAQ
                company_terms = [
                    company.get('company', '').lower(),
                    company.get('parentCompany', '').lower()
                ]
                
                if any(term for term in company_terms if term and any(kw in term for kw in faq_keywords)):
                    related_companies.append({
                        'company': company.get('company'),
                        'description': company.get('description', ''),
                        'industry': company.get('industry', '')
                    })
                
                # Check products
                for product in company.get('products', []):
                    product_terms = [
                        product.get('name', '').lower(),
                        product.get('category', '').lower()
                    ] + [feature.lower() for feature in product.get('features', [])]
                    
                    if any(term for term in product_terms if term and any(kw in term for kw in faq_keywords)):
                        related_products.append({
                            'id': product.get('id'),
                            'name': product.get('name'),
                            'company': company.get('company'),
                            'category': product.get('category', ''),
                            'description': product.get('description', '')
                        })
            
            return {
                'companies': related_companies[:5],  # Limit to 5 most relevant
                'products': related_products[:5]
            }
            
        except Exception as e:
            print(f"Error loading related content: {e}")
            return {'companies': [], 'products': []}
    
    def track_search(self, query: str, result_count: int):
        """Track search analytics (implement as needed)"""
        # This could log to a file, database, or analytics service
        print(f"FAQ Search: '{query}' returned {result_count} results")
```

### 3. Create FAQ Data File (`backend/data/faqs.json`)

Copy the content from `confirma_faqs_json.json` to `backend/data/faqs.json`.

## Frontend Implementation

### 1. Update API Service (`frontend/src/services/api.js`)

Add FAQ-related API methods to the existing API service:

```javascript
// Add to existing catalogAPI object
const catalogAPI = {
  // ... existing methods

  // FAQ Methods
  faqs: {
    // Get all FAQs with optional filtering
    getAll: (params = {}) => {
      const queryParams = new URLSearchParams();
      
      if (params.search) queryParams.append('search', params.search);
      if (params.category) queryParams.append('category', params.category);
      if (params.limit) queryParams.append('limit', params.limit);
      
      const url = queryParams.toString() ? `/api/faqs?${queryParams}` : '/api/faqs';
      return api.get(url);
    },

    // Get specific FAQ
    getById: (id) => api.get(`/api/faqs/${id}`),

    // Get FAQ categories
    getCategories: () => api.get('/api/faq-categories'),

    // Advanced search
    search: (query, filters = {}) => 
      api.post('/api/faq-search', { query, filters }),

    // Get related companies and products for FAQ integration
    getRelatedContent: (faqId) => 
      api.get(`/api/faqs/${faqId}/related`)
  }
};
```

### 2. Create FAQ Container Component (`frontend/src/components/FAQ/FAQContainer.js`)

**Integration Note**: This component follows the exact same patterns as existing components like `ProductGrid` and `CompanySelector`. It uses the same state management patterns, loading states, error handling, and API interaction methods to maintain consistency across the application.

```jsx
import React, { useState, useEffect, useCallback } from 'react';
import { Search, Filter, MessageCircle } from 'lucide-react';
import catalogAPI from '../../services/api';
import FAQSearch from './FAQSearch';
import FAQFilters from './FAQFilters';
import FAQItem from './FAQItem';
import FAQModal from './FAQModal';
import LoadingSpinner from '../LoadingSpinner';

const FAQContainer = () => {
  const [faqs, setFaqs] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedFAQ, setSelectedFAQ] = useState(null);
  const [searchResults, setSearchResults] = useState(null);

  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const [faqsResponse, categoriesResponse] = await Promise.all([
          catalogAPI.faqs.getAll(),
          catalogAPI.faqs.getCategories()
        ]);

        setFaqs(faqsResponse.data.data || []);
        setCategories(categoriesResponse.data.data || []);
        setError(null);
      } catch (err) {
        setError('Failed to load FAQ data');
        console.error('FAQ loading error:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Debounced search
  const debounceTimeout = React.useRef(null);
  
  const handleSearch = useCallback((query) => {
    setSearchQuery(query);
    
    if (debounceTimeout.current) {
      clearTimeout(debounceTimeout.current);
    }

    debounceTimeout.current = setTimeout(async () => {
      if (query.trim()) {
        try {
          const response = await catalogAPI.faqs.search(query, {
            category: selectedCategory
          });
          setSearchResults(response.data.data);
        } catch (err) {
          console.error('FAQ search error:', err);
        }
      } else {
        setSearchResults(null);
      }
    }, 300);
  }, [selectedCategory]);

  // Category filter
  const handleCategoryFilter = async (categoryId) => {
    setSelectedCategory(categoryId);
    setSearchResults(null);
    
    try {
      const response = await catalogAPI.faqs.getAll({
        category: categoryId,
        search: searchQuery
      });
      setFaqs(response.data.data || []);
    } catch (err) {
      console.error('FAQ filter error:', err);
    }
  };

  // FAQ selection
  const handleFAQSelect = (faq) => {
    setSelectedFAQ(faq);
  };

  // Clear filters
  const handleClearFilters = async () => {
    setSearchQuery('');
    setSelectedCategory('');
    setSearchResults(null);
    
    try {
      const response = await catalogAPI.faqs.getAll();
      setFaqs(response.data.data || []);
    } catch (err) {
      console.error('FAQ clear filters error:', err);
    }
  };

  const displayedFAQs = searchResults || faqs;
  const hasActiveFilters = searchQuery || selectedCategory;

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="faq-error">
        <MessageCircle size={48} />
        <h3>Error Loading FAQs</h3>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="faq-container">
      <div className="faq-header">
        <h1>Frequently Asked Questions</h1>
        <p>Find answers to common questions about our software solutions</p>
      </div>

      <FAQSearch
        searchQuery={searchQuery}
        onSearch={handleSearch}
        onClear={() => handleSearch('')}
      />

      <FAQFilters
        categories={categories}
        selectedCategory={selectedCategory}
        onCategoryChange={handleCategoryFilter}
        hasActiveFilters={hasActiveFilters}
        onClearFilters={handleClearFilters}
      />

      {hasActiveFilters && (
        <div className="faq-results-info">
          Showing {displayedFAQs.length} result{displayedFAQs.length !== 1 ? 's' : ''}
          {searchQuery && ` for "${searchQuery}"`}
        </div>
      )}

      <div className="faq-grid">
        {displayedFAQs.length === 0 ? (
          <div className="faq-no-results">
            <MessageCircle size={48} />
            <h3>No FAQs Found</h3>
            <p>
              {hasActiveFilters
                ? 'Try adjusting your search terms or filters'
                : 'No FAQs are available at this time'
              }
            </p>
          </div>
        ) : (
          displayedFAQs.map((faq) => (
            <FAQItem
              key={faq.id}
              faq={faq}
              searchQuery={searchQuery}
              onClick={handleFAQSelect}
            />
          ))
        )}
      </div>

      {selectedFAQ && (
        <FAQModal
          faq={selectedFAQ}
          onClose={() => setSelectedFAQ(null)}
        />
      )}
    </div>
  );
};

export default FAQContainer;
```

### 3. Create FAQ Search Component (`frontend/src/components/FAQ/FAQSearch.js`)

```jsx
import React from 'react';
import { Search, X } from 'lucide-react';

const FAQSearch = ({ searchQuery, onSearch, onClear }) => {
  const handleInputChange = (e) => {
    onSearch(e.target.value);
  };

  const handleClear = () => {
    onClear();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      handleClear();
    }
  };

  return (
    <div className="faq-search">
      <div className="faq-search-container">
        <div className="faq-search-input-wrapper">
          <Search className="faq-search-icon" size={20} />
          <input
            type="text"
            className="faq-search-input"
            placeholder="Search FAQs, topics, or keywords..."
            value={searchQuery}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            autoComplete="off"
          />
          {searchQuery && (
            <button
              className="faq-search-clear"
              onClick={handleClear}
              aria-label="Clear search"
            >
              <X size={16} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default FAQSearch;
```

### 4. Create FAQ Filters Component (`frontend/src/components/FAQ/FAQFilters.js`)

```jsx
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
```

### 5. Create FAQ Item Component (`frontend/src/components/FAQ/FAQItem.js`)

```jsx
import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Tag, ExternalLink } from 'lucide-react';

const FAQItem = ({ faq, searchQuery, onClick }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  const handleViewDetails = (e) => {
    e.stopPropagation();
    onClick(faq);
  };

  // Highlight search terms in text
  const highlightText = (text, query) => {
    if (!query) return text;
    
    const regex = new RegExp(`(${query})`, 'gi');
    const parts = text.split(regex);
    
    return parts.map((part, index) => 
      regex.test(part) ? 
        <mark key={index} className="faq-highlight">{part}</mark> : 
        part
    );
  };

  return (
    <div className={`faq-item ${isExpanded ? 'expanded' : ''}`}>
      <div className="faq-item-header" onClick={toggleExpanded}>
        <div className="faq-item-title">
          <h3>{highlightText(faq.question, searchQuery)}</h3>
          {faq.categoryName && (
            <span className="faq-item-category">
              {faq.categoryName}
            </span>
          )}
        </div>
        <button className="faq-item-toggle">
          {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
        </button>
      </div>

      <div className={`faq-item-content ${isExpanded ? 'expanded' : ''}`}>
        <div className="faq-item-answer">
          {highlightText(faq.answer, searchQuery)}
        </div>

        {faq.keywords && faq.keywords.length > 0 && (
          <div className="faq-item-keywords">
            <Tag size={14} />
            <div className="faq-keywords-list">
              {faq.keywords.map((keyword, index) => (
                <span key={index} className="faq-keyword">
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="faq-item-actions">
          <button 
            className="faq-item-detail-btn"
            onClick={handleViewDetails}
          >
            <ExternalLink size={14} />
            View Details
          </button>
        </div>
      </div>
    </div>
  );
};

export default FAQItem;
```

### 6. Create FAQ Modal Component (`frontend/src/components/FAQ/FAQModal.js`)

```jsx
import React, { useEffect } from 'react';
import { X, Tag, Info } from 'lucide-react';

const FAQModal = ({ faq, onClose }) => {
  // Close modal on escape key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    document.body.style.overflow = 'hidden';

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [onClose]);

  // Close modal on backdrop click
  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="faq-modal-backdrop" onClick={handleBackdropClick}>
      <div className="faq-modal">
        <div className="faq-modal-header">
          <div className="faq-modal-title">
            <Info size={20} />
            <h2>FAQ Details</h2>
          </div>
          <button 
            className="faq-modal-close"
            onClick={onClose}
            aria-label="Close modal"
          >
            <X size={20} />
          </button>
        </div>

        <div className="faq-modal-content">
          {faq.categoryName && (
            <div className="faq-modal-category">
              {faq.categoryName}
            </div>
          )}

          <h3 className="faq-modal-question">
            {faq.question}
          </h3>

          <div className="faq-modal-answer">
            {faq.answer}
          </div>

          {faq.keywords && faq.keywords.length > 0 && (
            <div className="faq-modal-keywords">
              <div className="faq-modal-keywords-title">
                <Tag size={16} />
                <span>Related Topics</span>
              </div>
              <div className="faq-modal-keywords-list">
                {faq.keywords.map((keyword, index) => (
                  <span key={index} className="faq-modal-keyword">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}

          {faq.searchTerms && faq.searchTerms.length > 0 && (
            <div className="faq-modal-search-terms">
              <strong>Also searched as:</strong>
              <p>{faq.searchTerms.join(', ')}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FAQModal;
```

## Styling Integration

### 1. Update CSS Variables (`frontend/src/styles/index.css`)

Add FAQ-specific CSS variables to the existing color scheme:

```css
:root {
  /* Existing variables... */
  
  /* FAQ Module Variables */
  --faq-primary: var(--primary-blue);
  --faq-secondary: var(--secondary-gray);
  --faq-background: var(--background-light);
  --faq-surface: var(--surface-white);
  --faq-border: var(--border-light);
  --faq-text-primary: var(--text-dark);
  --faq-text-secondary: var(--text-gray);
  --faq-hover: var(--hover-blue);
  --faq-highlight: var(--accent-yellow);
  --faq-success: var(--success-green);
  --faq-shadow-sm: var(--shadow-light);
  --faq-shadow-md: var(--shadow-medium);
  --faq-border-radius: var(--border-radius);
  --faq-transition: var(--transition-smooth);
}
```

### 2. Create FAQ Styles (`frontend/src/styles/faq.css`)

```css
/* FAQ Container */
.faq-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background: var(--faq-background);
  min-height: 100vh;
}

.faq-header {
  text-align: center;
  margin-bottom: 3rem;
}

.faq-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--faq-primary);
  margin-bottom: 1rem;
  font-family: var(--font-sofia-pro);
}

.faq-header p {
  font-size: 1.1rem;
  color: var(--faq-text-secondary);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* FAQ Search */
.faq-search {
  margin-bottom: 2rem;
}

.faq-search-container {
  background: var(--faq-surface);
  padding: 2rem;
  border-radius: var(--faq-border-radius);
  box-shadow: var(--faq-shadow-sm);
  border: 1px solid var(--faq-border);
}

.faq-search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.faq-search-icon {
  position: absolute;
  left: 1rem;
  color: var(--faq-text-secondary);
  z-index: 2;
}

.faq-search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  font-size: 1.1rem;
  border: 2px solid var(--faq-border);
  border-radius: var(--faq-border-radius);
  background: var(--faq-surface);
  color: var(--faq-text-primary);
  transition: var(--faq-transition);
}

.faq-search-input:focus {
  outline: none;
  border-color: var(--faq-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.faq-search-clear {
  position: absolute;
  right: 1rem;
  background: var(--faq-text-secondary);
  border: none;
  border-radius: 50%;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--faq-transition);
  color: white;
}

.faq-search-clear:hover {
  background: var(--faq-primary);
  transform: scale(1.1);
}

/* FAQ Filters */
.faq-filters {
  background: var(--faq-surface);
  padding: 1.5rem;
  border-radius: var(--faq-border-radius);
  box-shadow: var(--faq-shadow-sm);
  border: 1px solid var(--faq-border);
  margin-bottom: 2rem;
}

.faq-filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.faq-filters-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: var(--faq-text-primary);
}

.faq-filters-clear {
  background: transparent;
  border: 1px solid var(--faq-border);
  padding: 0.5rem 1rem;
  border-radius: var(--faq-border-radius);
  color: var(--faq-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: var(--faq-transition);
  font-size: 0.9rem;
}

.faq-filters-clear:hover {
  background: var(--faq-hover);
  color: white;
  border-color: var(--faq-hover);
}

.faq-filters-categories {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.faq-category-filter {
  background: var(--faq-surface);
  border: 2px solid var(--faq-border);
  padding: 0.75rem 1.25rem;
  border-radius: var(--faq-border-radius);
  color: var(--faq-text-primary);
  cursor: pointer;
  transition: var(--faq-transition);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.faq-category-filter:hover {
  border-color: var(--faq-primary);
  background: var(--faq-hover);
  color: white;
}

.faq-category-filter.active {
  background: var(--faq-primary);
  border-color: var(--faq-primary);
  color: white;
}

.faq-category-count {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 600;
}

.faq-category-filter.active .faq-category-count {
  background: rgba(255, 255, 255, 0.3);
}

/* Results Info */
.faq-results-info {
  margin-bottom: 1.5rem;
  padding: 1rem 1.5rem;
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: var(--faq-border-radius);
  color: var(--faq-primary);
  font-weight: 500;
}

/* FAQ Grid */
.faq-grid {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

/* FAQ Item */
.faq-item {
  background: var(--faq-surface);
  border-radius: var(--faq-border-radius);
  box-shadow: var(--faq-shadow-sm);
  border: 1px solid var(--faq-border);
  overflow: hidden;
  transition: var(--faq-transition);
}

.faq-item:hover {
  box-shadow: var(--faq-shadow-md);
  transform: translateY(-2px);
}

.faq-item-header {
  padding: 1.5rem;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  transition: var(--faq-transition);
}

.faq-item-header:hover {
  background: rgba(59, 130, 246, 0.05);
}

.faq-item-title h3 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--faq-text-primary);
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

.faq-item-category {
  display: inline-block;
  background: var(--faq-success);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
}

.faq-item-toggle {
  background: var(--faq-primary);
  border: none;
  border-radius: 50%;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--faq-transition);
  color: white;
  flex-shrink: 0;
}

.faq-item-toggle:hover {
  background: var(--faq-hover);
  transform: scale(1.1);
}

.faq-item.expanded .faq-item-toggle {
  transform: rotate(180deg);
}

/* FAQ Item Content */
.faq-item-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease-out;
}

.faq-item-content.expanded {
  max-height: 1000px;
}

.faq-item-answer {
  padding: 0 1.5rem 1rem;
  color: var(--faq-text-secondary);
  line-height: 1.7;
}

.faq-item-keywords {
  padding: 0 1.5rem 1rem;
  border-top: 1px solid var(--faq-border);
  margin: 1rem 1.5rem 0;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.faq-item-keywords svg {
  color: var(--faq-text-secondary);
  margin-top: 0.25rem;
  flex-shrink: 0;
}

.faq-keywords-list {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.faq-keyword {
  background: rgba(59, 130, 246, 0.1);
  color: var(--faq-primary);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
}

.faq-item-actions {
  padding: 0 1.5rem 1.5rem;
}

.faq-item-detail-btn {
  background: transparent;
  border: 1px solid var(--faq-primary);
  color: var(--faq-primary);
  padding: 0.5rem 1rem;
  border-radius: var(--faq-border-radius);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: var(--faq-transition);
  font-size: 0.9rem;
  font-weight: 500;
}

.faq-item-detail-btn:hover {
  background: var(--faq-primary);
  color: white;
}

/* Search Highlight */
.faq-highlight {
  background: var(--faq-highlight);
  padding: 0.1rem 0.2rem;
  border-radius: 0.2rem;
  font-weight: 600;
}

/* FAQ Modal */
.faq-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.faq-modal {
  background: var(--faq-surface);
  border-radius: var(--faq-border-radius);
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--faq-shadow-md);
  animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.faq-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid var(--faq-border);
}

.faq-modal-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.faq-modal-title h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--faq-text-primary);
}

.faq-modal-close {
  background: transparent;
  border: none;
  color: var(--faq-text-secondary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: var(--faq-transition);
}

.faq-modal-close:hover {
  background: var(--faq-border);
  color: var(--faq-text-primary);
}

.faq-modal-content {
  padding: 2rem;
}

.faq-modal-category {
  display: inline-block;
  background: var(--faq-success);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: var(--faq-border-radius);
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
}

.faq-modal-question {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--faq-text-primary);
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

.faq-modal-answer {
  color: var(--faq-text-secondary);
  line-height: 1.7;
  margin-bottom: 2rem;
  font-size: 1rem;
}

.faq-modal-keywords {
  border-top: 1px solid var(--faq-border);
  padding-top: 1.5rem;
  margin-top: 1.5rem;
}

.faq-modal-keywords-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: var(--faq-text-primary);
}

.faq-modal-keywords-list {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.faq-modal-keyword {
  background: rgba(59, 130, 246, 0.1);
  color: var(--faq-primary);
  padding: 0.5rem 1rem;
  border-radius: var(--faq-border-radius);
  font-size: 0.9rem;
  font-weight: 500;
}

.faq-modal-search-terms {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--faq-border);
  color: var(--faq-text-secondary);
}

.faq-modal-search-terms strong {
  color: var(--faq-text-primary);
}

/* No Results */
.faq-no-results {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--faq-text-secondary);
}

.faq-no-results svg {
  margin-bottom: 1rem;
  color: var(--faq-text-secondary);
}

.faq-no-results h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--faq-text-primary);
}

/* Error State */
.faq-error {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--faq-text-secondary);
}

.faq-error svg {
  margin-bottom: 1rem;
  color: var(--faq-text-secondary);
}

.faq-error h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: var(--faq-text-primary);
}

.faq-error button {
  background: var(--faq-primary);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: var(--faq-border-radius);
  cursor: pointer;
  font-weight: 600;
  margin-top: 1rem;
  transition: var(--faq-transition);
}

.faq-error button:hover {
  background: var(--faq-hover);
  transform: translateY(-2px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .faq-container {
    padding: 1rem;
  }

  .faq-header h1 {
    font-size: 2rem;
  }

  .faq-search-container {
    padding: 1.5rem;
  }

  .faq-filters {
    padding: 1rem;
  }

  .faq-filters-categories {
    flex-direction: column;
    gap: 0.75rem;
  }

  .faq-category-filter {
    text-align: center;
    justify-content: center;
  }

  .faq-item-header {
    padding: 1rem;
  }

  .faq-item-answer,
  .faq-item-keywords {
    padding: 0 1rem 1rem;
  }

  .faq-item-keywords {
    margin: 1rem 1rem 0;
  }

  .faq-item-actions {
    padding: 0 1rem 1rem;
  }

  .faq-modal-backdrop {
    padding: 1rem;
  }

  .faq-modal-header,
  .faq-modal-content {
    padding: 1.5rem;
  }

  .faq-modal-question {
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .faq-header h1 {
    font-size: 1.8rem;
  }

  .faq-item-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .faq-item-toggle {
    align-self: flex-end;
  }

  .faq-modal {
    margin: 1rem;
  }
}
```

### 3. Update Main App Component (`frontend/src/App.js`)

**Core Integration**: FAQ is integrated as a primary navigation option alongside the catalog, not as a secondary feature. The view switching logic treats FAQ and catalog as equal, core features of the system.

Add FAQ routing and component integration:

```jsx
import React, { useState } from 'react';
import Header from './components/Header';
import CompanySelector from './components/CompanySelector';
import ProductGrid from './components/ProductGrid';
import ProductModal from './components/ProductModal';
import FAQContainer from './components/FAQ/FAQContainer';
import './styles/index.css';
import './styles/faq.css';

function App() {
  const [currentView, setCurrentView] = useState('catalog'); // 'catalog' or 'faq'
  // ... existing state

  const renderCurrentView = () => {
    switch (currentView) {
      case 'faq':
        return <FAQContainer />;
      case 'catalog':
      default:
        return (
          <>
            <CompanySelector 
              selectedCompany={selectedCompany}
              onCompanySelect={setSelectedCompany}
            />
            <ProductGrid 
              selectedCompany={selectedCompany}
              searchQuery={searchQuery}
              selectedCategory={selectedCategory}
              selectedAudience={selectedAudience}
              onProductSelect={setSelectedProduct}
              onSearchChange={setSearchQuery}
              onCategoryChange={setSelectedCategory}
              onAudienceChange={setSelectedAudience}
            />
          </>
        );
    }
  };

  return (
    <div className="App">
      <Header 
        currentView={currentView}
        onViewChange={setCurrentView}
      />
      
      {renderCurrentView()}

      {selectedProduct && (
        <ProductModal 
          product={selectedProduct}
          onClose={() => setSelectedProduct(null)}
        />
      )}
    </div>
  );
}

export default App;
```

### 4. Update Header Component (`frontend/src/components/Header.js`)

Add FAQ navigation:

```jsx
import React from 'react';
import { MessageCircle, Package, Search } from 'lucide-react';

const Header = ({ currentView, onViewChange }) => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-logo">
          <Package className="header-icon" />
          <h1>Catalog AI</h1>
        </div>
        
        <nav className="header-nav">
          <button 
            className={`nav-button ${currentView === 'catalog' ? 'active' : ''}`}
            onClick={() => onViewChange('catalog')}
          >
            <Search size={16} />
            Catalog
          </button>
          <button 
            className={`nav-button ${currentView === 'faq' ? 'active' : ''}`}
            onClick={() => onViewChange('faq')}
          >
            <MessageCircle size={16} />
            FAQ
          </button>
        </nav>
      </div>
    </header>
  );
};

export default Header;
```

## Data Structure

The FAQ system uses the following JSON structure in `backend/data/faqs.json`:

```json
{
  "categories": [
    {
      "id": "string",           // Unique category identifier
      "name": "string",         // Display name
      "description": "string"   // Category description
    }
  ],
  "faqs": [
    {
      "id": "string",           // Unique FAQ identifier  
      "question": "string",     // The FAQ question
      "answer": "string",       // The answer (supports basic HTML)
      "categoryId": "string",   // References category.id
      "keywords": ["string"],   // Array of relevant keywords
      "searchTerms": ["string"] // Additional search terms
    }
  ]
}
```

## API Endpoints

The FAQ system adds the following core REST API endpoints that follow the same patterns as existing catalog endpoints (`/api/companies`, `/api/products`):

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/api/faqs` | Get all FAQs with optional filtering | `search`, `category`, `limit` |
| GET | `/api/faqs/{id}` | Get specific FAQ by ID | - |
| GET | `/api/faqs/{id}/related` | Get related companies and products for FAQ | - |
| GET | `/api/faq-categories` | Get all FAQ categories with counts | - |
| POST | `/api/faq-search` | Advanced FAQ search | `{query, filters}` |

### Example API Responses

**GET /api/faqs**
```json
{
  "success": true,
  "data": [
    {
      "id": "faq_001",
      "question": "What is Confirma Software?",
      "answer": "Confirma Software is a leading Nordic software company...",
      "categoryId": "general_information",
      "categoryName": "General Information",
      "keywords": ["company overview", "nordic", "software"],
      "searchTerms": ["about confirma", "services offered"]
    }
  ],
  "total": 45
}
```

**GET /api/faq-categories**
```json
{
  "success": true,
  "data": [
    {
      "id": "general_information",
      "name": "General Information",
      "description": "Company information and general inquiries",
      "faqCount": 8
    }
  ]
}
```

## Security Considerations

### Input Validation
- Sanitize search queries to prevent injection attacks
- Validate category IDs against allowed values
- Implement rate limiting for search endpoints

### API Security
```python
from flask import request
import re

def validate_search_query(query):
    # Remove potentially dangerous characters
    if len(query) > 200:
        raise ValueError("Search query too long")
    
    # Basic XSS prevention
    query = re.sub(r'[<>\"\'&]', '', query)
    return query.strip()

@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    search_query = request.args.get('search', '')
    if search_query:
        search_query = validate_search_query(search_query)
    
    # ... rest of the implementation
```

### Content Security
- Sanitize FAQ answers if they contain HTML
- Implement proper CORS headers
- Use HTTPS in production

## Performance Optimization

### Backend Optimizations
```python
# Cache FAQ data in memory
class FAQService:
    def __init__(self):
        self._cache = {}
        self._cache_timestamp = 0
        self.cache_duration = 300  # 5 minutes
    
    def get_cached_faqs(self):
        current_time = time.time()
        if (current_time - self._cache_timestamp) > self.cache_duration:
            self._load_data()
            self._cache_timestamp = current_time
        return self._cache.get('faqs', [])
```

### Frontend Optimizations
```jsx
// Implement search debouncing
const useDebounce = (value, delay) => {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);
  
  return debouncedValue;
};

// Use React.memo for expensive components
const FAQItem = React.memo(({ faq, searchQuery, onClick }) => {
  // Component implementation
});
```

### Database Considerations (Future Enhancement)
For large FAQ datasets, consider migrating to a database:

```python
# Example with SQLAlchemy
class FAQ(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.String(50), db.ForeignKey('category.id'))
    keywords = db.Column(db.JSON)
    search_terms = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Full-text search index
    __searchable__ = ['question', 'answer']
```

## Testing Guidelines

### Backend Tests (`tests/test_faq_service.py`)
```python
import unittest
from backend.services.faq_service import FAQService

class TestFAQService(unittest.TestCase):
    def setUp(self):
        self.faq_service = FAQService()
    
    def test_get_all_faqs(self):
        faqs = self.faq_service.get_faqs()
        self.assertIsInstance(faqs, list)
        self.assertGreater(len(faqs), 0)
    
    def test_search_functionality(self):
        results = self.faq_service.get_faqs(search_query='confirma')
        self.assertIsInstance(results, list)
        
        # Verify search results contain query term
        for faq in results:
            searchable_text = (
                faq['question'] + faq['answer'] + 
                ' '.join(faq.get('keywords', [])) +
                ' '.join(faq.get('searchTerms', []))
            ).lower()
            self.assertIn('confirma', searchable_text)
    
    def test_category_filtering(self):
        results = self.faq_service.get_faqs(category_id='general_information')
        for faq in results:
            self.assertEqual(faq['categoryId'], 'general_information')
```

### Frontend Tests (`src/components/FAQ/__tests__/FAQContainer.test.js`)
```jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import FAQContainer from '../FAQContainer';
import catalogAPI from '../../../services/api';

// Mock API
jest.mock('../../../services/api');

describe('FAQContainer', () => {
  const mockFAQs = [
    {
      id: 'faq_001',
      question: 'Test question',
      answer: 'Test answer',
      categoryId: 'general',
      keywords: ['test']
    }
  ];
  
  const mockCategories = [
    {
      id: 'general',
      name: 'General',
      faqCount: 1
    }
  ];
  
  beforeEach(() => {
    catalogAPI.faqs.getAll.mockResolvedValue({ data: { data: mockFAQs } });
    catalogAPI.faqs.getCategories.mockResolvedValue({ data: { data: mockCategories } });
  });
  
  test('renders FAQ container with search and filters', async () => {
    render(<FAQContainer />);
    
    await waitFor(() => {
      expect(screen.getByText('Frequently Asked Questions')).toBeInTheDocument();
      expect(screen.getByPlaceholderText(/search faqs/i)).toBeInTheDocument();
      expect(screen.getByText('Filter by Category')).toBeInTheDocument();
    });
  });
  
  test('performs search when typing in search input', async () => {
    render(<FAQContainer />);
    
    const searchInput = screen.getByPlaceholderText(/search faqs/i);
    fireEvent.change(searchInput, { target: { value: 'test query' } });
    
    await waitFor(() => {
      expect(catalogAPI.faqs.search).toHaveBeenCalledWith('test query', expect.any(Object));
    }, { timeout: 500 });
  });
});
```

### API Tests (`tests/test_faq_routes.py`)
```python
import unittest
import json
from backend.app import app

class TestFAQRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_get_faqs_endpoint(self):
        response = self.app.get('/api/faqs')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], list)
    
    def test_get_faqs_with_search(self):
        response = self.app.get('/api/faqs?search=confirma')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_get_single_faq(self):
        response = self.app.get('/api/faqs/faq_001')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
    
    def test_get_categories(self):
        response = self.app.get('/api/faq-categories')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
```

## Deployment Instructions

### 1. Backend Deployment Updates

Update `requirements.txt`:
```txt
Flask==2.3.3
Flask-CORS==4.0.0
python-dotenv==1.0.0
# Add any new dependencies
```

### 2. Production Configuration

Update `backend/app.py` for production:
```python
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Production CORS configuration
if os.getenv('FLASK_ENV') == 'production':
    CORS(app, origins=['https://yourdomain.com'])
else:
    CORS(app)

# Production error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500
```

### 3. Environment Variables

Create `.env` file:
```env
FLASK_ENV=production
FAQ_CACHE_DURATION=300
MAX_SEARCH_RESULTS=100
RATE_LIMIT_PER_MINUTE=60
```

### 4. Frontend Build Configuration

Update `frontend/package.json` build script:
```json
{
  "scripts": {
    "build": "react-scripts build && npm run copy-faq-assets",
    "copy-faq-assets": "cp -r src/styles/faq.css build/static/css/"
  }
}
```

### 5. Docker Configuration (Optional)

Create `Dockerfile` for containerized deployment:
```dockerfile
# Multi-stage build for production
FROM node:16-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ .
RUN npm run build

FROM python:3.9-slim AS backend
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
COPY --from=frontend-build /app/frontend/build ./static

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### 6. CI/CD Pipeline Updates

Update `.github/workflows/deploy.yml`:
```yaml
name: Deploy FAQ Module
on:
  push:
    branches: [main]
    paths: 
      - 'backend/**'
      - 'frontend/**'
      - 'FAQ_MODULE_INTEGRATION_GUIDE.md'

jobs:
  test-faq:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Test Backend FAQ Service
        run: |
          cd backend
          python -m pytest tests/test_faq* -v
      
      - name: Test Frontend FAQ Components  
        run: |
          cd frontend
          npm test -- --watchAll=false --testPathPattern=FAQ
  
  deploy:
    needs: test-faq
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: |
          # Your deployment commands here
```

### 7. Monitoring and Analytics

Add FAQ usage analytics:
```python
# backend/services/analytics_service.py
import json
import datetime

class FAQAnalytics:
    def __init__(self):
        self.log_file = 'logs/faq_analytics.log'
    
    def track_search(self, query, results_count, user_ip=None):
        event = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'event_type': 'search',
            'query': query,
            'results_count': results_count,
            'user_ip': user_ip
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
    
    def track_faq_view(self, faq_id, user_ip=None):
        event = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'event_type': 'view',
            'faq_id': faq_id,
            'user_ip': user_ip
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')
```

## Maintenance and Updates

### Regular Maintenance Tasks

1. **Content Updates**: Update FAQ content in `backend/data/faqs.json`
2. **Search Analytics**: Review search logs to identify content gaps
3. **Performance Monitoring**: Monitor API response times and search performance
4. **User Feedback**: Collect feedback on FAQ usefulness and accuracy

### Content Management Workflow

```python
# backend/utils/faq_content_manager.py
import json
import os
from datetime import datetime

class FAQContentManager:
    def __init__(self):
        self.data_file = 'data/faqs.json'
        self.backup_dir = 'backups/'
    
    def backup_content(self):
        """Create backup before updates"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'{self.backup_dir}faqs_backup_{timestamp}.json'
        
        os.makedirs(self.backup_dir, exist_ok=True)
        
        with open(self.data_file, 'r') as src:
            with open(backup_file, 'w') as dst:
                dst.write(src.read())
        
        return backup_file
    
    def validate_content(self, content):
        """Validate FAQ content structure"""
        required_fields = {
            'categories': ['id', 'name', 'description'],
            'faqs': ['id', 'question', 'answer', 'categoryId', 'keywords']
        }
        
        for section, fields in required_fields.items():
            if section not in content:
                raise ValueError(f"Missing section: {section}")
            
            for item in content[section]:
                for field in fields:
                    if field not in item:
                        raise ValueError(f"Missing field {field} in {section}")
        
        return True
    
    def update_content(self, new_content):
        """Safely update FAQ content"""
        # Backup current content
        backup_file = self.backup_content()
        
        try:
            # Validate new content
            self.validate_content(new_content)
            
            # Write new content
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(new_content, f, indent=2, ensure_ascii=False)
            
            return {'success': True, 'backup': backup_file}
            
        except Exception as e:
            return {'success': False, 'error': str(e), 'backup': backup_file}
```

## Conclusion

This FAQ system integration provides a comprehensive, production-ready solution that **seamlessly incorporates FAQ as a core component** of the Catalog AI system. This is not an add-on or plugin, but rather a native feature that users will experience as an integral part of the catalog functionality.

### Core Integration Achievements:

- ✅ **Native System Component**: FAQ is implemented as a first-class citizen with the same architectural patterns as catalog features
- ✅ **Unified User Experience**: Consistent navigation, styling, and interaction patterns across catalog and FAQ sections  
- ✅ **Shared Data Integration**: FAQ system can cross-reference and link to companies and products from the catalog
- ✅ **Consistent API Design**: FAQ endpoints follow identical patterns to existing `/api/companies` and `/api/products` endpoints
- ✅ **Common Component Architecture**: FAQ components use the same React patterns, hooks, and state management as existing components
- ✅ **Integrated Styling System**: FAQ styles extend the existing CSS variable system and design language
- ✅ **Security & Performance**: Same standards applied across the entire system
- ✅ **Testing & Documentation**: Comprehensive coverage following established project patterns

### System Cohesion:

The FAQ system is designed to feel like it was **always part of the catalog application**. Users can seamlessly navigate between browsing products and finding answers, with consistent design language, shared navigation patterns, and potential cross-linking between FAQ content and specific companies or products.

**Key Result**: Users experience FAQ as a natural extension of the catalog browsing experience, not as a separate help system, creating a cohesive, integrated software solution that serves both discovery and support needs within a unified interface.
