import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import { BarChart3 } from "lucide-react";

const ProductBarChart = ({ data, loading, metric }) => {
  const formatValue = (value) => {
    if (!value && value !== 0) return "N/A";
    
    if (metric === "revenue") {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value);
    }
    
    return new Intl.NumberFormat('en-US').format(value);
  };

  const formatProductName = (name) => {
    if (!name) return "";
    // Truncate long product names for display
    return name.length > 20 ? `${name.substring(0, 17)}...` : name;
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="chart-tooltip">
          <p className="tooltip-label">{data.full_name || label}</p>
          <p className="tooltip-value">
            <span className="tooltip-name">Company:</span>
            <span className="tooltip-amount">{data.company}</span>
          </p>
          <p className="tooltip-value">
            <span className="tooltip-name">
              {metric === "revenue" ? "Revenue" : "Units Sold"}:
            </span>
            <span className="tooltip-amount">{formatValue(payload[0].value)}</span>
          </p>
          {data.growth !== undefined && (
            <p className="tooltip-value">
              <span className="tooltip-name">Growth:</span>
              <span className={`tooltip-amount ${data.growth >= 0 ? 'positive' : 'negative'}`}>
                {data.growth > 0 ? '+' : ''}{data.growth.toFixed(1)}%
              </span>
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <div className="chart-container">
        <div className="chart-header">
          <div className="chart-title">
            <BarChart3 size={18} />
            <span>Top Performing Products</span>
          </div>
        </div>
        <div className="chart-loading">
          <div className="chart-skeleton">
            <div className="skeleton-bars">
              {[1, 2, 3, 4, 5].map(i => (
                <div 
                  key={i} 
                  className="skeleton-bar" 
                  style={{ height: `${30 + i * 10}%` }}
                ></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!data || !Array.isArray(data) || data.length === 0) {
    return (
      <div className="chart-container">
        <div className="chart-header">
          <div className="chart-title">
            <BarChart3 size={18} />
            <span>Top Performing Products</span>
          </div>
        </div>
        <div className="chart-empty">
          <p>No product performance data available.</p>
        </div>
      </div>
    );
  }

  // Prepare chart data with proper formatting
  const chartData = data.slice(0, 10).map(item => ({
    ...item,
    name: formatProductName(item.product_id),
    full_name: item.product_id,
    value: item[metric === "revenue" ? "total_revenue" : "total_units"] || 0,
    growth: item.average_growth_rate
  }));

  return (
    <div className="chart-container">
      <div className="chart-header">
        <div className="chart-title">
          <BarChart3 size={18} />
          <span>Top Performing Products - {metric === "revenue" ? "Revenue" : "Units Sold"}</span>
        </div>
        <div className="chart-controls">
          <span className="data-points">Top {chartData.length} products</span>
        </div>
      </div>
      
      <div className="chart-content">
        <ResponsiveContainer width="100%" height={350}>
          <BarChart
            data={chartData}
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 60,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
            <XAxis 
              dataKey="name"
              angle={-45}
              textAnchor="end"
              height={80}
              fontSize={11}
            />
            <YAxis 
              tickFormatter={(value) => formatValue(value)}
              fontSize={12}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar 
              dataKey="value" 
              fill="var(--primary-500)"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
        
        {/* Performance indicators */}
        <div className="chart-footer">
          <div className="performance-summary">
            <div className="summary-item">
              <span className="summary-label">Highest:</span>
              <span className="summary-value">
                {formatValue(chartData[0]?.value)} ({chartData[0]?.full_name})
              </span>
            </div>
            <div className="summary-item">
              <span className="summary-label">Average:</span>
              <span className="summary-value">
                {formatValue(chartData.reduce((sum, item) => sum + item.value, 0) / chartData.length)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductBarChart;
