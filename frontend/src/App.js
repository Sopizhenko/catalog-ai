import React, { useState, useEffect } from 'react';
import { catalogAPI } from './services/api';
import Header from './components/Header';
import CompanySelector from './components/CompanySelector';
import Filters from './components/Filters';
import ProductGrid from './components/ProductGrid';
import ProductModal from './components/ProductModal';
import LoadingSpinner from './components/LoadingSpinner';

function App() {
  const [products, setProducts] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  
  // Modal state
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Load initial data
  useEffect(() => {
    loadInitialData();
  }, []);

  // Load products when company or filters change
  useEffect(() => {
    if (selectedCompany) {
      loadCompanyProducts();
    }
  }, [selectedCompany, searchTerm, selectedCategory]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const companiesRes = await catalogAPI.getCompanies();
      setCompanies(companiesRes.data.companies || []);
    } catch (err) {
      setError('Failed to load companies');
      console.error('Error loading companies:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadCompanyProducts = async () => {
    if (!selectedCompany) return;
    
    try {
      let filteredProducts = selectedCompany.products || [];
      
      // Apply search filter
      if (searchTerm) {
        filteredProducts = filteredProducts.filter(product => 
          product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          product.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
          product.features.some(feature => feature.toLowerCase().includes(searchTerm.toLowerCase())) ||
          product.targetAudience.some(audience => audience.toLowerCase().includes(searchTerm.toLowerCase()))
        );
      }
      
      // Apply category filter
      if (selectedCategory !== 'all') {
        filteredProducts = filteredProducts.filter(product => 
          product.category.toLowerCase().includes(selectedCategory.toLowerCase())
        );
      }
      
      setProducts(filteredProducts);
    } catch (err) {
      setError('Failed to load products');
      console.error('Error loading products:', err);
    }
  };

  const handleCompanySelect = (company) => {
    setSelectedCompany(company);
    setSearchTerm('');
    setSelectedCategory('all');
  };

  const handleBackToCompanies = () => {
    setSelectedCompany(null);
    setProducts([]);
    setSearchTerm('');
    setSelectedCategory('all');
  };

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const handleCategoryFilter = (category) => {
    setSelectedCategory(category);
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
          selectedCompany={selectedCompany}
          onBackToCompanies={handleBackToCompanies}
        />
        
        {!selectedCompany ? (
          <CompanySelector
            companies={companies}
            selectedCompany={selectedCompany}
            onCompanySelect={handleCompanySelect}
          />
        ) : (
          <>
            <Filters
              categories={Array.from(new Set(selectedCompany.products.map(p => p.category)))}
              selectedCategory={selectedCategory}
              onCategoryFilter={handleCategoryFilter}
            />
            
            <ProductGrid
              products={products}
              onProductClick={handleProductClick}
            />
          </>
        )}
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
