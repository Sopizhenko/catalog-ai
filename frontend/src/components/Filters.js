import React from "react";
import {
  Filter,
  Package,
  Database,
  Users,
  Settings,
  BarChart3,
} from "lucide-react";
import { useScrollAnimation } from "../hooks/useScrollAnimation";

const Filters = ({ categories, selectedCategory, onCategoryFilter }) => {
  const [filtersRef, isFiltersVisible] = useScrollAnimation({
    threshold: 0.3,
    delay: 100,
  });

  const getCategoryIcon = (category) => {
    const categoryLower = category.toLowerCase();
    if (categoryLower.includes("erp") || categoryLower.includes("management"))
      return <Settings size={16} />;
    if (categoryLower.includes("database") || categoryLower.includes("data"))
      return <Database size={16} />;
    if (
      categoryLower.includes("analytics") ||
      categoryLower.includes("reporting")
    )
      return <BarChart3 size={16} />;
    if (categoryLower.includes("crm") || categoryLower.includes("customer"))
      return <Users size={16} />;
    return <Package size={16} />;
  };

  return (
    <div
      ref={filtersRef}
      className={`filters-container ${
        isFiltersVisible ? "animate-slide-up" : "animate-slide-down"
      }`}
    >
      <div className="filters-header">
        <Filter size={20} className="filters-icon" />
        <span className="filters-title">Filter by Category</span>
      </div>
      <div className="filters">
        <FilterButton
          category="all"
          icon={<Package size={16} />}
          label="All Products"
          isActive={selectedCategory === "all"}
          onClick={() => onCategoryFilter("all")}
          index={0}
        />

        {categories.map((category, index) => (
          <FilterButton
            key={category}
            category={category}
            icon={getCategoryIcon(category)}
            label={category}
            isActive={selectedCategory === category}
            onClick={() => onCategoryFilter(category)}
            index={index + 1}
          />
        ))}
      </div>
    </div>
  );
};

const FilterButton = ({ category, icon, label, isActive, onClick, index }) => {
  const [buttonRef, isVisible] = useScrollAnimation({
    threshold: 0.1,
    delay: index * 25, // Stagger animation by 25ms per button
    triggerOnce: true,
  });

  return (
    <button
      ref={buttonRef}
      className={`filter-btn ${isActive ? "active" : ""} ${
        isVisible ? "animate-fade-in" : "animate-fade-out"
      }`}
      onClick={onClick}
    >
      {icon}
      {label}
    </button>
  );
};

export default Filters;
