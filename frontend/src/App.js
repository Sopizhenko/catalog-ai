import React, { useState, useEffect } from "react";
import { catalogAPI } from "./services/api";
import Header from "./components/Header";
import CompanySelector from "./components/CompanySelector";
import Filters from "./components/Filters";
import ProductGrid from "./components/ProductGrid";
import ProductDetail from "./components/ProductDetail";
import ProductModal from "./components/ProductModal";
import LoadingSpinner from "./components/LoadingSpinner";
import MarketAnalysis from "./components/MarketAnalysis";
import ProductAnalysis from "./components/ProductAnalysis";
import ProductComparison from "./components/ProductComparison";
import { usePageTransition } from "./hooks/usePageTransition";

function App() {
  const [products, setProducts] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filter states
  const [searchTerm, setSearchTerm] = useState("");
  const [companySearchTerm, setCompanySearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");

  // Modal state
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Analysis views state
  const [currentView, setCurrentView] = useState('products'); // 'products', 'market-analysis'
  const [showProductAnalysis, setShowProductAnalysis] = useState(false);
  const [productForAnalysis, setProductForAnalysis] = useState(null);
  const [showProductComparison, setShowProductComparison] = useState(false);

  // Page transition state
  const [isTransitioning, setIsTransitioning] = useState(false);

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
      setError("Failed to load companies");
      console.error("Error loading companies:", err);
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
        filteredProducts = filteredProducts.filter(
          (product) =>
            product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            product.description
              .toLowerCase()
              .includes(searchTerm.toLowerCase()) ||
            product.features.some((feature) =>
              feature.toLowerCase().includes(searchTerm.toLowerCase())
            ) ||
            product.targetAudience.some((audience) =>
              audience.toLowerCase().includes(searchTerm.toLowerCase())
            )
        );
      }

      // Apply category filter
      if (selectedCategory !== "all") {
        filteredProducts = filteredProducts.filter((product) =>
          product.category
            .toLowerCase()
            .includes(selectedCategory.toLowerCase())
        );
      }

      setProducts(filteredProducts);
    } catch (err) {
      setError("Failed to load products");
      console.error("Error loading products:", err);
    }
  };

  const handleCompanySelect = (company) => {
    setIsTransitioning(true);
    setTimeout(() => {
      setSelectedCompany(company);
      setSearchTerm("");
      setSelectedCategory("all");
      setIsTransitioning(false);
    }, 250);
  };

  const handleBackToCompanies = () => {
    setIsTransitioning(true);
    setTimeout(() => {
      setSelectedCompany(null);
      setSelectedProduct(null);
      setProducts([]);
      setSearchTerm("");
      setCompanySearchTerm("");
      setSelectedCategory("all");
      setCurrentView('products');
      setShowProductAnalysis(false);
      setProductForAnalysis(null);
      setShowProductComparison(false);
      setIsTransitioning(false);
    }, 250);
  };

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const handleCompanySearch = (term) => {
    setCompanySearchTerm(term);
  };

  const handleCategoryFilter = (category) => {
    setSelectedCategory(category);
  };

  const handleProductClick = (product) => {
    setIsTransitioning(true);
    setTimeout(() => {
      setSelectedProduct(product);
      setIsTransitioning(false);
    }, 250);
  };

  const handleBackToProducts = () => {
    setIsTransitioning(true);
    setTimeout(() => {
      setSelectedProduct(null);
      setIsTransitioning(false);
    }, 250);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedProduct(null);
  };

  // New analysis handlers
  const handleViewChange = (view) => {
    setCurrentView(view);
    if (view === 'products') {
      setSelectedProduct(null);
    }
  };

  const handleProductAnalysis = (product) => {
    setProductForAnalysis(product);
    setShowProductAnalysis(true);
  };

  const handleCloseProductAnalysis = () => {
    setShowProductAnalysis(false);
    setProductForAnalysis(null);
  };

  const handleOpenProductComparison = () => {
    setShowProductComparison(true);
  };

  const handleCloseProductComparison = () => {
    setShowProductComparison(false);
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="container">
        <div className="no-results animate-fade-in">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <Header
        onSearch={handleSearch}
        onCompanySearch={handleCompanySearch}
        searchTerm={searchTerm}
        companySearchTerm={companySearchTerm}
        selectedCompany={selectedCompany}
        selectedProduct={selectedProduct}
        onBackToCompanies={handleBackToCompanies}
        onBackToProducts={handleBackToProducts}
      />

      <div
        className={`container ${isTransitioning ? "page-transitioning" : ""}`}
      >
        {!selectedCompany ? (
          <div
            className={`page-content ${
              isTransitioning ? "page-exit" : "page-enter"
            }`}
          >
            <CompanySelector
              companies={companies}
              companySearchTerm={companySearchTerm}
              selectedCompany={selectedCompany}
              onCompanySelect={handleCompanySelect}
            />
          </div>
        ) : selectedProduct ? (
          <div
            className={`page-content ${
              isTransitioning ? "page-exit" : "page-enter"
            }`}
          >
            <ProductDetail
              product={selectedProduct}
              onBackToProducts={handleBackToProducts}
            />
          </div>
        ) : (
          <div
            className={`page-content ${
              isTransitioning ? "page-exit" : "page-enter"
            }`}
          >
            {/* Company Analysis Navigation */}
            <div className="company-analysis-nav">
              <h2>📊 {selectedCompany.company} - Sales Intelligence</h2>
              <div className="analysis-nav-tabs">
                <button 
                  className={`nav-tab ${currentView === 'products' ? 'active' : ''}`}
                  onClick={() => handleViewChange('products')}
                >
                  📦 Products ({selectedCompany.products?.length || 0})
                </button>
                <button 
                  className={`nav-tab ${currentView === 'market-analysis' ? 'active' : ''}`}
                  onClick={() => handleViewChange('market-analysis')}
                >
                  📊 Market Analysis
                </button>
                <button 
                  className="nav-tab comparison-btn"
                  onClick={handleOpenProductComparison}
                >
                  🔄 Product Comparison
                </button>
              </div>
            </div>

            {/* Conditional Content Based on Current View */}
            {currentView === 'products' ? (
              <>
                <Filters
                  categories={Array.from(
                    new Set(selectedCompany.products.map((p) => p.category))
                  )}
                  selectedCategory={selectedCategory}
                  onCategoryFilter={handleCategoryFilter}
                />

                <ProductGrid
                  products={products}
                  onProductClick={handleProductClick}
                  onProductAnalysis={handleProductAnalysis}
                  showAnalysisButton={true}
                />
              </>
            ) : currentView === 'market-analysis' ? (
              <MarketAnalysis company={selectedCompany} />
            ) : null}
          </div>
        )}
      </div>

      {isModalOpen && selectedProduct && (
        <ProductModal product={selectedProduct} onClose={handleCloseModal} />
      )}

      {/* Product Analysis Modal */}
      {showProductAnalysis && productForAnalysis && (
        <ProductAnalysis 
          product={productForAnalysis} 
          onClose={handleCloseProductAnalysis} 
        />
      )}

      {/* Product Comparison Modal */}
      {showProductComparison && (
        <ProductComparison 
          onClose={handleCloseProductComparison} 
        />
      )}
    </div>
  );
}

export default App;
