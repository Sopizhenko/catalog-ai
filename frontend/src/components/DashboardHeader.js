import React from "react";
import { RefreshCw, Clock, ToggleLeft, ToggleRight } from "lucide-react";

const DashboardHeader = ({
  title,
  subtitle,
  lastUpdated,
  autoRefresh,
  onAutoRefreshToggle,
  onRefresh,
  loading
}) => {
  const formatLastUpdated = (date) => {
    if (!date) return "Never";
    
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins} min ago`;
    
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    
    return date.toLocaleDateString();
  };

  return (
    <div className="dashboard-header">
      <div className="dashboard-header-content">
        <div className="dashboard-title-section">
          <h1 className="dashboard-title">{title}</h1>
          {subtitle && <p className="dashboard-subtitle">{subtitle}</p>}
        </div>

        <div className="dashboard-controls">
          {/* Last Updated Display */}
          <div className="last-updated">
            <Clock size={16} />
            <span>Updated {formatLastUpdated(lastUpdated)}</span>
          </div>

          {/* Auto Refresh Toggle */}
          <div className="auto-refresh-control">
            <button
              className={`auto-refresh-toggle ${autoRefresh ? 'active' : ''}`}
              onClick={onAutoRefreshToggle}
              title={autoRefresh ? "Disable auto-refresh" : "Enable auto-refresh"}
            >
              {autoRefresh ? <ToggleRight size={20} /> : <ToggleLeft size={20} />}
              <span>Auto Refresh</span>
            </button>
          </div>

          {/* Manual Refresh Button */}
          <button
            className={`refresh-button ${loading ? 'loading' : ''}`}
            onClick={onRefresh}
            disabled={loading}
            title="Refresh data"
          >
            <RefreshCw size={16} className={loading ? 'spinning' : ''} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Progress indicator for loading */}
      {loading && (
        <div className="loading-progress">
          <div className="progress-bar">
            <div className="progress-fill"></div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DashboardHeader;
