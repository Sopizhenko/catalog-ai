import React from 'react';
import { Search, ArrowLeft } from 'lucide-react';

const Header = ({ onSearch, onCompanySearch, searchTerm, companySearchTerm, selectedCompany, selectedProduct, onBackToCompanies, onBackToProducts }) => {
  const handleSearchChange = (e) => {
    onSearch(e.target.value);
  };

  const handleCompanySearchChange = (e) => {
    onCompanySearch(e.target.value);
  };

  return (
    <header className="header">
      {selectedCompany && (
        <button 
          className="back-button" 
          onClick={selectedProduct ? onBackToProducts : onBackToCompanies}
        >
          <ArrowLeft size={20} />
          {selectedProduct ? 'Back to Products' : 'Back to Companies'}
        </button>
      )}
      
      <div className="header-content">
        {!selectedCompany ? (
          <>
            <h1>Catalog AI</h1>
            <div className="subtitle">Select a Company to Browse Products</div>
            <div className="search-container">
              <input
                type="text"
                className="search-bar"
                placeholder="Search companies by name or description..."
                value={companySearchTerm}
                onChange={handleCompanySearchChange}
              />
              <Search className="search-icon" size={20} />
            </div>
          </>
        ) : selectedProduct ? (
          <>
            <h1>{selectedProduct.name}</h1>
            <div className="subtitle">Product Details from {selectedCompany.company}</div>
          </>
        ) : (
          <>
            <h1>{selectedCompany.company}</h1>
            <div className="subtitle">Browse Products from {selectedCompany.company}</div>
            <div className="search-container">
              <input
                type="text"
                className="search-bar"
                placeholder="Search products, features, or target audience..."
                value={searchTerm}
                onChange={handleSearchChange}
              />
              <Search className="search-icon" size={20} />
            </div>
          </>
        )}
      </div>
    </header>
  );
};

export default Header;
