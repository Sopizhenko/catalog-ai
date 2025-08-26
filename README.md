# Catalog AI

A modern web application for browsing companies and their software products. Built with Python Flask backend and React frontend, featuring advanced search, filtering, and a beautiful user interface.

## 🚀 Features

- **Company & Product Browsing**: Browse through companies and their software products
- **Advanced Search**: Search products by name, features, target audience, or keywords
- **Smart Filtering**: Filter by category, target audience, and other criteria
- **Product Details**: Detailed product information with features, pricing, and integrations
- **Responsive Design**: Modern, mobile-friendly interface
- **Real-time Search**: Instant search results with live filtering

## 🛠️ Technology Stack

- **Backend**: Python Flask with RESTful API
- **Frontend**: React 18 with modern hooks and components
- **Styling**: Custom CSS with modern design patterns
- **Data**: JSON-based data storage with comprehensive product information
- **Icons**: Lucide React for beautiful icons

## 📋 Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** for version control

## 🚀 Quick Start

### Option 1: Automated Setup (Windows)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sopizhenko/catalog-ai.git
   cd catalog-ai
   ```

2. **Run setup scripts**
   ```bash
   # Setup backend
   setup-backend.bat
   
   # Setup frontend (in a new terminal)
   setup-frontend.bat
   
   # Start both servers
   start-app.bat
   ```

### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sopizhenko/catalog-ai.git
   cd catalog-ai
   ```

2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   pip install -r requirements.txt
   python app.py
   ```

3. **Setup Frontend** (in a new terminal)
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 🔧 Configuration

### Backend Configuration

The backend uses Flask with CORS enabled. Key configuration:

- **Port**: 5000 (default)
- **Data Source**: `backend/data/companies.json`
- **CORS**: Enabled for frontend communication

### Frontend Configuration

The frontend is configured to proxy API requests to the backend:

- **Development Port**: 3000
- **API Proxy**: Configured in `package.json`
- **Environment**: Development mode with hot reloading

## 📖 Usage

### Browsing Products

1. **Search**: Use the search bar to find products by name, features, or target audience
2. **Filter**: Click filter buttons to narrow down results by category or audience
3. **View Details**: Click on any product card to see detailed information
4. **Company Info**: Each product shows its company and parent company information

### API Endpoints

The backend provides the following REST API endpoints:

- `GET /api/companies` - Get all companies
- `GET /api/companies/{name}` - Get specific company
- `GET /api/products` - Get all products (with optional filters)
- `GET /api/products/{id}` - Get specific product
- `GET /api/categories` - Get all categories
- `GET /api/audiences` - Get all target audiences
- `GET /api/health` - Health check

### Example API Usage

```bash
# Get all products
curl http://localhost:5000/api/products

# Search products
curl "http://localhost:5000/api/products?search=pos"

# Filter by category
curl "http://localhost:5000/api/products?category=Point%20of%20Sale"
```

## 🏗️ Project Structure

```
catalog-ai/
├── backend/                 # Python Flask backend
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── data/
│       └── companies.json  # Product data
├── frontend/               # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   └── styles/         # CSS styles
│   └── package.json        # Node.js dependencies
├── setup-backend.bat       # Backend setup script
├── setup-frontend.bat      # Frontend setup script
├── start-app.bat          # Start both servers
└── README.md              # This file
```

## 🎯 Features Overview

### Backend Features
- **RESTful API**: Clean, well-documented API endpoints
- **Data Management**: JSON-based data storage with easy updates
- **CORS Support**: Cross-origin requests enabled for frontend
- **Error Handling**: Proper error responses and status codes
- **Health Check**: API health monitoring endpoint

### Frontend Features
- **Modern React**: Built with React 18 and modern hooks
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Search**: Instant search with debouncing
- **Advanced Filtering**: Multiple filter options for products
- **Product Details**: Comprehensive product information modal
- **Beautiful UI**: Modern design with smooth animations

## 🔧 Development

### Adding New Products

To add new products, edit `backend/data/companies.json`:

```json
{
  "company": "New Company",
  "parentCompany": "Parent Company",
  "description": "Company description",
  "products": [
    {
      "id": "unique-product-id",
      "name": "Product Name",
      "description": "Product description",
      "category": "Product Category",
      "features": ["Feature 1", "Feature 2"],
      "targetAudience": ["Audience 1", "Audience 2"],
      "pricing": {
        "model": "subscription",
        "startingPrice": 99,
        "currency": "EUR"
      }
    }
  ]
}
```

### Customizing the UI

- **Colors**: Modify CSS variables in `frontend/src/styles/index.css`
- **Components**: Add new components in `frontend/src/components/`
- **API**: Extend API endpoints in `backend/app.py`

## 🚀 Deployment

### Production Deployment

1. **Backend Deployment**
   ```bash
   cd backend
   pip install -r requirements.txt
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Frontend Deployment**
   ```bash
   cd frontend
   npm run build
   # Serve the build folder with a web server
   ```

### Docker Deployment

Create `Dockerfile` for containerized deployment:

```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write meaningful commit messages
- Test your changes before submitting

## 📝 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Confirma Software**: For providing the comprehensive product data
- **React Team**: For the amazing React framework
- **Flask Team**: For the lightweight Python web framework
- **Lucide**: For the beautiful icon library

## 📞 Support

For support and questions:

- **Issues**: Open an issue in the GitHub repository
- **Documentation**: Check this README and inline code comments
- **API**: Use the `/api/health` endpoint to check backend status

---

**Built with ❤️ for the software catalog community**
