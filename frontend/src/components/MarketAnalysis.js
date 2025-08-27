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
  const [useAI, setUseAI] = useState(true);
  const [aiStatus, setAiStatus] = useState(null);
  const [realTimeInsights, setRealTimeInsights] = useState(null);

  useEffect(() => {
    if (company) {
      loadMarketAnalysis();
    }
  }, [company, useAI]);

  const toggleAI = () => {
    setUseAI(!useAI);
  };

  const loadMarketAnalysis = async () => {
    try {
      setLoading(true);
      setError(null);

      if (useAI) {
        // Load AI-powered analysis with real-time insights
        console.log('Loading AI-powered market analysis...');
        
        // First check AI status
        const statusRes = await catalogAPI.ai.getStatus();
        setAiStatus(statusRes.data);
        
        // Load AI-powered data in parallel
        const [marketRes, positionRes, crossSellingRes, realTimeRes] = await Promise.all([
          catalogAPI.getMarketAnalysis(company.industry), // Enhanced with AI
          catalogAPI.getCompetitivePosition(company.company), // Enhanced with AI
          catalogAPI.getCrossSellingRecommendations(company.company),
          catalogAPI.ai.getRealTimeInsights(company.industry, company.company)
        ]);

        setMarketData(marketRes.data);
        setCompetitivePosition(positionRes.data);
        setCrossSellingData(crossSellingRes.data);
        setRealTimeInsights(realTimeRes.data);
        
        console.log('AI-powered analysis loaded successfully');
      } else {
        // Load traditional analysis
        console.log('Loading traditional market analysis...');
        
        const [marketRes, positionRes, crossSellingRes] = await Promise.all([
          catalogAPI.getMarketAnalysis(company.industry),
          catalogAPI.getCompetitivePosition(company.company),
          catalogAPI.getCrossSellingRecommendations(company.company)
        ]);

        setMarketData(marketRes.data);
        setCompetitivePosition(positionRes.data);
        setCrossSellingData(crossSellingRes.data);
        setRealTimeInsights(null);
      }
    } catch (err) {
      setError(useAI ? 'Failed to load AI market analysis data' : 'Failed to load market analysis data');
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
        <div className="header-main">
          <h2>📊 Market & Competitive Analysis</h2>
          <p className="company-name">{company.company}</p>
          <p className="industry-badge">{company.industry}</p>
        </div>
        
        {/* AI Toggle and Status */}
        <div className="ai-controls">
          <div className="ai-toggle">
            <label className="toggle-label">
              <input 
                type="checkbox" 
                checked={useAI} 
                onChange={toggleAI}
                className="toggle-input"
              />
              <span className="toggle-slider"></span>
              <span className="toggle-text">
                {useAI ? '🤖 AI-Powered Analysis' : '📊 Traditional Analysis'}
              </span>
            </label>
          </div>
          
          {/* AI Status Indicator */}
          {useAI && aiStatus && (
            <div className="ai-status">
              <div className={`status-indicator ${aiStatus.status === 'active' ? 'active' : 'inactive'}`}>
                <span className="status-dot"></span>
                <span className="status-text">
                  {aiStatus.status === 'active' ? 'AI Services Active' : 'AI Services Unavailable'}
                </span>
              </div>
              {aiStatus.confidence_score && (
                <div className="confidence-score">
                  Confidence: {Math.round(aiStatus.confidence_score * 100)}%
                </div>
              )}
            </div>
          )}
        </div>
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
      {/* Market Summary Table */}
      <div className="market-summary">
        <h3>📊 Market Intelligence Summary</h3>
        <div className="market-summary-table-container">
          <table className="market-summary-table">
            <thead>
              <tr>
                <th>Market Metric</th>
                <th>Value</th>
                <th>Status</th>
                <th>Trend</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="metric-name">
                  <span className="metric-icon">🌍</span>
                  Global Market Size
                </td>
                <td className="metric-value">{market.market_size?.global || 'N/A'}</td>
                <td className="status-cell">
                  <span className="status-badge expanding">📈 Expanding</span>
                </td>
                <td className="trend-cell">
                  <span className="trend-positive">↗️ Growing</span>
                </td>
              </tr>
              <tr>
                <td className="metric-name">
                  <span className="metric-icon">🇪🇺</span>
                  European Market
                </td>
                <td className="metric-value">{market.market_size?.europe || 'N/A'}</td>
                <td className="status-cell">
                  <span className="status-badge strong">💪 Strong</span>
                </td>
                <td className="trend-cell">
                  <span className="trend-positive">↗️ Growing</span>
                </td>
              </tr>
              <tr>
                <td className="metric-name">
                  <span className="metric-icon">📊</span>
                  Annual Growth Rate
                </td>
                <td className="metric-value">{market.growth_rate || 'N/A'}</td>
                <td className="status-cell">
                  <span className="status-badge healthy">✅ Healthy</span>
                </td>
                <td className="trend-cell">
                  <span className="trend-positive">🚀 Accelerating</span>
                </td>
              </tr>
              <tr>
                <td className="metric-name">
                  <span className="metric-icon">🎯</span>
                  Market Maturity
                </td>
                <td className="metric-value">Moderate</td>
                <td className="status-cell">
                  <span className="status-badge growing">🌱 Growing</span>
                </td>
                <td className="trend-cell">
                  <span className="trend-positive">📈 Maturing</span>
                </td>
              </tr>
              <tr>
                <td className="metric-name">
                  <span className="metric-icon">🏆</span>
                  Market Concentration
                </td>
                <td className="metric-value">{competitive.market_concentration || 'Moderate'}</td>
                <td className="status-cell">
                  <span className="status-badge competitive">⚔️ Competitive</span>
                </td>
                <td className="trend-cell">
                  <span className="trend-neutral">➡️ Stable</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Market Trends Table */}
      <div className="market-trends-table">
        <h3>🔥 Key Market Trends Analysis</h3>
        <div className="trends-table-container">
          <table className="trends-analysis-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Market Trend</th>
                <th>Impact Level</th>
                <th>Timeline</th>
                <th>Opportunity</th>
              </tr>
            </thead>
            <tbody>
              {market.key_trends?.map((trend, index) => (
                <tr key={index}>
                  <td className="rank-cell">#{index + 1}</td>
                  <td className="trend-description">
                    <span className="trend-icon">📈</span>
                    {trend}
                  </td>
                  <td className="impact-level">
                    {index < 2 ? (
                      <span className="impact-high">🔥 High</span>
                    ) : index < 4 ? (
                      <span className="impact-medium">⚡ Medium</span>
                    ) : (
                      <span className="impact-low">💡 Moderate</span>
                    )}
                  </td>
                  <td className="timeline-cell">
                    {index < 2 ? "Current" : index < 4 ? "Near-term" : "Long-term"}
                  </td>
                  <td className="opportunity-level">
                    {index < 2 ? (
                      <span className="opportunity-high">🎯 Major</span>
                    ) : index < 4 ? (
                      <span className="opportunity-medium">📊 Significant</span>
                    ) : (
                      <span className="opportunity-low">💡 Emerging</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Major Market Players Table */}
      <div className="market-players-analysis">
        <h3>🏆 Major Market Players Analysis</h3>
        <div className="players-table-container">
          <table className="market-players-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Company</th>
                <th>Market Share</th>
                <th>Target Market</th>
                <th>Pricing Model</th>
                <th>Competitive Status</th>
              </tr>
            </thead>
            <tbody>
              {competitive.major_players?.map((competitor, index) => (
                <tr key={index}>
                  <td className="player-rank">#{index + 1}</td>
                  <td className="company-name">
                    <div className="company-info">
                      <span className="company-title">{competitor.name}</span>
                    </div>
                  </td>
                  <td className="market-share-cell">
                    <div className="share-display">
                      <span className="share-value">{competitor.market_share}</span>
                      <div className="share-bar">
                        <div 
                          className="share-fill" 
                          style={{width: `${parseInt(competitor.market_share) || 15}%`}}
                        ></div>
                      </div>
                    </div>
                  </td>
                  <td className="target-market">{competitor.target_market}</td>
                  <td className="pricing-model">
                    <span className={`pricing-badge ${competitor.pricing_model?.toLowerCase()}`}>
                      {competitor.pricing_model}
                    </span>
                  </td>
                  <td className="competitive-status">
                    {index === 0 ? (
                      <span className="status-leader">👑 Leader</span>
                    ) : index < 3 ? (
                      <span className="status-strong">💪 Strong</span>
                    ) : (
                      <span className="status-emerging">🌱 Emerging</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Detailed Competitor Analysis */}
        {competitive.major_players?.length > 0 && (
          <div className="detailed-competitor-analysis">
            <h4>📋 Detailed Competitive Intelligence</h4>
            <div className="competitor-details-table-container">
              <table className="competitor-details-table">
                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Key Strengths</th>
                    <th>Notable Weaknesses</th>
                    <th>Strategic Focus</th>
                  </tr>
                </thead>
                <tbody>
                  {competitive.major_players?.slice(0, 3).map((competitor, index) => (
                    <tr key={index}>
                      <td className="competitor-name-detail">{competitor.name}</td>
                      <td className="strengths-cell">
                        <ul className="strengths-list">
                          {competitor.strengths?.slice(0, 2).map((strength, i) => (
                            <li key={i}>
                              <span className="strength-icon">✅</span>
                              {strength}
                            </li>
                          ))}
                        </ul>
                      </td>
                      <td className="weaknesses-cell">
                        <ul className="weaknesses-list">
                          {competitor.weaknesses?.slice(0, 2).map((weakness, i) => (
                            <li key={i}>
                              <span className="weakness-icon">⚠️</span>
                              {weakness}
                            </li>
                          ))}
                        </ul>
                      </td>
                      <td className="strategic-focus">{competitor.target_market}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* Strategic Recommendations Table */}
      <div className="strategic-recommendations-table">
        <h3>💡 Strategic Recommendations Matrix</h3>
        <div className="recommendations-table-container">
          <table className="recommendations-analysis-table">
            <thead>
              <tr>
                <th>Priority</th>
                <th>Strategic Recommendation</th>
                <th>Implementation</th>
                <th>Expected Impact</th>
                <th>Resource Level</th>
              </tr>
            </thead>
            <tbody>
              {marketData?.recommendations?.map((recommendation, index) => (
                <tr key={index}>
                  <td className="priority-rank">
                    {index < 2 ? (
                      <span className="priority-critical">🔴 Critical</span>
                    ) : index < 4 ? (
                      <span className="priority-high">🟡 High</span>
                    ) : (
                      <span className="priority-medium">🟢 Medium</span>
                    )}
                  </td>
                  <td className="recommendation-text">
                    <span className="recommendation-icon">💡</span>
                    {recommendation}
                  </td>
                  <td className="implementation-timeline">
                    {index < 2 ? "Immediate (0-3 months)" : 
                     index < 4 ? "Short-term (3-6 months)" : 
                     "Medium-term (6-12 months)"}
                  </td>
                  <td className="expected-impact">
                    {index < 2 ? (
                      <span className="impact-major">🚀 Major</span>
                    ) : index < 4 ? (
                      <span className="impact-significant">📈 Significant</span>
                    ) : (
                      <span className="impact-moderate">📊 Moderate</span>
                    )}
                  </td>
                  <td className="resource-level">
                    {index < 2 ? "High" : index < 4 ? "Medium" : "Low"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const CompetitivePosition = ({ competitiveData }) => {
  const positioning = competitiveData?.positioning || {};
  const competitors = competitiveData?.competitors || [];

  return (
    <div className="competitive-position">
      {/* Position Summary Table */}
      <div className="position-summary">
        <h3>🎯 Market Position Summary</h3>
        <div className="summary-table-container">
          <table className="position-summary-table">
            <tbody>
              <tr>
                <td className="metric-label">Overall Score</td>
                <td className="metric-value">
                  <div className="score-display-inline">
                    <span className="score-value">{positioning.positioning_score || 0}</span>
                    <span className="score-max">/10</span>
                    <div className="score-bar-inline">
                      <div 
                        className="score-fill-inline" 
                        style={{width: `${((positioning.positioning_score || 0) / 10) * 100}%`}}
                      ></div>
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td className="metric-label">Market Segment</td>
                <td className="metric-value">{positioning.market_segment || 'Not specified'}</td>
              </tr>
              <tr>
                <td className="metric-label">Market Presence</td>
                <td className="metric-value">{positioning.market_presence || 'Not assessed'}</td>
              </tr>
              <tr>
                <td className="metric-label">Industry</td>
                <td className="metric-value">{competitiveData?.industry || 'Not specified'}</td>
              </tr>
              <tr>
                <td className="metric-label">Product Portfolio</td>
                <td className="metric-value">{competitiveData?.products_count || 0} products</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Competitive Analysis Tables */}
      <div className="competitive-analysis-tables">
        <div className="advantages-table-section">
          <h3>🏅 Competitive Advantages</h3>
          <div className="advantages-table-container">
            <table className="competitive-analysis-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Competitive Advantage</th>
                  <th>Impact</th>
                </tr>
              </thead>
              <tbody>
                {positioning.competitive_advantages?.map((advantage, index) => (
                  <tr key={index}>
                    <td className="rank-cell">#{index + 1}</td>
                    <td className="advantage-text">{advantage}</td>
                    <td className="impact-cell">
                      {index < 2 ? (
                        <span className="impact-high">🔥 High</span>
                      ) : index < 4 ? (
                        <span className="impact-medium">⚡ Medium</span>
                      ) : (
                        <span className="impact-low">💡 Low</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="improvements-table-section">
          <h3>🔧 Areas for Improvement</h3>
          <div className="improvements-table-container">
            <table className="competitive-analysis-table">
              <thead>
                <tr>
                  <th>Priority</th>
                  <th>Improvement Area</th>
                  <th>Urgency</th>
                </tr>
              </thead>
              <tbody>
                {positioning.areas_for_improvement?.map((area, index) => (
                  <tr key={index}>
                    <td className="priority-cell">
                      {index < 2 ? (
                        <span className="priority-high">🔴 High</span>
                      ) : index < 4 ? (
                        <span className="priority-medium">🟡 Medium</span>
                      ) : (
                        <span className="priority-low">🟢 Low</span>
                      )}
                    </td>
                    <td className="improvement-text">{area}</td>
                    <td className="urgency-cell">
                      {index < 2 ? "Immediate" : index < 4 ? "Short-term" : "Long-term"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Competitors Analysis Table */}
      {competitors.length > 0 && (
        <div className="competitors-analysis">
          <h3>🏢 Competitor Analysis</h3>
          <div className="competitors-table-container">
            <table className="competitors-table">
              <thead>
                <tr>
                  <th>Competitor</th>
                  <th>Products</th>
                  <th>Categories</th>
                  <th>Threat Level</th>
                  <th>Overlap</th>
                </tr>
              </thead>
              <tbody>
                {competitors.map((competitor, index) => (
                  <tr key={index}>
                    <td className="competitor-name">{competitor.name}</td>
                    <td className="products-count">{competitor.products_count}</td>
                    <td className="categories-count">{competitor.categories?.length || 0}</td>
                    <td className="threat-level">
                      <span className={`threat-badge ${competitor.threat_level?.toLowerCase()}`}>
                        {competitor.threat_level === 'High' && '🔴'}
                        {competitor.threat_level === 'Medium' && '🟡'}
                        {competitor.threat_level === 'Low' && '🟢'}
                        {competitor.threat_level}
                      </span>
                    </td>
                    <td className="overlap-score">{competitor.overlap_categories || 0} categories</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* SWOT Analysis Table */}
      <div className="swot-analysis-table">
        <h3>📊 SWOT Analysis Overview</h3>
        <div className="swot-table-container">
          <table className="swot-table">
            <thead>
              <tr>
                <th className="swot-header opportunities-header">🚀 Market Opportunities</th>
                <th className="swot-header threats-header">⚠️ Competitive Threats</th>
              </tr>
            </thead>
            <tbody>
              {Array.from({ 
                length: Math.max(
                  competitiveData?.market_opportunities?.length || 0, 
                  competitiveData?.competitive_threats?.length || 0
                )
              }).map((_, index) => (
                <tr key={index}>
                  <td className="opportunity-cell">
                    {competitiveData?.market_opportunities?.[index] ? (
                      <div className="swot-item">
                        <span className="swot-icon">🚀</span>
                        <span className="swot-text">{competitiveData.market_opportunities[index]}</span>
                      </div>
                    ) : (
                      <div className="empty-cell">-</div>
                    )}
                  </td>
                  <td className="threat-cell">
                    {competitiveData?.competitive_threats?.[index] ? (
                      <div className="swot-item">
                        <span className="swot-icon">⚠️</span>
                        <span className="swot-text">{competitiveData.competitive_threats[index]}</span>
                      </div>
                    ) : (
                      <div className="empty-cell">-</div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const CrossSellingOpportunities = ({ crossSellingData }) => {
  const opportunities = crossSellingData?.cross_selling_opportunities || [];
  const groupCompanies = crossSellingData?.group_companies || [];
  
  // State for selected company
  const [selectedCompany, setSelectedCompany] = useState('');
  
  // Get unique companies from opportunities
  const availableCompanies = opportunities.map(opp => opp.company);
  
  // Set default selection when opportunities change
  React.useEffect(() => {
    if (availableCompanies.length > 0 && !selectedCompany) {
      setSelectedCompany(availableCompanies[0]);
    }
  }, [availableCompanies, selectedCompany]);
  
  // Filter opportunities based on selected company
  const selectedOpportunity = opportunities.find(opp => opp.company === selectedCompany);

  return (
    <div className="cross-selling-opportunities">
      {/* Group Overview */}
      <div className="group-overview">
        <h3>🏢 Company Group Overview</h3>
        <div className="group-info">
          <p><strong>Parent Company:</strong> {crossSellingData?.parent_company || 'Independent'}</p>
          <p><strong>Group Companies:</strong> {groupCompanies.length + 1} companies</p>
        </div>

      </div>

      {/* Cross-selling Opportunities */}
      {opportunities.length > 0 ? (
        <div className="opportunities-section">
          <div className="section-header">
            <h3>💰 Cross-selling Opportunities</h3>
            
            {/* Company Selection Dropdown */}
            <div className="company-selector">
              <label htmlFor="company-select">Select Company:</label>
              <select 
                id="company-select"
                value={selectedCompany}
                onChange={(e) => setSelectedCompany(e.target.value)}
                className="company-dropdown"
              >
                {availableCompanies.map((company, index) => (
                  <option key={index} value={company}>
                    {company}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Display selected company's opportunities */}
          {selectedOpportunity && (
            <div className="cross-selling-analysis">
              <div className="partnership-header">
                <h4>🤝 Collaboration with {selectedOpportunity.company}</h4>
                {selectedOpportunity.partnership_type && (
                  <span className={`partnership-type-badge ${selectedOpportunity.partnership_type?.toLowerCase().replace(' ', '-')}`}>
                    {selectedOpportunity.partnership_type}
                  </span>
                )}
              </div>
              
              {/* Complementary Products Table */}
              <div className="complementary-products-section">
                <h5>📦 Complementary Products Analysis</h5>
                {selectedOpportunity.complementary_products?.length > 0 ? (
                  <div className="products-table-container">
                    <table className="cross-selling-products-table">
                      <thead>
                        <tr>
                          <th>Product Name</th>
                          <th>Category</th>
                          <th>Cross-sell Potential</th>
                          <th>Synergy Score</th>
                          <th>Opportunity Level</th>
                        </tr>
                      </thead>
                      <tbody>
                        {selectedOpportunity.complementary_products.map((product, productIndex) => (
                          <tr key={productIndex}>
                            <td className="product-name-cell">
                              <span className="product-name">{product.product_name}</span>
                            </td>
                            <td className="category-cell">
                              <span className="category-badge">{product.category}</span>
                            </td>
                            <td className="potential-cell">
                              <span className={`potential-indicator ${product.cross_sell_potential?.toLowerCase()}`}>
                                {product.cross_sell_potential === 'High' && '🔥'}
                                {product.cross_sell_potential === 'Medium' && '⚡'}
                                {product.cross_sell_potential === 'Low' && '💡'}
                                {product.cross_sell_potential}
                              </span>
                            </td>
                            <td className="synergy-cell">
                              <div className="synergy-score">
                                <span className="score-number">{product.synergy_score}/10</span>
                                <div className="score-bar">
                                  <div 
                                    className="score-fill" 
                                    style={{width: `${(product.synergy_score / 10) * 100}%`}}
                                  ></div>
                                </div>
                              </div>
                            </td>
                            <td className="opportunity-cell">
                              {product.synergy_score >= 8 ? (
                                <span className="opportunity-high">🎯 High Value</span>
                              ) : product.synergy_score >= 6 ? (
                                <span className="opportunity-medium">📈 Good Fit</span>
                              ) : (
                                <span className="opportunity-low">🔍 Explore</span>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="no-products">
                    <p>No complementary products identified for this partnership.</p>
                  </div>
                )}
              </div>

              {/* Collaboration Strategies Table */}
              <div className="strategies-section">
                <h5>🤝 Collaboration Strategies</h5>
                {selectedOpportunity.partnership_opportunities?.length > 0 ? (
                  <div className="strategies-table-container">
                    <table className="collaboration-strategies-table">
                      <thead>
                        <tr>
                          <th>Strategy</th>
                          <th>Implementation</th>
                          <th>Priority</th>
                        </tr>
                      </thead>
                      <tbody>
                        {selectedOpportunity.partnership_opportunities.map((strategy, strategyIndex) => (
                          <tr key={strategyIndex}>
                            <td className="strategy-cell">
                              <span className="strategy-icon">💡</span>
                              <span className="strategy-text">{strategy}</span>
                            </td>
                            <td className="implementation-cell">
                              {strategyIndex === 0 && "Short-term (1-3 months)"}
                              {strategyIndex === 1 && "Medium-term (3-6 months)"}
                              {strategyIndex === 2 && "Long-term (6-12 months)"}
                              {strategyIndex >= 3 && "Future consideration"}
                            </td>
                            <td className="priority-cell">
                              {strategyIndex === 0 && <span className="priority-high">🔴 High</span>}
                              {strategyIndex === 1 && <span className="priority-medium">🟡 Medium</span>}
                              {strategyIndex >= 2 && <span className="priority-low">🟢 Low</span>}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="no-strategies">
                    <p>No specific collaboration strategies defined yet.</p>
                  </div>
                )}
              </div>
            </div>
          )}
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
