import React from "react";

const DashboardLayout = ({ children, filters }) => {
  return (
    <div className="dashboard-layout">
      {filters && (
        <div className="dashboard-filters-container">
          {filters}
        </div>
      )}
      <div className="dashboard-content">
        {children}
      </div>
    </div>
  );
};

export default DashboardLayout;
