import React from "react";
import { Building2, Package, Briefcase, Search } from "lucide-react";
import { useScrollAnimation } from "../hooks/useScrollAnimation";

const CompanySelector = ({
  companies,
  companySearchTerm,
  selectedCompany,
  onCompanySelect,
}) => {
  const [headerRef, isHeaderVisible] = useScrollAnimation({
    threshold: 0.3,
    delay: 200,
  });

  // Filter companies based on search term
  const filteredCompanies = companies.filter((company) => {
    if (!companySearchTerm) return true;

    const searchLower = companySearchTerm.toLowerCase();
    return (
      company.company.toLowerCase().includes(searchLower) ||
      company.description.toLowerCase().includes(searchLower) ||
      (company.parentCompany &&
        company.parentCompany.toLowerCase().includes(searchLower)) ||
      (company.industry && company.industry.toLowerCase().includes(searchLower))
    );
  });

  return (
    <div className="company-selector">
      <div
        ref={headerRef}
        className={`selector-header ${
          isHeaderVisible ? "animate-slide-up" : "animate-slide-down"
        }`}
      >
        <Building2 size={32} className="selector-icon" />
        <h2>Select a Company</h2>
        <p className="selector-subtitle">
          Choose from our portfolio of innovative software companies
        </p>
      </div>

      {companySearchTerm && (
        <div className="search-results-info animate-fade-in">
          <Search size={16} />
          {filteredCompanies.length} company
          {filteredCompanies.length !== 1 ? "ies" : ""} found
        </div>
      )}

      {filteredCompanies.length > 0 ? (
        <div className="companies-grid">
          {filteredCompanies.map((company, index) => (
            <CompanyCard
              key={company.company}
              company={company}
              selectedCompany={selectedCompany}
              onCompanySelect={onCompanySelect}
              index={index}
            />
          ))}
        </div>
      ) : (
        <div className="no-results animate-fade-in">
          <Search size={48} className="no-results-icon" />
          <h3>No companies found</h3>
          <p>Try adjusting your search terms or browse all companies.</p>
        </div>
      )}
    </div>
  );
};

const CompanyCard = ({ company, selectedCompany, onCompanySelect, index }) => {
  const [cardRef, isVisible] = useScrollAnimation({
    threshold: 0.1,
    delay: index * 40, // Stagger animation by 40ms per card
    triggerOnce: true,
  });

  return (
    <div
      ref={cardRef}
      className={`company-card ${
        isVisible ? "animate-card-enter" : "animate-card-exit"
      } ${selectedCompany?.company === company.company ? "selected" : ""}`}
      onClick={() => onCompanySelect(company)}
    >
      <div className="company-header">
        <div className="company-title-section">
          <h3>{company.company}</h3>
          {company.parentCompany && (
            <span className="parent-company">{company.parentCompany}</span>
          )}
        </div>
        <div className="company-icon">
          <Building2 size={24} />
        </div>
      </div>
      <p className="company-description">{company.description}</p>
      <div className="company-stats">
        <div className="stat-item">
          <Package size={16} className="stat-icon" />
          <span>{company.products?.length || 0} Products</span>
        </div>
        {company.industry && (
          <div className="stat-item">
            <Briefcase size={16} className="stat-icon" />
            <span>{company.industry}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default CompanySelector;
