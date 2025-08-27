import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";
import { TrendingUp } from "lucide-react";

const SalesTrendChart = ({ data, loading, metric, period }) => {
  // Transform trends data from API response - MUST BE AT TOP (React hooks rule)
  const chartData = React.useMemo(() => {
    if (!data || !Array.isArray(data) || data.length === 0) return [];
    
    // Aggregate all product data by period
    const periodMap = {};
    
    data.forEach(product => {
      if (product.trend_data) {
        product.trend_data.forEach(point => {
          if (!periodMap[point.period]) {
            periodMap[point.period] = {
              period: point.period,
              revenue: 0,
              units: 0,
              count: 0
            };
          }
          periodMap[point.period].revenue += point.revenue || 0;
          periodMap[point.period].units += point.units_sold || 0;
          periodMap[point.period].count += 1;
        });
      }
    });
    
    return Object.values(periodMap).sort((a, b) => new Date(a.period + '-01') - new Date(b.period + '-01'));
  }, [data]);

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

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const periodMap = {
      "1month": { month: "short", day: "numeric" },
      "3months": { month: "short", day: "numeric" },
      "6months": { month: "short" },
      "12months": { month: "short" },
      "24months": { month: "short", year: "2-digit" }
    };
    
    const formatOptions = periodMap[period] || { month: "short", year: "numeric" };
    return date.toLocaleDateString('en-US', formatOptions);
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="chart-tooltip">
          <p className="tooltip-label">{formatDate(label)}</p>
          {payload.map((entry, index) => (
            <p key={index} className="tooltip-value" style={{ color: entry.color }}>
              <span className="tooltip-name">{entry.name}:</span>
              <span className="tooltip-amount">{formatValue(entry.value)}</span>
            </p>
          ))}
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
            <TrendingUp size={18} />
            <span>Sales Trends</span>
          </div>
        </div>
        <div className="chart-loading">
          <div className="chart-skeleton">
            <div className="skeleton-lines">
              {[1, 2, 3, 4, 5].map(i => (
                <div key={i} className="skeleton-line" style={{ height: `${20 + i * 15}%` }}></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!data || !Array.isArray(data) || chartData.length === 0) {
    return (
      <div className="chart-container">
        <div className="chart-header">
          <div className="chart-title">
            <TrendingUp size={18} />
            <span>Sales Trends</span>
          </div>
        </div>
        <div className="chart-empty">
          <p>No trend data available for the selected period.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <div className="chart-header">
        <div className="chart-title">
          <TrendingUp size={18} />
          <span>Sales Trends - {metric === "revenue" ? "Revenue" : "Units Sold"}</span>
        </div>
        <div className="chart-controls">
          <span className="data-points">{chartData.length} data points</span>
        </div>
      </div>
      
      <div className="chart-content">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart
            data={chartData}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
            <XAxis 
              dataKey="period"
              tickFormatter={formatDate}
              fontSize={12}
            />
            <YAxis 
              tickFormatter={(value) => formatValue(value)}
              fontSize={12}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Line
              type="monotone"
              dataKey={metric === "revenue" ? "revenue" : "units"}
              stroke="var(--primary-500)"
              strokeWidth={2}
              dot={{ fill: "var(--primary-500)", strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: "var(--primary-500)", strokeWidth: 2 }}
              name={metric === "revenue" ? "Revenue" : "Units Sold"}
            />
            
            {/* Add moving average line if available */}
            {data[0]?.moving_average && (
              <Line
                type="monotone"
                dataKey="moving_average"
                stroke="var(--accent-500)"
                strokeWidth={1}
                strokeDasharray="5 5"
                dot={false}
                name="Moving Average"
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default SalesTrendChart;
