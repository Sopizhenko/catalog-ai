import React, { useState, useEffect } from 'react';
import { catalogAPI } from './services/api';
import Header from './components/Header';
import Filters from './components/Filters';
import ProductGrid from './components/ProductGrid';
import ProductModal from './components/ProductModal';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [products, setProducts] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [categories, setCategories] = useState([]);
  const [audiences, setAudiences] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedAudience, setSelectedAudience] = useState('all');
  
  // Modal state
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Load initial data
  useEffect(() => {
    loadInitialData();
  }, []);

  // Load products when filters change
  useEffect(() => {
    loadProducts();
  }, [searchTerm, selectedCategory, selectedAudience]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [companiesRes, categoriesRes, audiencesRes] = await Promise.all([
        catalogAPI.getCompanies(),
        catalogAPI.getCategories(),
        catalogAPI.getAudiences()
      ]);
      
      setCompanies(companiesRes.data.companies || []);
      setCategories(categoriesRes.data || []);
      setAudiences(audiencesRes.data || []);
    } catch (err) {
      setError('Failed to load initial data');
      console.error('Error loading initial data:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadProducts = async () => {
    try {
      const filters = {
        search: searchTerm,
        category: selectedCategory !== 'all' ? selectedCategory : '',
        audience: selectedAudience !== 'all' ? selectedAudience : ''
      };
      
      const response = await catalogAPI.getProducts(filters);
      setProducts(response.data.products || []);
    } catch (err) {
      setError('Failed to load products');
      console.error('Error loading products:', err);
    }
  };

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const handleCategoryFilter = (category) => {
    setSelectedCategory(category);
  };

  const handleAudienceFilter = (audience) => {
    setSelectedAudience(audience);
  };

  const handleProductClick = (product) => {
    setSelectedProduct(product);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedProduct(null);
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="container">
        <div className="no-results">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <div className="container">
        <Header 
          onSearch={handleSearch}
          searchTerm={searchTerm}
        />
        
        <Filters
          categories={categories}
          audiences={audiences}
          selectedCategory={selectedCategory}
          selectedAudience={selectedAudience}
          onCategoryFilter={handleCategoryFilter}
          onAudienceFilter={handleAudienceFilter}
        />
        
        <ProductGrid
          products={products}
          onProductClick={handleProductClick}
        />
      </div>
      
      {isModalOpen && selectedProduct && (
        <ProductModal
          product={selectedProduct}
          onClose={handleCloseModal}
        />
      )}
    </div>
  );
}

export default App;
