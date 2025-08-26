import React from 'react';
import { Search, ArrowLeft } from 'lucide-react';

const Header = ({ onSearch, searchTerm, selectedCompany, onBackToCompanies }) => {
  const handleSearchChange = (e) => {
    onSearch(e.target.value);
  };

  return (
    <header className="header">
      <div>
        {!selectedCompany ? (
          <>
            <h1>Catalog AI</h1>
            <div className="subtitle">Select a Company to Browse Products</div>
          </>
        ) : (
          <>
            <div className="company-header-row">
              <button className="back-button" onClick={onBackToCompanies}>
                <ArrowLeft size={20} />
                Back to Companies
              </button>
              <h1>{selectedCompany.company}</h1>
            </div>
            <div className="subtitle">Browse Products from {selectedCompany.company}</div>
          </>
        )}
        
        {selectedCompany && (
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
        )}
      </div>
    </header>
  );
};

export default Header;
