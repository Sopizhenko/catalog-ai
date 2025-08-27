import React, { useState, useEffect } from 'react';
import { catalogAPI } from '../services/api';
import LoadingSpinner from './LoadingSpinner';

const ProductAnalysis = ({ product, onClose }) => {
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (product) {
      loadProductAnalysis();
    }
  }, [product]);

  const loadProductAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await catalogAPI.getProductAnalysis(product.id);
      setAnalysisData(response.data);
    } catch (err) {
      setError('Failed to load product analysis');
      console.error('Product analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="product-analysis-modal">
        <div className="modal-content">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="product-analysis-modal">
        <div className="modal-content">
          <div className="modal-header">
            <h2>Product Analysis</h2>
            <button onClick={onClose} className="close-button">×</button>
          </div>
          <div className="error-state">
            <h3>⚠️ Error Loading Analysis</h3>
            <p>{error}</p>
            <button onClick={loadProductAnalysis} className="retry-button">
              🔄 Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="product-analysis-modal">
      <div className="modal-content">
        <div className="modal-header">
          <div className="header-info">
            <h2>🔍 Product Competitive Analysis</h2>
            <p className="product-name">{product.name}</p>
            <span className="category-badge">{product.category}</span>
          </div>
          <button onClick={onClose} className="close-button">×</button>
        </div>

        <div className="analysis-body">
          {/* Competitive Comparison */}
          <div className="competitive-comparison">
            <h3>⚔️ Competitive Comparison</h3>
            <div className="comparison-grid">
              {analysisData?.competitive_comparison?.map((comparison, index) => (
                <div key={index} className="competitor-comparison">
                  <div className="competitor-header">
                    <h4>{comparison.competitor}</h4>
                    <div className="competitive-score">
                      <span className="score-label">Competitive Score</span>
                      <span className="score-value">{comparison.competitive_score}/10</span>
                    </div>
                  </div>
                  
                  <div className="feature-analysis">
                    <div className="feature-overlap">
                      <h5>🔄 Feature Overlap</h5>
                      <p>{comparison.feature_overlap} similar features</p>
                    </div>
                    
                    <div className="unique-features">
                      <h5>⭐ Our Unique Features</h5>
                      <div className="features-list">
                        {comparison.unique_features?.map((feature, featureIndex) => (
                          <span key={featureIndex} className="feature-tag unique">{feature}</span>
                        ))}
                      </div>
                    </div>
                    
                    <div className="missing-features">
                      <h5>❌ Features We're Missing</h5>
                      <div className="features-list">
                        {comparison.missing_features?.map((feature, featureIndex) => (
                          <span key={featureIndex} className="feature-tag missing">{feature}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Pricing Analysis */}
          <div className="pricing-analysis">
            <h3>💰 Pricing Analysis</h3>
            <div className="pricing-overview">
              <div className="current-pricing">
                <h4>📊 Current Position</h4>
                <div className="pricing-info">
                  <span className="price-value">
                    {product.pricing?.startingPrice} {product.pricing?.currency}
                  </span>
                  <span className="pricing-model">{product.pricing?.model}</span>
                  <span className="market-position">
                    {analysisData?.pricing_analysis?.market_position} Pricing
                  </span>
                </div>
              </div>
              
              <div className="pricing-recommendations">
                <h4>💡 Pricing Recommendations</h4>
                <div className="recommendations-list">
                  {analysisData?.pricing_analysis?.price_recommendations?.map((recommendation, index) => (
                    <div key={index} className="recommendation-item">
                      <span className="recommendation-icon">💡</span>
                      <span className="recommendation-text">{recommendation}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Differentiation Opportunities */}
          <div className="differentiation-opportunities">
            <h3>🚀 Differentiation Opportunities</h3>
            <div className="opportunities-grid">
              {analysisData?.differentiation_opportunities?.map((opportunity, index) => (
                <div key={index} className="opportunity-card">
                  <div className="opportunity-icon">🎯</div>
                  <div className="opportunity-content">
                    <h4>Opportunity #{index + 1}</h4>
                    <p>{opportunity}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Product Strengths & Weaknesses */}
          <div className="product-swot">
            <div className="product-strengths">
              <h3>💪 Product Strengths</h3>
              <div className="strengths-analysis">
                {/* Extract from product features and analysis */}
                <div className="strength-item">
                  <span className="strength-icon">✅</span>
                  <span>Comprehensive feature set with {product.features?.length} capabilities</span>
                </div>
                <div className="strength-item">
                  <span className="strength-icon">✅</span>
                  <span>Competitive pricing at {product.pricing?.startingPrice} {product.pricing?.currency}</span>
                </div>
                <div className="strength-item">
                  <span className="strength-icon">✅</span>
                  <span>Multi-platform support</span>
                </div>
                <div className="strength-item">
                  <span className="strength-icon">✅</span>
                  <span>Strong integration capabilities</span>
                </div>
              </div>
            </div>

            <div className="improvement-areas">
              <h3>🔧 Areas for Improvement</h3>
              <div className="improvement-analysis">
                <div className="improvement-item">
                  <span className="improvement-icon">🔧</span>
                  <span>Enhanced analytics and reporting features</span>
                </div>
                <div className="improvement-item">
                  <span className="improvement-icon">🔧</span>
                  <span>Improved user interface and user experience</span>
                </div>
                <div className="improvement-item">
                  <span className="improvement-icon">🔧</span>
                  <span>Advanced automation capabilities</span>
                </div>
                <div className="improvement-item">
                  <span className="improvement-icon">🔧</span>
                  <span>Enhanced mobile functionality</span>
                </div>
              </div>
            </div>
          </div>

          {/* Strategic Recommendations */}
          <div className="strategic-recommendations">
            <h3>🎯 Strategic Recommendations</h3>
            <div className="recommendations-summary">
              <div className="recommendation-category">
                <h4>📈 Product Development</h4>
                <ul>
                  <li>Focus on advanced analytics and AI-powered insights</li>
                  <li>Develop mobile-first features for better user adoption</li>
                  <li>Enhance integration capabilities with major platforms</li>
                </ul>
              </div>
              
              <div className="recommendation-category">
                <h4>💼 Market Positioning</h4>
                <ul>
                  <li>Emphasize unique features in marketing materials</li>
                  <li>Target underserved market segments</li>
                  <li>Develop industry-specific solutions</li>
                </ul>
              </div>
              
              <div className="recommendation-category">
                <h4>💰 Pricing Strategy</h4>
                <ul>
                  <li>Consider value-based pricing tiers</li>
                  <li>Offer flexible deployment options</li>
                  <li>Bundle complementary services for higher value</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button onClick={onClose} className="close-modal-button">
            Close Analysis
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductAnalysis;
