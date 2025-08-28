import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Settings, MessageCircle } from "lucide-react";

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleSalesTrendsNavigation = () => {
    navigate('/sales-trends');
  };

  const handleCatalogNavigation = () => {
    navigate('/');
  };

  const handleFAQNavigation = () => {
    navigate('/faq');
  };

  const handleAdminClick = () => {
    window.open('http://localhost:5000/admin-dashboard', '_blank');
  };

  const handleLogoClick = () => {
    navigate('/');
  };

  const isOnSalesTrends = location.pathname === '/sales-trends';
  const isOnCatalog = location.pathname === '/' || location.pathname.startsWith('/company/') || location.pathname.startsWith('/product/');
  const isOnFAQ = location.pathname === '/faq';

  return (
    <nav className="header-nav">
      <div className="nav-menu">
        <div className="nav-logo">
          <button 
            className="logo-button" 
            onClick={handleLogoClick}
            title="Go to Home"
            aria-label="Go to Home"
          >
            <span className="logo-text-main">Confirma</span>
          </button>
        </div>
        
        <div className="nav-links">
          <button
            className={`nav-link ${isOnCatalog ? 'active' : ''}`}
            onClick={handleCatalogNavigation}
          >
            Catalog
          </button>
          <button
            className={`nav-link ${isOnSalesTrends ? 'active' : ''}`}
            onClick={handleSalesTrendsNavigation}
          >
            Sales Trends
          </button>
          <button
            className={`nav-link ${isOnFAQ ? 'active' : ''}`}
            onClick={handleFAQNavigation}
          >
            FAQ
          </button>
          <button
            className="admin-nav-button"
            onClick={handleAdminClick}
            aria-label="Open Admin Panel"
            title="Admin Panel"
          >
            <Settings size={16} />
            Admin
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
