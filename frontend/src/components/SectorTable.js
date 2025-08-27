import React, { useState } from "react";
import { 
  ChevronDown, 
  ChevronUp, 
  TrendingUp, 
  TrendingDown, 
  Download, 
  Eye 
} from "lucide-react";

const SectorTable = ({ data, loading, metric, onSectorSelect }) => {
  const [sortField, setSortField] = useState("value");
  const [sortDirection, setSortDirection] = useState("desc");
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(10);

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

  const formatPercentage = (value) => {
    if (!value && value !== 0) return "N/A";
    return `${value > 0 ? '+' : ''}${value.toFixed(1)}%`;
  };

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("desc");
    }
  };

  const getSortIcon = (field) => {
    if (sortField !== field) return null;
    return sortDirection === "asc" ? <ChevronUp size={14} /> : <ChevronDown size={14} />;
  };

  const getTrendIcon = (trend) => {
    if (trend > 0) return <TrendingUp className="trend-icon positive" size={14} />;
    if (trend < 0) return <TrendingDown className="trend-icon negative" size={14} />;
    return null;
  };

  const exportToCSV = () => {
    const headers = ["Sector", "Value", "Growth %", "Market Share %", "Products"];
    const csvData = sortedData.map(row => [
      row.name,
      row.value,
      row.growth || 0,
      row.market_share || 0,
      row.product_count || 0
    ]);
    
    const csvContent = [headers, ...csvData]
      .map(row => row.map(cell => `"${cell}"`).join(","))
      .join("\n");
    
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `sector-performance-${metric}-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <div className="table-container">
        <div className="table-header">
          <h3>Sector Performance</h3>
          <div className="table-actions">
            <button className="action-button" disabled>
              <Download size={16} />
              Export
            </button>
          </div>
        </div>
        <div className="table-loading">
          <div className="table-skeleton">
            {[1, 2, 3, 4, 5].map(i => (
              <div key={i} className="skeleton-row">
                <div className="skeleton-cell"></div>
                <div className="skeleton-cell"></div>
                <div className="skeleton-cell"></div>
                <div className="skeleton-cell"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!data || !Array.isArray(data) || data.length === 0) {
    return (
      <div className="table-container">
        <div className="table-header">
          <h3>Sector Performance</h3>
        </div>
        <div className="table-empty">
          <p>No sector data available.</p>
        </div>
      </div>
    );
  }

  // Sort data
  const sortedData = [...data].sort((a, b) => {
    let aValue = a[sortField];
    let bValue = b[sortField];
    
    // Map to actual field names from API
    if (sortField === 'name') {
      aValue = a.sector;
      bValue = b.sector;
    } else if (sortField === 'value') {
      aValue = metric === "revenue" ? a.total_revenue : a.total_units;
      bValue = metric === "revenue" ? b.total_revenue : b.total_units;
    } else if (sortField === 'growth') {
      aValue = a.average_growth_rate;
      bValue = b.average_growth_rate;
    } else if (sortField === 'market_share') {
      aValue = a.average_market_share;
      bValue = b.average_market_share;
    } else if (sortField === 'product_count') {
      aValue = a.product_count;
      bValue = b.product_count;
    }
    
    if (typeof aValue === "string") {
      aValue = aValue.toLowerCase();
      bValue = bValue.toLowerCase();
    }
    
    if (sortDirection === "asc") {
      return aValue > bValue ? 1 : -1;
    } else {
      return aValue < bValue ? 1 : -1;
    }
  });

  // Pagination
  const totalPages = Math.ceil(sortedData.length / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const paginatedData = sortedData.slice(startIndex, startIndex + pageSize);

  return (
    <div className="table-container">
      <div className="table-header">
        <h3>Sector Performance - {metric === "revenue" ? "Revenue" : "Units Sold"}</h3>
        <div className="table-actions">
          <button className="action-button" onClick={exportToCSV}>
            <Download size={16} />
            Export
          </button>
        </div>
      </div>
      
      <div className="table-content">
        <table className="data-table">
          <thead>
            <tr>
              <th 
                className={`sortable ${sortField === 'name' ? 'sorted' : ''}`}
                onClick={() => handleSort('name')}
              >
                Sector
                {getSortIcon('name')}
              </th>
              <th 
                className={`sortable ${sortField === 'value' ? 'sorted' : ''}`}
                onClick={() => handleSort('value')}
              >
                {metric === "revenue" ? "Revenue" : "Units"}
                {getSortIcon('value')}
              </th>
              <th 
                className={`sortable ${sortField === 'growth' ? 'sorted' : ''}`}
                onClick={() => handleSort('growth')}
              >
                Growth
                {getSortIcon('growth')}
              </th>
              <th 
                className={`sortable ${sortField === 'market_share' ? 'sorted' : ''}`}
                onClick={() => handleSort('market_share')}
              >
                Market Share
                {getSortIcon('market_share')}
              </th>
              <th 
                className={`sortable ${sortField === 'product_count' ? 'sorted' : ''}`}
                onClick={() => handleSort('product_count')}
              >
                Products
                {getSortIcon('product_count')}
              </th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((row, index) => (
              <tr key={row.sector || index}>
                <td className="sector-name">
                  <strong>{row.sector}</strong>
                </td>
                <td className="value-cell">
                  {formatValue(metric === "revenue" ? row.total_revenue : row.total_units)}
                </td>
                <td className="growth-cell">
                  <div className="growth-indicator">
                    {getTrendIcon(row.average_growth_rate)}
                    <span className={row.average_growth_rate >= 0 ? 'positive' : 'negative'}>
                      {formatPercentage(row.average_growth_rate)}
                    </span>
                  </div>
                </td>
                <td>
                  {formatPercentage(row.average_market_share)}
                </td>
                <td>
                  {row.product_count || 0}
                </td>
                <td>
                  <button
                    className="action-button small"
                    onClick={() => onSectorSelect(row.sector)}
                    title="View sector details"
                  >
                    <Eye size={14} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {totalPages > 1 && (
        <div className="table-pagination">
          <button
            className="pagination-button"
            onClick={() => setCurrentPage(currentPage - 1)}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          
          <span className="pagination-info">
            Page {currentPage} of {totalPages} ({sortedData.length} sectors)
          </span>
          
          <button
            className="pagination-button"
            onClick={() => setCurrentPage(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default SectorTable;
