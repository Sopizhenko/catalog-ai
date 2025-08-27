import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from "react-router-dom";
import { catalogAPI } from "./services/api";
import Header from "./components/Header";
import Navigation from "./components/Navigation";
import CompanySelector from "./components/CompanySelector";
import Filters from "./components/Filters";
import ProductGrid from "./components/ProductGrid";
import ProductDetail from "./components/ProductDetail";
import ProductModal from "./components/ProductModal";
import LoadingSpinner from "./components/LoadingSpinner";
import MarketAnalysis from "./components/MarketAnalysis";
import ProductAnalysis from "./components/ProductAnalysis";
import ProductComparison from "./components/ProductComparison";
import SalesTrendsDashboard from "./components/SalesTrendsDashboard";
import FAQContainer from "./components/FAQ/FAQContainer";
import { usePageTransition } from "./hooks/usePageTransition";
import './styles/faq.css';

// Main App Component with Router
function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

// Main App Content Component
function AppContent() {
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
  const [isTransitioning] = useState(false);

  // Navigation hook
  const navigate = useNavigate();
  const location = useLocation();

  // Load initial data
  useEffect(() => {
    loadInitialData();
  }, []);

  // Load products when company or filters change
  useEffect(() => {
    if (selectedCompany) {
      loadCompanyProducts();
    }
  }, [selectedCompany, searchTerm, selectedCategory]); // eslint-disable-line react-hooks/exhaustive-deps

  // Handle browser back/forward navigation
  useEffect(() => {
    const path = location.pathname;
    
    if (path === '/') {
      // Home page - show company selector
      setSelectedCompany(null);
      setSelectedProduct(null);
      setCurrentView('products');
    } else if (path.startsWith('/company/')) {
      // Company page - extract company name from URL
      const companyName = decodeURIComponent(path.replace('/company/', ''));
      const company = companies.find(c => c.company === companyName);
      if (company) {
        setSelectedCompany(company);
        setSelectedProduct(null);
        setCurrentView('products');
      }
    } else if (path.startsWith('/product/')) {
      // Product page - extract product ID from URL
      const productId = path.replace('/product/', '');
      if (selectedCompany) {
        const product = selectedCompany.products.find(p => p.id === productId);
        if (product) {
          setSelectedProduct(product);
        }
      }
          } else if (path.startsWith('/analysis/')) {
        // Analysis page - extract company name from URL
        const companyName = decodeURIComponent(path.replace('/analysis/', ''));
        const company = companies.find(c => c.company === companyName);
        if (company) {
          setSelectedCompany(company);
          setSelectedProduct(null);
          setCurrentView('market-analysis');
        }
      } else if (path === '/sales-trends') {
        // Sales trends dashboard
        setSelectedCompany(null);
        setSelectedProduct(null);
        setCurrentView('sales-trends');
      } else if (path === '/faq') {
        // FAQ page - clear company/product selection
        setSelectedCompany(null);
        setSelectedProduct(null);
        setCurrentView('faq');
      }
  }, [location.pathname, companies, selectedCompany]); // eslint-disable-line react-hooks/exhaustive-deps

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
    setSelectedCompany(company);
    setSelectedProduct(null);
    setCurrentView('products');
    setSearchTerm("");
    setSelectedCategory("all");
    navigate(`/company/${encodeURIComponent(company.company)}`);
  };

  const handleProductClick = (product) => {
    setSelectedProduct(product);
    navigate(`/product/${product.id}`);
  };

  const handleBackToCompanies = () => {
    setSelectedCompany(null);
    setSelectedProduct(null);
    setCurrentView('products');
    setSearchTerm("");
    setSelectedCategory("all");
    navigate('/');
  };

  const handleBackToProducts = () => {
    setSelectedProduct(null);
    if (selectedCompany) {
      navigate(`/company/${encodeURIComponent(selectedCompany.company)}`);
    } else {
      navigate('/');
    }
  };

  const handleViewChange = (view) => {
    setCurrentView(view);
    if (view === 'market-analysis' && selectedCompany) {
      navigate(`/analysis/${encodeURIComponent(selectedCompany.company)}`);
    } else if (view === 'products' && selectedCompany) {
      navigate(`/company/${encodeURIComponent(selectedCompany.company)}`);
    } else if (view === 'sales-trends') {
      navigate('/sales-trends');
    }
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

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedProduct(null);
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
        <div className="error-state">
          <h3>Error</h3>
          <p>{error}</p>
          <button onClick={loadInitialData} className="retry-button">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="App">
      <Navigation />
      
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
        <Routes>
          {/* Home/Company Selector Route */}
          <Route path="/" element={
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
          } />

          {/* Company Products Route */}
          <Route path="/company/:companyName" element={
            selectedCompany ? (
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
            ) : (
              <div className="loading">Loading company...</div>
            )
          } />

          {/* Product Detail Route */}
          <Route path="/product/:productId" element={
            selectedProduct ? (
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
              <div className="loading">Loading product...</div>
            )
          } />

          {/* Market Analysis Route */}
          <Route path="/analysis/:companyName" element={
            selectedCompany ? (
              <div
                className={`page-content ${
                  isTransitioning ? "page-exit" : "page-enter"
                }`}
              >
                <MarketAnalysis company={selectedCompany} />
              </div>
            ) : (
              <div className="loading">Loading analysis...</div>
            )
          } />

          {/* Sales Trends Dashboard Route */}
          <Route path="/sales-trends" element={
            <div
              className={`page-content ${
                isTransitioning ? "page-exit" : "page-enter"
              }`}
            >
              <SalesTrendsDashboard />
            </div>
          } />

          {/* FAQ Route */}
          <Route path="/faq" element={
            <div
              className={`page-content ${
                isTransitioning ? "page-exit" : "page-enter"
              }`}
            >
              <FAQContainer />
            </div>
          } />
        </Routes>
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
