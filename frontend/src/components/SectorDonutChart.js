import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend
} from "recharts";
import { PieChart as PieIcon } from "lucide-react";

const SectorDonutChart = ({ data, loading, metric }) => {
  const colors = [
    "var(--primary-500)",
    "var(--accent-500)",
    "var(--secondary-400)",
    "var(--primary-300)",
    "var(--accent-300)",
    "var(--secondary-600)",
    "var(--primary-700)",
    "var(--accent-700)"
  ];

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

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="chart-tooltip">
          <p className="tooltip-label">{data.name}</p>
          <p className="tooltip-value">
            <span className="tooltip-name">
              {metric === "revenue" ? "Revenue" : "Units"}:
            </span>
            <span className="tooltip-amount">{formatValue(data.value)}</span>
          </p>
          <p className="tooltip-value">
            <span className="tooltip-name">Share:</span>
            <span className="tooltip-amount">{data.percentageDisplay}%</span>
          </p>
        </div>
      );
    }
    return null;
  };

  const renderCustomLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percentage }) => {
    // Ensure percentage is a valid number
    const numPercentage = typeof percentage === 'number' ? percentage : parseFloat(percentage) || 0;
    
    if (numPercentage < 5) return null; // Don't show labels for small slices
    
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        fontSize={12}
        fontWeight={500}
      >
        {`${numPercentage.toFixed(0)}%`}
      </text>
    );
  };

  if (loading) {
    return (
      <div className="chart-container">
        <div className="chart-header">
          <div className="chart-title">
            <PieIcon size={18} />
            <span>Sector Distribution</span>
          </div>
        </div>
        <div className="chart-loading">
          <div className="donut-skeleton">
            <div className="skeleton-donut"></div>
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
            <PieIcon size={18} />
            <span>Sector Distribution</span>
          </div>
        </div>
        <div className="chart-empty">
          <p>No sector data available.</p>
        </div>
      </div>
    );
  }

  // Calculate percentages and format data
  const totalValue = data.reduce((sum, item) => {
    const itemValue = metric === "revenue" ? (item.total_revenue || 0) : (item.total_units || 0);
    return sum + itemValue;
  }, 0);
  
  const chartData = data.map((item, index) => {
    const itemValue = metric === "revenue" ? (item.total_revenue || 0) : (item.total_units || 0);
    const percentage = totalValue > 0 ? (itemValue / totalValue) * 100 : 0;
    
    return {
      ...item,
      name: item.sector,
      value: itemValue,
      percentage: percentage, // Keep as number for chart library
      percentageDisplay: percentage.toFixed(1), // String for display
      color: colors[index % colors.length]
    };
  });

  return (
    <div className="chart-container">
      <div className="chart-header">
        <div className="chart-title">
          <PieIcon size={18} />
          <span>Sector Distribution - {metric === "revenue" ? "Revenue" : "Units"}</span>
        </div>
        <div className="chart-controls">
          <span className="data-points">{data.length} sectors</span>
        </div>
      </div>
      
      <div className="chart-content">
        <ResponsiveContainer width="100%" height={280}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={renderCustomLabel}
              outerRadius={100}
              innerRadius={40}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
        
        {/* Custom Legend */}
        <div className="sector-legend">
          {chartData.map((entry, index) => (
            <div key={entry.name} className="legend-item">
              <div 
                className="legend-color" 
                style={{ backgroundColor: entry.color }}
              ></div>
              <div className="legend-content">
                <span className="legend-name">{entry.name}</span>
                <span className="legend-value">
                  {formatValue(entry.value)} ({entry.percentageDisplay}%)
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SectorDonutChart;
