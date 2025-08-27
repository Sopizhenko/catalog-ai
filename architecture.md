# Catalog AI - System Architecture

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Data Architecture](#data-architecture)
- [API Architecture](#api-architecture)
- [Component Architecture](#component-architecture)
- [Deployment Architecture](#deployment-architecture)
- [Security Architecture](#security-architecture)
- [Performance Architecture](#performance-architecture)

## Overview

Catalog AI is a modern web application designed for browsing companies and their software products. The system follows a clean separation of concerns with a Python Flask backend providing RESTful APIs and a React frontend delivering a responsive user experience.

### Key Architectural Principles
- **Separation of Concerns**: Clear separation between frontend and backend
- **RESTful Design**: API follows REST conventions
- **Responsive Design**: Mobile-first approach with cross-device compatibility
- **Scalability**: Modular design allowing for easy expansion
- **Maintainability**: Clean code structure with proper documentation

## System Architecture

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────┐
│                 │<===============>│                 │
│  React Frontend │                 │  Flask Backend  │
│   (Port 3000)   │                 │   (Port 5000)   │
│                 │                 │                 │
└─────────────────┘                 └─────────────────┘
         │                                   │
         │                                   │
         ▼                                   ▼
┌─────────────────┐                 ┌─────────────────┐
│   Browser DOM   │                 │   JSON Data     │
│   Components    │                 │     Storage     │
└─────────────────┘                 └─────────────────┘
```

### Technology Stack
- **Backend**: Python 3.8+, Flask 2.3+, Flask-CORS
- **Frontend**: React 18, JavaScript ES6+, CSS3
- **Data Storage**: JSON files
- **Icons**: Lucide React
- **Development**: Node.js 16+, npm, Python venv

## Backend Architecture

### Flask Application Structure
```
backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── venv/              # Python virtual environment
└── data/
    └── companies.json # Product and company data
```

### Core Backend Components

#### 1. Flask Application (`app.py`)
- **Purpose**: Main application entry point and API route definitions
- **Responsibilities**:
  - API endpoint routing
  - CORS configuration
  - Request/response handling
  - Data processing and filtering
  - Error handling

#### 2. Data Management
- **Storage**: JSON-based file system storage
- **Location**: `backend/data/companies.json`
- **Structure**: Hierarchical company and product data
- **Access Pattern**: File-based read operations

### API Layer Architecture

#### Request Flow
```
Client Request → Flask Router → Data Processor → JSON Response
      ↓               ↓              ↓              ↑
   Validation → Route Handler → Data Query → Response Format
```

#### Core API Endpoints
- **Companies**: `/api/companies`, `/api/companies/{name}`
- **Products**: `/api/products`, `/api/products/{id}`
- **Metadata**: `/api/categories`, `/api/audiences`
- **Health**: `/api/health`

## Frontend Architecture

### React Application Structure
```
frontend/src/
├── App.js              # Root application component
├── index.js           # Application entry point
├── components/        # React components
│   ├── CompanySelector.js
│   ├── Filters.js
│   ├── Header.js
│   ├── LoadingSpinner.js
│   ├── ProductCard.js
│   ├── ProductGrid.js
│   └── ProductModal.js
├── services/          # API communication
│   └── api.js
└── styles/            # CSS stylesheets
    └── index.css
```

### Component Hierarchy
```
App
├── Header
├── CompanySelector
├── Filters
├── ProductGrid
│   └── ProductCard (multiple)
├── ProductModal
└── LoadingSpinner
```

### State Management Architecture

#### Application State Flow
```
User Interaction → Component State → API Call → State Update → UI Re-render
      ↓                ↓              ↓           ↓            ↑
   Event Handler → useState Hook → API Service → setState → Component Update
```

#### Key State Components
- **Search State**: Search queries and filters
- **Product State**: Product data and loading states
- **UI State**: Modal visibility, loading indicators
- **Company State**: Selected company and company data

## Data Architecture

### Data Model Structure

#### Company Entity
```json
{
  "company": "string",           # Company name
  "parentCompany": "string",     # Parent organization
  "description": "string",       # Company description
  "products": [Product]          # Array of products
}
```

#### Product Entity
```json
{
  "id": "string",               # Unique identifier
  "name": "string",             # Product name
  "description": "string",      # Product description
  "category": "string",         # Product category
  "features": ["string"],       # Array of features
  "targetAudience": ["string"], # Array of audiences
  "pricing": {                  # Pricing information
    "model": "string",
    "startingPrice": number,
    "currency": "string"
  }
}
```

### Data Access Patterns
- **Read-Heavy**: Optimized for frequent read operations
- **File-Based**: JSON file storage for simplicity
- **In-Memory**: Data loaded into memory for fast access
- **Filtering**: Server-side filtering and search capabilities

## API Architecture

### RESTful Design Principles
- **Resource-Based URLs**: Clear resource identification
- **HTTP Methods**: Proper use of GET operations
- **Status Codes**: Appropriate HTTP status responses
- **JSON Format**: Consistent JSON request/response format

### API Contract

#### Request/Response Patterns
```http
GET /api/products?search=<term>&category=<cat>&audience=<aud>
Accept: application/json

HTTP/1.1 200 OK
Content-Type: application/json

{
  "products": [Product],
  "total": number,
  "filters": {
    "categories": [string],
    "audiences": [string]
  }
}
```

### Error Handling Architecture
- **Standard Error Format**: Consistent error response structure
- **HTTP Status Codes**: Proper status code usage
- **Error Messages**: User-friendly error descriptions
- **Logging**: Server-side error logging for debugging

## Component Architecture

### Frontend Component Design

#### Component Types
1. **Container Components**: Data fetching and state management
2. **Presentational Components**: UI rendering and user interactions
3. **Service Components**: API communication and data processing
4. **Utility Components**: Shared functionality and helpers

#### Component Communication Patterns
- **Props Down**: Data flows down through props
- **Events Up**: User interactions bubble up through callbacks
- **Context API**: Shared state when needed
- **Custom Hooks**: Reusable logic extraction

### Component Responsibilities

#### `App.js`
- Application initialization
- Global state management
- Route coordination
- Error boundary handling

#### `ProductGrid.js`
- Product list rendering
- Grid layout management
- Infinite scrolling (future)
- Loading state handling

#### `ProductModal.js`
- Detailed product display
- Modal state management
- User interaction handling
- Close/escape functionality

## Deployment Architecture

### Development Environment
```
Development Machine
├── Backend (localhost:5000)
│   ├── Flask Dev Server
│   ├── Python Virtual Environment
│   └── JSON Data Files
└── Frontend (localhost:3000)
    ├── React Dev Server
    ├── Hot Reload
    └── API Proxy to Backend
```

### Production Environment (Recommended)
```
Production Server
├── Web Server (nginx/Apache)
├── WSGI Server (Gunicorn)
│   └── Flask Application
├── Static File Serving
│   └── React Build Files
└── Process Management
    └── Systemd/Docker
```

### Containerization Architecture
```dockerfile
# Multi-stage Docker build
Frontend Build → Static Files
Backend Setup → Python Application
Runtime → Nginx + Gunicorn + Static Files
```

## Security Architecture

### Security Measures
- **CORS Configuration**: Proper cross-origin request handling
- **Input Validation**: Server-side input sanitization
- **Error Handling**: Secure error message handling
- **Dependencies**: Regular security updates

### Data Security
- **No Sensitive Data**: Public product catalog information
- **Read-Only Operations**: Limited to GET requests
- **No Authentication**: Current design is public access

## Performance Architecture

### Frontend Performance
- **Component Optimization**: React.memo for expensive components
- **Search Debouncing**: Reduced API call frequency
- **Lazy Loading**: Modal and detailed view loading
- **Bundle Optimization**: Code splitting and minification

### Backend Performance
- **In-Memory Caching**: Data loaded into memory
- **Efficient Filtering**: Optimized search algorithms
- **Response Compression**: Gzip compression for responses
- **Minimal Processing**: Lightweight request handling

### Scalability Considerations
- **Horizontal Scaling**: Multiple backend instances
- **Database Migration**: Future database integration
- **CDN Integration**: Static asset delivery
- **Load Balancing**: Request distribution

## Monitoring and Observability

### Health Monitoring
- **Health Endpoint**: `/api/health` for system monitoring
- **Error Logging**: Application error tracking
- **Performance Metrics**: Response time monitoring

### Development Tools
- **Hot Reload**: Frontend development efficiency
- **API Testing**: Manual endpoint testing
- **Browser DevTools**: Frontend debugging
- **Flask Debug Mode**: Backend debugging

## Future Architecture Considerations

### Planned Enhancements
- **Database Integration**: PostgreSQL/MongoDB migration
- **Authentication System**: User management and access control
- **Caching Layer**: Redis for improved performance
- **Search Enhancement**: Elasticsearch integration
- **Real-time Features**: WebSocket support
- **Mobile App**: React Native implementation

### Scalability Roadmap
1. **Database Migration**: Move from JSON to proper database
2. **Microservices**: Split into smaller services
3. **Container Orchestration**: Kubernetes deployment
4. **CI/CD Pipeline**: Automated testing and deployment
5. **Monitoring Stack**: Comprehensive observability

---

This architecture document serves as the foundation for all development decisions and should be referenced for any system modifications or enhancements. All changes should maintain consistency with the established architectural patterns and principles outlined above.
