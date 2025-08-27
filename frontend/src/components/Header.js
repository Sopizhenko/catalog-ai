import React from "react";
import { Search, ArrowLeft, MessageCircle, Package, Settings } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";

const Header = ({
  onSearch,
  onCompanySearch,
  searchTerm,
  companySearchTerm,
  selectedCompany,
  selectedProduct,
  onBackToCompanies,
  onBackToProducts,
  onFAQSearch, // Add FAQ search prop
  faqSearchTerm, // Add FAQ search term prop
}) => {
  const navigate = useNavigate();
  const location = useLocation();
  const handleSearchChange = (e) => {
    onSearch(e.target.value);
  };

  const handleCompanySearchChange = (e) => {
    onCompanySearch(e.target.value);
  };

  const handleFAQSearchChange = (e) => {
    if (onFAQSearch) {
      onFAQSearch(e.target.value);
    }
  };

  const isOnFAQPage = location.pathname === '/faq';
  const isOnHomePage = location.pathname === '/';

  const showMainNavigation = isOnHomePage || isOnFAQPage;
  
  const handleAdminClick = () => {
    window.open('http://localhost:5000/admin-dashboard', '_blank');
  };



  // Dynamic title based on current page
  const getPageTitle = () => {
    if (isOnFAQPage) {
      return "Confirma FAQ AI";
    }
    return "Confirma Catalog AI";
  };

  return (
    <header className="header">

      {/* Top Navigation Bar - Navigation buttons and Admin */}
      {showMainNavigation && (
        <div className="header-top-nav">
          <nav className="header-nav">
            <button 
              className={`nav-button ${!isOnFAQPage ? 'active' : ''}`}
              onClick={() => navigate('/')}
            >
              <Package size={16} />
              Catalog
            </button>
            <button 
              className={`nav-button ${isOnFAQPage ? 'active' : ''}`}
              onClick={() => navigate('/faq')}
            >
              <MessageCircle size={16} />
              FAQ
            </button>
          </nav>
          
          <button
            className="admin-button"
            onClick={handleAdminClick}
            aria-label="Open Admin Panel"
            title="Admin Panel"
          >
            <Settings size={20} />
            <span>Admin</span>
          </button>
        </div>
      )}


      {selectedCompany && (
        <button
          className="back-button icon-text-container"
          onClick={selectedProduct ? onBackToProducts : onBackToCompanies}
          aria-label={
            selectedProduct ? "Back to Products" : "Back to Companies"
          }
        >
          <ArrowLeft size={20} className="icon" />
          {selectedProduct ? "Back to Products" : "Back to Companies"}
        </button>
      )}

      <div className="header-background">
        <div className="header-overlay">
          <div className="header-content">
            {!selectedCompany ? (
              <>
                <div className="header-brand">
                  <div className="brand-letter">C</div>
                  <h1>{getPageTitle()}</h1>
                </div>
                
                {/* Search Container - Show appropriate search based on page */}
                <div className="search-container">
                  {isOnFAQPage ? (
                    <input
                      type="text"
                      className="search-bar"
                      placeholder="Search FAQs..."
                      value={faqSearchTerm || ''}
                      onChange={handleFAQSearchChange}
                      aria-label="Search FAQs"
                    />
                  ) : (
                    <input
                      type="text"
                      className="search-bar"
                      placeholder="Search companies by name or description..."
                      value={companySearchTerm}
                      onChange={handleCompanySearchChange}
                      aria-label="Search companies"
                    />
                  )}
                  <Search className="search-icon" size={20} />
                </div>
              </>
            ) : selectedProduct ? (
              <>
                <div className="header-brand">
                  <h1>{selectedProduct.name}</h1>
                </div>
                <div className="subtitle">
                  Product Details from {selectedCompany.company}
                </div>
              </>
            ) : (
              <>
                <div className="header-brand">
                  <h1>{selectedCompany.company}</h1>
                  <div className="company-contact-info">
                    <a 
                      href={`https://${selectedCompany.company.toLowerCase().replace(/\s+/g, '').replace(/[^a-z0-9]/g, '')}.com`} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="contact-link"
                    >
                      🌐 {selectedCompany.company.toLowerCase().replace(/\s+/g, '').replace(/[^a-z0-9]/g, '')}.com
                    </a>
                    <span className="contact-separator">•</span>
                    <a 
                      href={`mailto:info@${selectedCompany.company.toLowerCase().replace(/\s+/g, '').replace(/[^a-z0-9]/g, '')}.com`}
                      className="contact-link"
                    >
                      ✉️ info@{selectedCompany.company.toLowerCase().replace(/\s+/g, '').replace(/[^a-z0-9]/g, '')}.com
                    </a>
                    <span className="contact-separator">•</span>
                    <span className="contact-link">
                      📞 +1 (555) {Math.floor(Math.random() * 900 + 100)}-{Math.floor(Math.random() * 9000 + 1000)}
                    </span>
                  </div>
                </div>

                <div className="subtitle">
                  Browse Products from {selectedCompany.company}
                </div>
                <div className="search-container">
                  <input
                    type="text"
                    className="search-bar"
                    placeholder="Search products, features, or target audience..."
                    value={searchTerm}
                    onChange={handleSearchChange}
                    aria-label="Search products"
                  />
                  <Search className="search-icon" size={20} />
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;