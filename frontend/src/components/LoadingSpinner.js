import React from "react";
import { Loader2 } from "lucide-react";

const LoadingSpinner = () => {
  return (
    <div className="loading-spinner">
      <div className="spinner-container">
        <Loader2 size={48} className="spinner-icon" />
        <h3>Loading Catalog</h3>
        <p>Please wait while we load the catalog data...</p>
      </div>
    </div>
  );
};

export default LoadingSpinner;
