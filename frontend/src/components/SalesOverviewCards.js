import React from "react";
import { TrendingUp, TrendingDown, DollarSign, Package, Target, Award } from "lucide-react";

const SalesOverviewCards = ({ data, loading, metric }) => {
  const formatValue = (value, type = "currency") => {
    if (!value && value !== 0) return "N/A";
    
    if (type === "currency") {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value);
    }
    
    if (type === "number") {
      return new Intl.NumberFormat('en-US').format(value);
    }
    
    if (type === "percentage") {
      return `${value > 0 ? '+' : ''}${value.toFixed(1)}%`;
    }
    
    return value;
  };

  const getTrendIcon = (trend) => {
    if (trend > 0) return <TrendingUp className="trend-icon positive" size={16} />;
    if (trend < 0) return <TrendingDown className="trend-icon negative" size={16} />;
    return null;
  };

  const cards = [
    {
      id: "total-revenue",
      title: metric === "revenue" ? "Total Revenue" : "Total Units Sold",
      value: metric === "revenue" ? data.total_revenue : data.total_units,
      trend: metric === "revenue" ? data.revenue_growth : data.units_growth,
      icon: metric === "revenue" ? DollarSign : Package,
      type: metric === "revenue" ? "currency" : "number",
      description: "vs. previous period"
    },
    {
      id: "growth-rate",
      title: "Growth Rate",
      value: metric === "revenue" ? data.revenue_growth : data.units_growth,
      trend: data.growth_acceleration,
      icon: TrendingUp,
      type: "percentage",
      description: "period over period"
    },
    {
      id: "top-sector",
      title: "Top Performing Sector",
      value: data.top_sector?.name || "N/A",
      trend: data.top_sector?.growth,
      icon: Target,
      type: "text",
      description: data.top_sector ? formatValue(data.top_sector.value, metric === "revenue" ? "currency" : "number") : "No data"
    },
    {
      id: "best-product",
      title: "Best Product",
      value: data.best_product?.name || "N/A",
      trend: data.best_product?.growth,
      icon: Award,
      type: "text",
      description: data.best_product ? formatValue(data.best_product.value, metric === "revenue" ? "currency" : "number") : "No data"
    }
  ];

  if (loading) {
    return (
      <div className="overview-cards">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="overview-card loading">
            <div className="card-skeleton">
              <div className="skeleton-icon"></div>
              <div className="skeleton-content">
                <div className="skeleton-line short"></div>
                <div className="skeleton-line long"></div>
                <div className="skeleton-line medium"></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="overview-cards">
      {cards.map(card => {
        const IconComponent = card.icon;
        
        return (
          <div key={card.id} className="overview-card">
            <div className="card-header">
              <div className="card-icon">
                <IconComponent size={20} />
              </div>
              <h3 className="card-title">{card.title}</h3>
            </div>
            
            <div className="card-content">
              <div className="card-value">
                {card.type === "text" ? (
                  <span className="text-value">{card.value}</span>
                ) : (
                  <span className="numeric-value">
                    {formatValue(card.value, card.type)}
                  </span>
                )}
                
                {card.trend !== undefined && card.trend !== null && (
                  <div className={`trend-indicator ${card.trend > 0 ? 'positive' : card.trend < 0 ? 'negative' : 'neutral'}`}>
                    {getTrendIcon(card.trend)}
                    <span className="trend-value">
                      {formatValue(card.trend, "percentage")}
                    </span>
                  </div>
                )}
              </div>
              
              <p className="card-description">{card.description}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default SalesOverviewCards;
