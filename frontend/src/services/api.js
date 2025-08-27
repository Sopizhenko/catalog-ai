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
