import React, { useState, useEffect } from "react";
import { TrendingUp, Calendar, Filter, RefreshCw } from "lucide-react";
import DashboardHeader from "./DashboardHeader";
import DashboardFilters from "./DashboardFilters";
import DashboardLayout from "./DashboardLayout";
import SalesOverviewCards from "./SalesOverviewCards";
import SalesTrendChart from "./SalesTrendChart";
import SectorDonutChart from "./SectorDonutChart";
import ProductBarChart from "./ProductBarChart";
import SectorTable from "./SectorTable";
import ProductTable from "./ProductTable";
import LoadingSpinner from "./LoadingSpinner";
import { salesAPI } from "../services/api";

const SalesTrendsDashboard = () => {
  // Dashboard state
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  // Data state
  const [salesData, setSalesData] = useState({
    overview: {},
    trends: [],
    sectors: [],
    products: [],
    topProducts: [],
    sectorPerformance: []
  });

  // Filter state
  const [filters, setFilters] = useState({
    period: "12months",
    sector: "all",
    region: "all",
    dateRange: null,
    metric: "revenue" // revenue or units
  });

  // UI state
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [refreshInterval, setRefreshInterval] = useState(null);

  // Load dashboard data
  useEffect(() => {
    loadDashboardData();
  }, [filters]);

  // Auto-refresh functionality
  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        loadDashboardData();
      }, 300000); // Refresh every 5 minutes
      setRefreshInterval(interval);
    } else {
      if (refreshInterval) {
        clearInterval(refreshInterval);
        setRefreshInterval(null);
      }
    }

    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, [autoRefresh]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Parallel API calls for better performance
      const [
        summaryRes,
        trendsRes,
        sectorsRes,
        topProductsRes
      ] = await Promise.all([
        salesAPI.getSalesSummary(filters),
        salesAPI.getAllProductsTrends(filters),
        salesAPI.getSectorAnalysis(filters),
        salesAPI.getTopProducts(filters)
      ]);

      // Transform API data to match component expectations
      const topSector = sectorsRes.data.sectors?.[0];
      const topProduct = topProductsRes.data.top_products?.[0];
      
      // Debug logging (removed for production)
      
      setSalesData({
        overview: {
          total_revenue: summaryRes.data.total_revenue,
          total_units: summaryRes.data.total_units,
          revenue_growth: summaryRes.data.average_growth_rate,
          units_growth: summaryRes.data.average_growth_rate,
          growth_acceleration: 2.5, // Mock data
          top_sector: topSector ? {
            name: topSector.sector,
            value: topSector.total_revenue,
            growth: topSector.average_growth_rate
          } : null,
          best_product: topProduct ? {
            name: topProduct.product_id,
            value: topProduct.total_revenue,
            growth: topProduct.average_growth_rate
          } : null
        },
        trends: Array.isArray(trendsRes.data) ? trendsRes.data : [],
        sectors: Array.isArray(sectorsRes.data.sectors) ? sectorsRes.data.sectors : [],
        products: Array.isArray(topProductsRes.data.top_products) ? topProductsRes.data.top_products : [],
        topProducts: Array.isArray(topProductsRes.data.top_products) ? topProductsRes.data.top_products : [],
        sectorPerformance: Array.isArray(sectorsRes.data.sectors) ? sectorsRes.data.sectors : []
      });

      setLastUpdated(new Date());
    } catch (err) {
      console.error("Error loading dashboard data:", err);
      setError("Failed to load dashboard data. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handleRefresh = () => {
    loadDashboardData();
  };

  const handleAutoRefreshToggle = () => {
    setAutoRefresh(prev => !prev);
  };

  if (loading && !salesData.overview.total_revenue) {
    return <LoadingSpinner />;
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="error-state">
          <h3>Dashboard Error</h3>
          <p>{error}</p>
          <button onClick={handleRefresh} className="retry-button">
            <RefreshCw size={16} />
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <DashboardHeader
        title="Sales Trends Dashboard"
        subtitle="Track product performance across sectors and regions"
        lastUpdated={lastUpdated}
        autoRefresh={autoRefresh}
        onAutoRefreshToggle={handleAutoRefreshToggle}
        onRefresh={handleRefresh}
        loading={loading}
      />

      <DashboardFilters
        filters={filters}
        onFilterChange={handleFilterChange}
        sectors={salesData.sectors}
      />

      <DashboardLayout>
        {/* Overview Cards Section */}
        <div className="dashboard-section overview-section">
          <SalesOverviewCards 
            data={salesData.overview}
            loading={loading}
            metric={filters.metric}
          />
        </div>

        {/* Charts Section */}
        <div className="dashboard-section charts-section">
          <div className="chart-grid">
              <SalesTrendChart
                data={salesData.trends}
                loading={loading}
                metric={filters.metric}
                period={filters.period}
              />
            
              <SectorDonutChart
                data={salesData.sectorPerformance}
                loading={loading}
                metric={filters.metric}
              />
            
          </div>
        </div>

        {/* Performance Tables Section */}
        <div className="dashboard-section performance-tables-section">
          <div className="chart-grid">
              <SectorTable
                data={salesData.sectorPerformance}
                loading={loading}
                metric={filters.metric}
                onSectorSelect={(sector) => handleFilterChange({ sector })}
              />
            
              <ProductBarChart
                data={salesData.topProducts}
                loading={loading}
                metric={filters.metric}
              />
          </div>
        </div>

        {/* Product Performance Section */}
        <div className="dashboard-section product-performance-section">
          <div className="table-container">
            <ProductTable
              data={salesData.products}
              loading={loading}
              metric={filters.metric}
            />
          </div>
        </div>
      </DashboardLayout>

      {/* Loading overlay for data refresh */}
      {loading && salesData.overview.total_revenue && (
        <div className="refresh-overlay">
          <div className="refresh-indicator">
            <RefreshCw size={20} className="spinning" />
            Updating data...
          </div>
        </div>
      )}
    </div>
  );
};

export default SalesTrendsDashboard;
