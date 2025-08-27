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

export default api;
