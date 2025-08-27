import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const catalogAPI = {
  // Get all companies
  getCompanies: () => api.get('/companies'),
  
  // Get a specific company
  getCompany: (companyName) => api.get(`/companies/${companyName}`),
  
  // Get all products with optional filters
  getProducts: (filters = {}) => {
    const params = new URLSearchParams();
    
    if (filters.search) params.append('search', filters.search);
    if (filters.category) params.append('category', filters.category);
    if (filters.audience) params.append('audience', filters.audience);
    
    return api.get(`/products?${params.toString()}`);
  },
  
  // Get a specific product
  getProduct: (productId) => api.get(`/products/${productId}`),
  
  // Get all categories
  getCategories: () => api.get('/categories'),
  
  // Get all target audiences
  getAudiences: () => api.get('/audiences'),
  
  // Health check
  healthCheck: () => api.get('/health'),
  
  // Market Analysis APIs
  getMarketAnalysis: (industry) => api.get(`/market-analysis/${encodeURIComponent(industry)}`),
  
  // Competitive Analysis APIs
  getCompetitivePosition: (companyName) => api.get(`/competitive-position/${encodeURIComponent(companyName)}`),
  getProductAnalysis: (productId) => api.get(`/product-analysis/${encodeURIComponent(productId)}`),
  
  // Cross-selling APIs
  getCrossSellingRecommendations: (companyName) => api.get(`/cross-selling/${encodeURIComponent(companyName)}`),
  compareProducts: (productIds) => api.post('/product-comparison', { product_ids: productIds }),
  
  // AI-Powered Analysis APIs
  ai: {
    // Get real-time AI market intelligence
    getMarketIntelligence: (industry, companyName = null) => {
      const params = new URLSearchParams();
      if (companyName) params.append('company', companyName);
      const url = `/ai-market-intelligence/${encodeURIComponent(industry)}`;
      return api.get(params.toString() ? `${url}?${params}` : url);
    },
    
    // Get AI-powered trend analysis
    getTrendAnalysis: (industry, timeHorizon = '6_months') => {
      const params = new URLSearchParams();
      if (timeHorizon) params.append('horizon', timeHorizon);
      const url = `/ai-trend-analysis/${encodeURIComponent(industry)}`;
      return api.get(`${url}?${params}`);
    },
    
    // Get AI trend alerts
    getTrendAlerts: (industry, companyName = null) => {
      const params = new URLSearchParams();
      if (companyName) params.append('company', companyName);
      const url = `/ai-trend-alerts/${encodeURIComponent(industry)}`;
      return api.get(params.toString() ? `${url}?${params}` : url);
    },
    
    // Get comprehensive real-time insights
    getRealTimeInsights: (industry, companyName = null) => {
      const params = new URLSearchParams();
      if (companyName) params.append('company', companyName);
      const url = `/real-time-insights/${encodeURIComponent(industry)}`;
      return api.get(params.toString() ? `${url}?${params}` : url);
    },
    
    // Get AI competitive intelligence
    getCompetitiveIntelligence: (companyName, industry = 'Point of Sale Software') => {
      const params = new URLSearchParams();
      if (industry) params.append('industry', industry);
      const url = `/ai-competitive-intelligence/${encodeURIComponent(companyName)}`;
      return api.get(`${url}?${params}`);
    },
    
    // Get AI competitive scoring
    getCompetitiveScoring: (companyName, industry = 'Point of Sale Software') => {
      const params = new URLSearchParams();
      if (industry) params.append('industry', industry);
      const url = `/ai-competitive-scoring/${encodeURIComponent(companyName)}`;
      return api.get(`${url}?${params}`);
    },
    
    // Get AI analysis service status
    getStatus: () => api.get('/ai-analysis-status')
  },
  
  // FAQ APIs
  faqs: {
    // Get all FAQs with optional filtering
    getAll: (params = {}) => {
      const queryParams = new URLSearchParams();
      
      if (params.search) queryParams.append('search', params.search);
      if (params.category) queryParams.append('category', params.category);
      if (params.limit) queryParams.append('limit', params.limit);
      
      const url = queryParams.toString() ? `/faqs?${queryParams}` : '/faqs';
      return api.get(url);
    },

    // Get specific FAQ
    getById: (id) => api.get(`/faqs/${id}`),

    // Get FAQ categories
    getCategories: () => api.get('/faq-categories'),

    // Advanced search
    search: (query, filters = {}) => 
      api.post('/faq-search', { query, filters }),

    // Get related companies and products for FAQ integration
    getRelatedContent: (faqId) => 
      api.get(`/faqs/${faqId}/related`)
  }
};

// Sales Analytics API
export const salesAPI = {
  // Basic sales endpoints
  getHealthCheck: () => api.get('/sales/health'),
  getSalesSummary: (filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== 'all') {
        params.append(key, filters[key]);
      }
    });
    return api.get(`/sales/summary?${params.toString()}`);
  },
  
  // Sales trends
  getSalesTrends: (filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== 'all') {
        params.append(key, filters[key]);
      }
    });
    return api.get(`/sales/trends?${params.toString()}`);
  },
  
  getAllProductsTrends: (filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== 'all') {
        params.append(key, filters[key]);
      }
    });
    return api.get(`/sales/trends/all?${params.toString()}`);
  },
  
  getProductTrends: (productId, filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== 'all') {
        params.append(key, filters[key]);
      }
    });
    return api.get(`/sales/trends/${productId}?${params.toString()}`);
  },
  
  // Sector analysis
  getSectorAnalysis: (filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== 'all') {
        params.append(key, filters[key]);
      }
    });
    return api.get(`/sales/by-sector?${params.toString()}`);
  },
  
  getSectorTrends: (filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== 'all') {
        params.append(key, filters[key]);
      }
    });
    return api.get(`/sales/sector-trends?${params.toString()}`);
  },
  
  // Product performance
  getTopProducts: (filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== 'all') {
        params.append(key, filters[key]);
      }
    });
    return api.get(`/sales/top-products?${params.toString()}`);
  },
  
  getProductRankings: (filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== 'all') {
        params.append(key, filters[key]);
      }
    });
    return api.get(`/sales/product-rankings?${params.toString()}`);
  },
  
  getProductPerformance: (productId, filters = {}) => {
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== 'all') {
        params.append(key, filters[key]);
      }
    });
    return api.get(`/sales/performance/${productId}?${params.toString()}`);
  },
  
  // Advanced analytics
  getAdvancedQuery: (queryParams) => api.post('/sales/advanced-query', queryParams),
  getQuickFilters: () => api.get('/sales/quick-filters'),
  getCacheStats: () => api.get('/sales/cache-stats'),
  
  // Development endpoints
  getTestData: () => api.get('/sales/test-data'),
  validateData: () => api.get('/sales/validation'),
  reloadData: () => api.post('/sales/reload'),
};

export default api;
