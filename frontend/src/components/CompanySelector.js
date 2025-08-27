import React from 'react';

const CompanySelector = ({ companies, companySearchTerm, selectedCompany, onCompanySelect }) => {
  // Filter companies based on search term
  const filteredCompanies = companies.filter(company => {
    if (!companySearchTerm) return true;
    
    const searchLower = companySearchTerm.toLowerCase();
    return (
      company.company.toLowerCase().includes(searchLower) ||
      company.description.toLowerCase().includes(searchLower) ||
      (company.parentCompany && company.parentCompany.toLowerCase().includes(searchLower)) ||
      (company.industry && company.industry.toLowerCase().includes(searchLower))
    );
  });

  return (
    <div className="company-selector">
      <h2>Select a Company</h2>
      {companySearchTerm && (
        <div className="search-results-info">
          {filteredCompanies.length} company{filteredCompanies.length !== 1 ? 'ies' : ''} found
        </div>
      )}
      {filteredCompanies.length > 0 ? (
        <div className="companies-grid">
          {filteredCompanies.map((company) => (
            <div
              key={company.company}
              className={`company-card ${selectedCompany?.company === company.company ? 'selected' : ''}`}
              onClick={() => onCompanySelect(company)}
            >
              <div className="company-header">
                <h3>{company.company}</h3>
                {company.parentCompany && (
                  <span className="parent-company">{company.parentCompany}</span>
                )}
              </div>
              <p className="company-description">{company.description}</p>
              <div className="company-stats">
                <span className="product-count">
                  {company.products?.length || 0} Products
                </span>
                {company.industry && (
                  <span className="industry">{company.industry}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-results">
          <h3>No companies found</h3>
          <p>Try adjusting your search terms or browse all companies.</p>
        </div>
      )}
    </div>
  );
};

export default CompanySelector;
