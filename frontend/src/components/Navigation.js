import React from "react";
import { useNavigate, useLocation } from "react-router-dom";

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleSalesTrendsNavigation = () => {
    navigate('/sales-trends');
  };

  const handleCatalogNavigation = () => {
    navigate('/');
  };

  const isOnSalesTrends = location.pathname === '/sales-trends';
  const isOnCatalog = location.pathname === '/';

  return (
    <nav className="header-nav">
      <div className="nav-menu">
        <div className="nav-logo">
          <img 
            src="https://confirma.fi/wp-content/uploads/2023/05/Group-4072.svg" 
            alt="Confirma" 
            className="brand-logo"
          />
        </div>
        
        <div className="nav-links">
          <button 
            className={`nav-link ${isOnCatalog ? 'active' : ''}`}
            onClick={handleCatalogNavigation}
            title="Go to Catalog"
          >
            Catalog
          </button>
          <button 
            className={`nav-link ${isOnSalesTrends ? 'active' : ''}`}
            onClick={handleSalesTrendsNavigation}
            title="View Sales Trends Dashboard"
          >
            Sales Trends
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
