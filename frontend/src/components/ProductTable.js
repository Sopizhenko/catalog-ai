import React, { useState } from "react";
import { 
  ChevronDown, 
  ChevronUp, 
  TrendingUp, 
  TrendingDown, 
  Download, 
  Search,
  ExternalLink
} from "lucide-react";

const ProductTable = ({ data, loading, metric }) => {
  const [sortField, setSortField] = useState("value");
  const [sortDirection, setSortDirection] = useState("desc");
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize] = useState(10);
  const [searchTerm, setSearchTerm] = useState("");

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
    const headers = ["Product", "Company", "Sector", "Value", "Growth %", "Rank"];
    const csvData = filteredAndSortedData.map(row => [
      row.name,
      row.company,
      row.sector,
      row.value,
      row.growth || 0,
      row.rank || 0
    ]);
    
    const csvContent = [headers, ...csvData]
      .map(row => row.map(cell => `"${cell}"`).join(","))
      .join("\n");
    
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `product-performance-${metric}-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  if (loading) {
    return (
      <div className="table-container">
        <div className="table-header">
          <h3>Product Performance</h3>
          <div className="table-actions">
            <div className="search-box">
              <Search size={16} />
              <input type="text" placeholder="Search products..." disabled />
            </div>
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
          <h3>Product Performance</h3>
        </div>
        <div className="table-empty">
          <p>No product data available.</p>
        </div>
      </div>
    );
  }

  // Filter data based on search
  const filteredData = data.filter(item =>
    (item.product_id || "").toLowerCase().includes(searchTerm.toLowerCase()) ||
    (item.company || "").toLowerCase().includes(searchTerm.toLowerCase()) ||
    (item.sectors?.[0] || "").toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Sort data
  const filteredAndSortedData = [...filteredData].sort((a, b) => {
    let aValue = a[sortField];
    let bValue = b[sortField];
    
    // Map to actual field names from API
    if (sortField === 'name') {
      aValue = a.product_id;
      bValue = b.product_id;
    } else if (sortField === 'value') {
      aValue = metric === "revenue" ? a.total_revenue : a.total_units;
      bValue = metric === "revenue" ? b.total_revenue : b.total_units;
    } else if (sortField === 'growth') {
      aValue = a.average_growth_rate;
      bValue = b.average_growth_rate;
    } else if (sortField === 'sector') {
      aValue = a.sectors?.[0] || "";
      bValue = b.sectors?.[0] || "";
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

  // Add ranking
  const rankedData = filteredAndSortedData.map((item, index) => ({
    ...item,
    value: item[metric === "revenue" ? "total_revenue" : "total_units"] || 0,
    rank: index + 1
  }));

  // Pagination
  const totalPages = Math.ceil(rankedData.length / pageSize);
  const startIndex = (currentPage - 1) * pageSize;
  const paginatedData = rankedData.slice(startIndex, startIndex + pageSize);

  return (
    <div className="table-container">
      <div className="table-header">
        <h3>Product Performance - {metric === "revenue" ? "Revenue" : "Units Sold"}</h3>
        <div className="table-actions">
          <div className="search-box">
            <Search size={16} />
            <input
              type="text"
              placeholder="Search products, companies, sectors..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
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
                className={`sortable ${sortField === 'rank' ? 'sorted' : ''}`}
                onClick={() => handleSort('rank')}
              >
                Rank
                {getSortIcon('rank')}
              </th>
              <th 
                className={`sortable ${sortField === 'name' ? 'sorted' : ''}`}
                onClick={() => handleSort('name')}
              >
                Product
                {getSortIcon('name')}
              </th>
              <th 
                className={`sortable ${sortField === 'company' ? 'sorted' : ''}`}
                onClick={() => handleSort('company')}
              >
                Company
                {getSortIcon('company')}
              </th>
              <th 
                className={`sortable ${sortField === 'sector' ? 'sorted' : ''}`}
                onClick={() => handleSort('sector')}
              >
                Sector
                {getSortIcon('sector')}
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
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((row, index) => (
              <tr key={row.product_id || `${row.product_id}-${index}`}>
                <td className="rank-cell">
                  <span className={`rank-badge ${row.rank <= 3 ? 'top-rank' : ''}`}>
                    #{row.rank}
                  </span>
                </td>
                <td className="product-name">
                  <strong>{row.product_id}</strong>
                </td>
                <td className="company-name">
                  {row.company}
                </td>
                <td className="sector-tag">
                  <span className="sector-badge">{row.sectors?.[0] || 'N/A'}</span>
                </td>
                <td className="value-cell">
                  {formatValue(row.value)}
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
                  <button
                    className="action-button small"
                    onClick={() => {
                      // Navigate to product details
                      window.open(`/product/${row.product_id}`, '_blank');
                    }}
                    title="View product details"
                  >
                    <ExternalLink size={14} />
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
            Page {currentPage} of {totalPages} ({rankedData.length} products)
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

export default ProductTable;
