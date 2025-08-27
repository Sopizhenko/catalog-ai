import React, { useState, useEffect } from 'react';
import { catalogAPI } from '../services/api';
import LoadingSpinner from './LoadingSpinner';

const MarketAnalysis = ({ company }) => {
  const [marketData, setMarketData] = useState(null);
  const [competitivePosition, setCompetitivePosition] = useState(null);
  const [crossSellingData, setCrossSellingData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('market');

  useEffect(() => {
    if (company) {
      loadMarketAnalysis();
    }
  }, [company]);

  const loadMarketAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load all analysis data in parallel
      const [marketRes, positionRes, crossSellingRes] = await Promise.all([
        catalogAPI.getMarketAnalysis(company.industry),
        catalogAPI.getCompetitivePosition(company.company),
        catalogAPI.getCrossSellingRecommendations(company.company)
      ]);

      setMarketData(marketRes.data);
      setCompetitivePosition(positionRes.data);
      setCrossSellingData(crossSellingRes.data);
    } catch (err) {
      setError('Failed to load market analysis data');
      console.error('Market analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="market-analysis-error">
        <h3>⚠️ Error Loading Analysis</h3>
        <p>{error}</p>
        <button onClick={loadMarketAnalysis} className="retry-button">
          🔄 Retry
        </button>
      </div>
    );
  }

  return (
    <div className="market-analysis">
      <div className="analysis-header">
        <h2>📊 Market & Competitive Analysis</h2>
        <p className="company-name">{company.company}</p>
        <p className="industry-badge">{company.industry}</p>
      </div>

      {/* Analysis Navigation Tabs */}
      <div className="analysis-nav">
        <button 
          className={`nav-tab ${activeTab === 'market' ? 'active' : ''}`}
          onClick={() => setActiveTab('market')}
        >
          🏢 Market Overview
        </button>
        <button 
          className={`nav-tab ${activeTab === 'competitive' ? 'active' : ''}`}
          onClick={() => setActiveTab('competitive')}
        >
          ⚔️ Competitive Position
        </button>
        <button 
          className={`nav-tab ${activeTab === 'crossselling' ? 'active' : ''}`}
          onClick={() => setActiveTab('crossselling')}
        >
          🎯 Cross-selling Opportunities
        </button>
      </div>

      {/* Tab Content */}
      <div className="analysis-content">
        {activeTab === 'market' && (
          <MarketOverview marketData={marketData} />
        )}
        {activeTab === 'competitive' && (
          <CompetitivePosition competitiveData={competitivePosition} />
        )}
        {activeTab === 'crossselling' && (
          <CrossSellingOpportunities crossSellingData={crossSellingData} />
        )}
      </div>
    </div>
  );
};

