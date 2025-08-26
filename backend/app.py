from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Load data from JSON file
def load_data():
    try:
        with open('data/companies.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to empty structure if file doesn't exist
        return {"companies": []}

# API Routes
@app.route('/api/companies', methods=['GET'])
def get_companies():
    """Get all companies with their products"""
    data = load_data()
    return jsonify(data)

@app.route('/api/companies/<company_name>', methods=['GET'])
def get_company(company_name):
    """Get a specific company and its products"""
    data = load_data()
    company = next((c for c in data.get('companies', []) if c['company'].lower() == company_name.lower()), None)
    
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    
    return jsonify(company)

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products across all companies with optional filtering"""
    data = load_data()
    all_products = []
    
    # Flatten all products from all companies
    for company in data.get('companies', []):
        for product in company.get('products', []):
            product_with_company = product.copy()
            product_with_company['company'] = company['company']
            product_with_company['parentCompany'] = company.get('parentCompany')
            all_products.append(product_with_company)
    
    # Apply filters
    search = request.args.get('search', '').lower()
    category = request.args.get('category', '').lower()
    target_audience = request.args.get('audience', '').lower()
    
    filtered_products = all_products
    
    if search:
        filtered_products = [
            p for p in filtered_products
            if (search in p.get('name', '').lower() or
                search in p.get('description', '').lower() or
                any(search in feature.lower() for feature in p.get('features', [])) or
                any(search in audience.lower() for audience in p.get('targetAudience', [])))
        ]
    
    if category:
        filtered_products = [
            p for p in filtered_products
            if category in p.get('category', '').lower()
        ]
    
    if target_audience:
        filtered_products = [
            p for p in filtered_products
            if any(target_audience in audience.lower() for audience in p.get('targetAudience', []))
        ]
    
    return jsonify({
        'products': filtered_products,
        'total': len(filtered_products)
    })

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    data = load_data()
    
    for company in data.get('companies', []):
        for product in company.get('products', []):
            if product.get('id') == product_id:
                product_with_company = product.copy()
                product_with_company['company'] = company['company']
                product_with_company['parentCompany'] = company.get('parentCompany')
                return jsonify(product_with_company)
    
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    data = load_data()
    categories = set()
    
    for company in data.get('companies', []):
        for product in company.get('products', []):
            if product.get('category'):
                categories.add(product['category'])
    
    return jsonify(sorted(list(categories)))

@app.route('/api/audiences', methods=['GET'])
def get_audiences():
    """Get all unique target audiences"""
    data = load_data()
    audiences = set()
    
    for company in data.get('companies', []):
        for product in company.get('products', []):
            for audience in product.get('targetAudience', []):
                audiences.add(audience)
    
    return jsonify(sorted(list(audiences)))

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Catalog API is running'})

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
