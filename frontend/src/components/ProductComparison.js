import React, { useState, useEffect } from 'react';
import { catalogAPI } from '../services/api';
import LoadingSpinner from './LoadingSpinner';

const ProductComparison = ({ onClose }) => {
  const [companies, setCompanies] = useState([]);
  const [selectedProducts, setSelectedProducts] = useState([]);
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [step, setStep] = useState('selection'); // 'selection' or 'results'

  useEffect(() => {
    loadCompanies();
  }, []);

  const loadCompanies = async () => {
    try {
      const response = await catalogAPI.getCompanies();
      setCompanies(response.data.companies || []);
    } catch (err) {
      setError('Failed to load companies');
      console.error('Error loading companies:', err);
    }
  };

  const handleProductToggle = (product, company) => {
    const productWithCompany = {
      ...product,
      company_name: company.company,
      parent_company: company.parentCompany
    };

    setSelectedProducts(prev => {
      const isSelected = prev.some(p => p.id === product.id);
      if (isSelected) {
        return prev.filter(p => p.id !== product.id);
      } else {
        return [...prev, productWithCompany];
      }
    });
  };

  const runComparison = async () => {
    if (selectedProducts.length < 2) {
      setError('Please select at least 2 products for comparison');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const productIds = selectedProducts.map(p => p.id);
      const response = await catalogAPI.compareProducts(productIds);
      setComparisonData(response.data);
      setStep('results');
    } catch (err) {
      setError('Failed to generate comparison');
      console.error('Comparison error:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetComparison = () => {
    setStep('selection');
    setSelectedProducts([]);
    setComparisonData(null);
    setError(null);
  };

  if (loading) {
    return (
      <div className="product-comparison-modal">
        <div className="modal-content">
          <LoadingSpinner />
          <p>Analyzing product synergies...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="product-comparison-modal">
      <div className="modal-content">
        <div className="modal-header">
          <h2>🔄 Product Comparison & Cross-selling Analysis</h2>
          <button onClick={onClose} className="close-button">×</button>
        </div>

        {step === 'selection' ? (
          <ProductSelectionStep 
            companies={companies}
            selectedProducts={selectedProducts}
            onProductToggle={handleProductToggle}
            onRunComparison={runComparison}
            error={error}
          />
        ) : (
          <ComparisonResults 
            comparisonData={comparisonData}
            selectedProducts={selectedProducts}
            onReset={resetComparison}
          />
        )}
      </div>
    </div>
  );
};

const ProductSelectionStep = ({ companies, selectedProducts, onProductToggle, onRunComparison, error }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCompany, setSelectedCompany] = useState('all');

  const filteredCompanies = companies.filter(company => {
    const matchesSearch = company.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         company.products.some(p => p.name.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCompany = selectedCompany === 'all' || company.company === selectedCompany;
    return matchesSearch && matchesCompany;
  });

  return (
    <div className="product-selection">
      <div className="selection-header">
        <p>Select products to compare for cross-selling opportunities</p>
        <div className="selection-controls">
          <input
            type="text"
            placeholder="Search products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          <select 
            value={selectedCompany} 
            onChange={(e) => setSelectedCompany(e.target.value)}
            className="company-filter"
          >
            <option value="all">All Companies</option>
            {companies.map(company => (
              <option key={company.company} value={company.company}>
                {company.company}
              </option>
            ))}
          </select>
        </div>
      </div>

      {error && (
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          {error}
        </div>
      )}

      <div className="selected-summary">
        <h3>Selected Products ({selectedProducts.length})</h3>
        {selectedProducts.length > 0 && (
          <div className="selected-products">
            {selectedProducts.map(product => (
              <span key={product.id} className="selected-product-tag">
                {product.name} ({product.company_name})
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="products-table-container">
        <table className="products-comparison-table">
          <thead>
            <tr>
              <th>Product Name</th>
              <th>Company</th>
              <th>Category</th>
              <th>Description</th>
              <th>Starting Price</th>
              <th>Features Count</th>
              <th>Select</th>
            </tr>
          </thead>
          <tbody>
            {filteredCompanies.map(company => 
              company.products.map(product => {
                const isSelected = selectedProducts.some(p => p.id === product.id);
                return (
                  <tr 
                    key={product.id} 
                    className={`product-row ${isSelected ? 'selected' : ''}`}
                  >
                    <td className="product-name">
                      <strong>{product.name}</strong>
                    </td>
                    <td className="company-name">
                      <div className="company-info">
                        <span className="company">{company.company}</span>
                        {company.parentCompany && (
                          <span className="parent-company">({company.parentCompany})</span>
                        )}
                      </div>
                    </td>
                    <td className="category">
                      <span className="category-badge">{product.category}</span>
                    </td>
                    <td className="description">
                      <p>{product.description}</p>
                    </td>
                    <td className="pricing">
                      <span className="price">
                        {product.pricing?.startingPrice ? 
                          `${product.pricing.startingPrice} ${product.pricing.currency || ''}` : 
                          'Contact for pricing'
                        }
                      </span>
                    </td>
                    <td className="features">
                      <span className="features-count">
                        {product.features?.length || 0} features
                      </span>
                    </td>
                    <td className="select-column">
                      <input
                        type="checkbox"
                        checked={isSelected}
                        onChange={() => onProductToggle(product, company)}
                        className="product-checkbox"
                      />
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
        
        {filteredCompanies.length === 0 && (
          <div className="no-products">
            <p>No products found matching your search criteria.</p>
          </div>
        )}
      </div>

      <div className="selection-footer">
        <button 
          onClick={onRunComparison}
          disabled={selectedProducts.length < 2}
          className="run-comparison-button"
        >
          🔍 Analyze Cross-selling Potential ({selectedProducts.length} products)
        </button>
      </div>
    </div>
  );
};

const ComparisonResults = ({ comparisonData, selectedProducts, onReset }) => {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="comparison-results">
      <div className="results-header">
        <h3>📊 Cross-selling Analysis Results</h3>
        <button onClick={onReset} className="new-comparison-button">
          🔄 New Comparison
        </button>
      </div>

      {/* Results Navigation */}
      <div className="results-nav">
        <button 
          className={`nav-tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📋 Overview
        </button>
        <button 
          className={`nav-tab ${activeTab === 'features' ? 'active' : ''}`}
          onClick={() => setActiveTab('features')}
        >
          ⚙️ Feature Matrix
        </button>
        <button 
          className={`nav-tab ${activeTab === 'pricing' ? 'active' : ''}`}
          onClick={() => setActiveTab('pricing')}
        >
          💰 Pricing
        </button>
        <button 
          className={`nav-tab ${activeTab === 'synergies' ? 'active' : ''}`}
          onClick={() => setActiveTab('synergies')}
        >
          🎯 Synergies
        </button>
      </div>

      {/* Tab Content */}
      <div className="results-content">
        {activeTab === 'overview' && (
          <OverviewTab comparisonData={comparisonData} />
        )}
        {activeTab === 'features' && (
          <FeatureMatrixTab featureMatrix={comparisonData?.feature_matrix} products={selectedProducts} />
        )}
        {activeTab === 'pricing' && (
          <PricingTab pricingComparison={comparisonData?.pricing_comparison} />
        )}
        {activeTab === 'synergies' && (
          <SynergiesTab 
            crossSellingPotential={comparisonData?.cross_selling_potential}
            audienceOverlap={comparisonData?.target_audience_overlap}
          />
        )}
      </div>
    </div>
  );
};

const OverviewTab = ({ comparisonData }) => (
  <div className="overview-tab">
    <div className="products-overview">
      <h4>🎯 Selected Products</h4>
      <div className="products-summary">
        {comparisonData?.products?.map(product => (
          <div key={product.id} className="product-summary">
            <h5>{product.name}</h5>
            <p className="company">{product.company_name}</p>
            <span className="category">{product.category}</span>
          </div>
        ))}
      </div>
    </div>

    <div className="recommendations-summary">
      <h4>💡 Key Recommendations</h4>
      <div className="recommendations-list">
        {comparisonData?.recommendation_summary?.map((recommendation, index) => (
          <div key={index} className="recommendation-item">
            <span className="recommendation-icon">💡</span>
            <span className="recommendation-text">{recommendation}</span>
          </div>
        ))}
      </div>
    </div>
  </div>
);

const FeatureMatrixTab = ({ featureMatrix, products }) => {
  if (!featureMatrix || !products || featureMatrix.length === 0 || products.length === 0) {
    return (
      <div className="feature-matrix-tab">
        <h4>⚙️ Feature Comparison Matrix</h4>
        <div className="no-feature-data">
          <p>No feature comparison data available for the selected products.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="feature-matrix-tab">
      <h4>⚙️ Feature Comparison Matrix</h4>
      <div className="feature-matrix">
        <div className="matrix-table" style={{ gridTemplateColumns: `200px repeat(${products.length}, 1fr)` }}>
          <div className="matrix-header">
            <div className="feature-column-header">Feature</div>
            {products.map((product, index) => (
              <div key={product.id} className={`product-column-header product-column-${index}`}>
                <div className="product-name">{product.name}</div>
                <div className="product-company">{product.company_name}</div>
              </div>
            ))}
          </div>
          {featureMatrix.map((featureRow, rowIndex) => (
            <div key={rowIndex} className="matrix-row">
              <div className="feature-name">{featureRow.feature}</div>
              {products.map((product, colIndex) => (
                <div key={product.id} className={`feature-cell product-column-${colIndex}`}>
                  {featureRow[product.id] ? (
                    <div className="feature-available">
                      <span className="feature-icon">✅</span>
                    </div>
                  ) : (
                    <div className="feature-unavailable">
                      <span className="feature-icon">❌</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const PricingTab = ({ pricingComparison }) => (
  <div className="pricing-tab">
    <h4>💰 Pricing Comparison</h4>
    <div className="pricing-grid">
      {pricingComparison?.map(pricing => (
        <div key={pricing.product_id} className="pricing-card">
          <h5>{pricing.product_name}</h5>
          <div className="pricing-details">
            <span className="price-value">
              {pricing.starting_price} {pricing.currency}
            </span>
            <span className="pricing-model">{pricing.pricing_model}</span>
          </div>
        </div>
      ))}
    </div>
  </div>
);

const SynergiesTab = ({ crossSellingPotential, audienceOverlap }) => (
  <div className="synergies-tab">
    <div className="cross-selling-potential">
      <h4>🎯 Cross-selling Potential</h4>
      <div className="potential-grid">
        {crossSellingPotential?.map((potential, index) => (
          <div key={index} className="potential-card">
            <div className="potential-header">
              <h5>{potential.product1} + {potential.product2}</h5>
              <span className={`potential-level ${potential.potential_level?.toLowerCase()}`}>
                {potential.potential_level}
              </span>
            </div>
            <div className="synergy-score">
              <span className="score-label">Synergy Score:</span>
              <span className="score-value">{potential.synergy_score}/10</span>
            </div>
          </div>
        ))}
      </div>
    </div>

    <div className="audience-overlap">
      <h4>👥 Target Audience Overlap</h4>
      <div className="overlap-grid">
        {audienceOverlap?.map((overlap, index) => (
          <div key={index} className="overlap-card">
            <div className="overlap-header">
              <h5>{overlap.product1} & {overlap.product2}</h5>
              <span className="overlap-percentage">{overlap.overlap_percentage}% overlap</span>
            </div>
            {overlap.common_audiences?.length > 0 && (
              <div className="common-audiences">
                <span className="audiences-label">Common audiences:</span>
                <div className="audiences-list">
                  {overlap.common_audiences.map((audience, audienceIndex) => (
                    <span key={audienceIndex} className="audience-tag">{audience}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  </div>
);

export default ProductComparison;
