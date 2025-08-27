import React, { useState, useEffect, useCallback } from 'react';
import { MessageCircle } from 'lucide-react';
import { catalogAPI } from '../../services/api';
import FAQFilters from './FAQFilters';
import FAQItem from './FAQItem';
import FAQModal from './FAQModal';
import LoadingSpinner from '../LoadingSpinner';

const FAQContainer = ({ searchTerm = '' }) => {
  const [faqs, setFaqs] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState(searchTerm);
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

  // Sync searchQuery with searchTerm prop and trigger search
  useEffect(() => {
    if (searchTerm !== searchQuery) {
      setSearchQuery(searchTerm);
      // Trigger the search when searchTerm changes
      handleSearch(searchTerm);
    }
  }, [searchTerm, searchQuery]);

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
      {/* FAQ Filters */}
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
