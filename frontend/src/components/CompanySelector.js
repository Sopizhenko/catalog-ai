import React from 'react';

const CompanySelector = ({ companies, selectedCompany, onCompanySelect }) => {
  return (
    <div className="company-selector">
      <h2>Select a Company</h2>
      <div className="companies-grid">
        {companies.map((company) => (
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
    </div>
  );
};

export default CompanySelector;
