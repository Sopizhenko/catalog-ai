import React, { useState } from "react";
import { Calendar, Filter, MapPin, DollarSign, Package } from "lucide-react";

const DashboardFilters = ({ filters, onFilterChange, sectors }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const periodOptions = [
    { value: "1month", label: "Last Month" },
    { value: "3months", label: "Last 3 Months" },
    { value: "6months", label: "Last 6 Months" },
    { value: "12months", label: "Last 12 Months" },
    { value: "24months", label: "Last 2 Years" },
    { value: "custom", label: "Custom Range" }
  ];

  const regionOptions = [
    { value: "all", label: "All Regions" },
    { value: "north_america", label: "North America" },
    { value: "europe", label: "Europe" },
    { value: "asia_pacific", label: "Asia Pacific" },
    { value: "latin_america", label: "Latin America" },
    { value: "middle_east_africa", label: "Middle East & Africa" }
  ];

  const metricOptions = [
    { value: "revenue", label: "Revenue", icon: DollarSign },
    { value: "units", label: "Units Sold", icon: Package }
  ];

  const handleFilterUpdate = (key, value) => {
    onFilterChange({ [key]: value });
  };

  const handleDateRangeChange = (startDate, endDate) => {
    onFilterChange({
      period: "custom",
      dateRange: { 
        start: startDate || "", 
        end: endDate || "" 
      }
    });
  };

  const resetFilters = () => {
    onFilterChange({
      period: "12months",
      sector: "all",
      region: "all",
      dateRange: null,
      metric: "revenue"
    });
  };

  const getActiveFilterCount = () => {
    let count = 0;
    if (filters.sector !== "all") count++;
    if (filters.region !== "all") count++;
    if (filters.period === "custom" && filters.dateRange) count++;
    return count;
  };

  return (
    <div className="dashboard-filters">
      <div className="filters-header">
        <div className="filters-title">
          <Filter size={18} />
          <span>Filters</span>
          {getActiveFilterCount() > 0 && (
            <span className="active-filters-count">{getActiveFilterCount()}</span>
          )}
        </div>
        
        <div className="filters-actions">
          <button 
            className="expand-toggle"
            onClick={() => setIsExpanded(!isExpanded)}
          >
            {isExpanded ? "Less" : "More"} Filters
          </button>
          
          {getActiveFilterCount() > 0 && (
            <button className="reset-filters" onClick={resetFilters}>
              Reset
            </button>
          )}
        </div>
      </div>

      <div className={`filters-content ${isExpanded ? 'expanded' : ''}`}>
        {/* Primary Filters - Always Visible */}
        <div className="primary-filters">
          {/* Metric Selection */}
          <div className="filter-group metric-filter">
            <div className="metric-toggle">
              {metricOptions.map(option => {
                const IconComponent = option.icon;
                return (
                  <button
                    key={option.value}
                    className={`metric-option ${(filters.metric || "revenue") === option.value ? 'active' : ''}`}
                    onClick={() => handleFilterUpdate('metric', option.value)}
                  >
                    <IconComponent size={16} />
                    <span>{option.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Period Selection */}
          <div className="filter-group">
            <label className="filter-label">
              <Calendar size={16} />
              Time Period
            </label>
            <select
              value={filters.period || "12months"}
              onChange={(e) => handleFilterUpdate('period', e.target.value)}
              className="filter-select"
            >
              {periodOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Sector Selection */}
          <div className="filter-group">
            <label className="filter-label">
              <Filter size={16} />
              Sector
            </label>
            <select
              value={filters.sector || "all"}
              onChange={(e) => handleFilterUpdate('sector', e.target.value)}
              className="filter-select"
            >
              <option key="all-sectors" value="all">All Sectors</option>
              {Array.isArray(sectors) && sectors.map((sector, index) => (
                <option key={sector.sector || `sector-${index}`} value={sector.sector}>
                  {sector.sector} ({sector.product_count})
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Secondary Filters - Expandable */}
        {isExpanded && (
          <div className="secondary-filters">
            {/* Region Selection */}
            <div className="filter-group">
              <label className="filter-label">
                <MapPin size={16} />
                Region
              </label>
              <select
                value={filters.region || "all"}
                onChange={(e) => handleFilterUpdate('region', e.target.value)}
                className="filter-select"
              >
                {regionOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Custom Date Range */}
            {filters.period === "custom" && (
              <div className="filter-group date-range-group">
                <label className="filter-label">Custom Date Range</label>
                <div className="date-range-inputs">
                  <input
                    type="date"
                    value={filters.dateRange?.start || ""}
                    onChange={(e) => handleDateRangeChange(e.target.value, filters.dateRange?.end || "")}
                    className="date-input"
                  />
                  <span>to</span>
                  <input
                    type="date"
                    value={filters.dateRange?.end || ""}
                    onChange={(e) => handleDateRangeChange(filters.dateRange?.start || "", e.target.value)}
                    className="date-input"
                  />
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardFilters;