const MarketOverview = ({ marketData }) => {
  const market = marketData?.market_overview || {};
  const competitive = marketData?.competitive_landscape || {};

  return (
    <div className="market-overview">
      {/* Market Size & Growth */}
      <div className="market-metrics">
        <h3>📈 Market Metrics</h3>
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-icon">🌍</div>
            <div className="metric-content">
              <span className="metric-label">Global Market Size</span>
              <span className="metric-value">{market.market_size?.global || 'N/A'}</span>
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-icon">🇪🇺</div>
            <div className="metric-content">
              <span className="metric-label">European Market</span>
              <span className="metric-value">{market.market_size?.europe || 'N/A'}</span>
            </div>
          </div>
          <div className="metric-card">
            <div className="metric-icon">📊</div>
            <div className="metric-content">
              <span className="metric-label">Growth Rate</span>
              <span className="metric-value">{market.growth_rate || 'N/A'}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Market Trends */}
      <div className="market-trends">
        <h3>🔥 Key Market Trends</h3>
        <div className="trends-list">
          {market.key_trends?.map((trend, index) => (
            <div key={index} className="trend-item">
              <span className="trend-icon">📈</span>
              <span className="trend-text">{trend}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Major Competitors */}
      <div className="major-competitors">
        <h3>🏆 Major Market Players</h3>
        <div className="competitors-grid">
          {competitive.major_players?.map((competitor, index) => (
            <div key={index} className="competitor-card">
              <div className="competitor-header">
                <h4>{competitor.name}</h4>
                <span className="market-share">{competitor.market_share}</span>
              </div>
              <div className="competitor-info">
                <p><strong>Target:</strong> {competitor.target_market}</p>
                <p><strong>Pricing:</strong> {competitor.pricing_model}</p>
              </div>
              <div className="competitor-analysis">
                <div className="strengths">
                  <h5>💪 Strengths</h5>
                  <ul>
                    {competitor.strengths?.slice(0, 2).map((strength, i) => (
                      <li key={i}>{strength}</li>
                    ))}
                  </ul>
                </div>
                <div className="weaknesses">
                  <h5>⚠️ Weaknesses</h5>
                  <ul>
                    {competitor.weaknesses?.slice(0, 2).map((weakness, i) => (
                      <li key={i}>{weakness}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Strategic Recommendations */}
      <div className="recommendations">
        <h3>💡 Strategic Recommendations</h3>
        <div className="recommendations-list">
          {marketData?.recommendations?.map((recommendation, index) => (
            <div key={index} className="recommendation-item">
              <span className="recommendation-icon">💡</span>
              <span className="recommendation-text">{recommendation}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const CompetitivePosition = ({ competitiveData }) => {
  const positioning = competitiveData?.positioning || {};

  return (
    <div className="competitive-position">
      {/* Position Score */}
      <div className="position-score">
        <h3>🎯 Market Position Score</h3>
        <div className="score-display">
          <div className="score-circle">
            <span className="score-value">{positioning.positioning_score || 0}</span>
            <span className="score-max">/10</span>
          </div>
          <div className="score-details">
            <p className="market-segment">{positioning.market_segment}</p>
            <p className="market-presence">{positioning.market_presence}</p>
          </div>
        </div>
      </div>

      {/* Competitive Advantages */}
      <div className="competitive-advantages">
        <h3>🏅 Competitive Advantages</h3>
        <div className="advantages-list">
          {positioning.competitive_advantages?.map((advantage, index) => (
            <div key={index} className="advantage-item">
              <span className="advantage-icon">✅</span>
              <span className="advantage-text">{advantage}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Areas for Improvement */}
      <div className="improvement-areas">
        <h3>🔧 Areas for Improvement</h3>
        <div className="improvement-list">
          {positioning.areas_for_improvement?.map((area, index) => (
            <div key={index} className="improvement-item">
              <span className="improvement-icon">🔧</span>
              <span className="improvement-text">{area}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Opportunities & Threats */}
      <div className="swot-analysis">
        <div className="opportunities">
          <h3>🚀 Market Opportunities</h3>
          <div className="opportunities-list">
            {competitiveData?.market_opportunities?.map((opportunity, index) => (
              <div key={index} className="opportunity-item">
                <span className="opportunity-icon">🚀</span>
                <span className="opportunity-text">{opportunity}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="threats">
          <h3>⚠️ Competitive Threats</h3>
          <div className="threats-list">
            {competitiveData?.competitive_threats?.map((threat, index) => (
              <div key={index} className="threat-item">
                <span className="threat-icon">⚠️</span>
                <span className="threat-text">{threat}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const CrossSellingOpportunities = ({ crossSellingData }) => {
  const opportunities = crossSellingData?.cross_selling_opportunities || [];
  const groupCompanies = crossSellingData?.group_companies || [];

  return (
    <div className="cross-selling-opportunities">
      {/* Group Overview */}
      <div className="group-overview">
        <h3>🏢 Company Group Overview</h3>
        <div className="group-info">
          <p><strong>Parent Company:</strong> {crossSellingData?.parent_company || 'Independent'}</p>
          <p><strong>Group Companies:</strong> {groupCompanies.length + 1} companies</p>
        </div>
        {groupCompanies.length > 0 && (
          <div className="group-companies">
            <h4>Related Companies:</h4>
            <div className="companies-list">
              {groupCompanies.map((companyName, index) => (
                <span key={index} className="company-tag">{companyName}</span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Cross-selling Opportunities */}
      {opportunities.length > 0 ? (
        <div className="opportunities-section">
          <h3>💰 Cross-selling Opportunities</h3>
          {opportunities.map((opportunity, index) => (
            <div key={index} className="opportunity-card">
              <div className="opportunity-header">
                <h4>🤝 Partnership with {opportunity.company}</h4>
              </div>
              
              {/* Complementary Products */}
              <div className="complementary-products">
                <h5>📦 Complementary Products</h5>
                <div className="products-grid">
                  {opportunity.complementary_products?.map((product, productIndex) => (
                    <div key={productIndex} className="product-opportunity">
                      <div className="product-header">
                        <span className="product-name">{product.product_name}</span>
                        <span className={`potential-badge ${product.cross_sell_potential?.toLowerCase()}`}>
                          {product.cross_sell_potential} Potential
                        </span>
                      </div>
                      <div className="product-details">
                        <span className="product-category">{product.category}</span>
                        <span className="synergy-score">Synergy: {product.synergy_score}/10</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Partnership Opportunities */}
              <div className="partnership-opportunities">
                <h5>🤝 Partnership Strategies</h5>
                <div className="strategies-list">
                  {opportunity.partnership_opportunities?.map((strategy, strategyIndex) => (
                    <div key={strategyIndex} className="strategy-item">
                      <span className="strategy-icon">💡</span>
                      <span className="strategy-text">{strategy}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="no-opportunities">
          <h3>💼 Independent Company</h3>
          <p>This company operates independently with no direct group partnerships for cross-selling.</p>
          <div className="suggestions">
            <h4>💡 Suggestions for Growth:</h4>
            <ul>
              <li>Explore strategic partnerships with complementary solution providers</li>
              <li>Consider acquisition opportunities in related markets</li>
              <li>Develop integration partnerships with major platforms</li>
              <li>Build an ecosystem of third-party add-ons and extensions</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default MarketAnalysis;
