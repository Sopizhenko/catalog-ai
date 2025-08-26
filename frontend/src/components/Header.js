import React from 'react';
import { Search } from 'lucide-react';

const Header = ({ onSearch, searchTerm }) => {
  const handleSearchChange = (e) => {
    onSearch(e.target.value);
  };

  return (
    <header className="header">
      <div>
        <h1>Catalog AI</h1>
        <div className="subtitle">Software Product Catalog</div>
        <div className="search-container">
          <input
            type="text"
            className="search-bar"
            placeholder="Search products, features, or target audience..."
            value={searchTerm}
            onChange={handleSearchChange}
          />
          <Search className="search-icon" size={20} />
        </div>
      </div>
    </header>
  );
};

export default Header;
