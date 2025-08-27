import React from "react";
import { Search, ArrowLeft, Building2 } from "lucide-react";

const Header = ({
  onSearch,
  onCompanySearch,
  searchTerm,
  companySearchTerm,
  selectedCompany,
  selectedProduct,
  onBackToCompanies,
  onBackToProducts,
}) => {
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
          aria-label={
            selectedProduct ? "Back to Products" : "Back to Companies"
          }
        >
          <ArrowLeft size={20} />
          {selectedProduct ? "Back to Products" : "Back to Companies"}
        </button>
      )}

      <div className="header-background">
        <div className="header-overlay">
          <div className="header-content">
            {!selectedCompany ? (
              <>
                <div className="header-brand">
                  <Building2 size={48} className="brand-icon" />
                  <h1>Confirma Catalog AI</h1>
                </div>
                <div className="search-container">
                  <input
                    type="text"
                    className="search-bar"
                    placeholder="Search companies by name or description..."
                    value={companySearchTerm}
                    onChange={handleCompanySearchChange}
                    aria-label="Search companies"
                  />
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
