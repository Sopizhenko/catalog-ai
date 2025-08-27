from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from admin_db import admin_db
from admin_api import create_admin_app
from admin_dashboard import create_dashboard_app

app = Flask(__name__)
CORS(app)

def load_data():
    """Load data from JSON file"""
    try:
        with open('data/companies.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"companies": []}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Catalog API is running"})

@app.route('/api/companies', methods=['GET'])
def get_companies():
    """Get all companies (JSON + admin)"""
    try:
        # Get combined data from JSON and admin database
        combined_data = admin_db.get_combined_data()
        return jsonify(combined_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/companies/<company_name>', methods=['GET'])
def get_company(company_name):
    """Get a specific company by name"""
    try:
        # First check JSON data
        json_data = load_data()
        for company in json_data.get('companies', []):
            if company['company'].lower() == company_name.lower():
                return jsonify(company)
        
        # Then check admin database
        admin_companies = admin_db.get_all_companies()
        for company in admin_companies:
            if company['company'].lower() == company_name.lower():
                # Add products to the company data
                company_with_products = company.copy()
                company_with_products['products'] = admin_db.get_products_by_company(company['id'])
                return jsonify(company_with_products)
        
        return jsonify({"error": "Company not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    try:
        # Get search parameters
        search = request.args.get('search', '').lower()
        category = request.args.get('category', '').lower()
        
        # Get combined data
        combined_data = admin_db.get_combined_data()
        all_products = []
        
        # Process each company's products
        for company in combined_data.get('companies', []):
            company_name = company.get('company', '')
            company_products = company.get('products', [])
            
            for product in company_products:
                # Add company context to product
                product_with_company = product.copy()
                product_with_company['company'] = company_name
                product_with_company['parentCompany'] = company.get('parentCompany', '')
                product_with_company['industry'] = company.get('industry', '')
                product_with_company['source'] = company.get('source', 'unknown')
                
                # Apply search filter
                if search:
                    searchable_text = (
                        product.get('name', '') + ' ' +
                        product.get('description', '') + ' ' +
                        ' '.join(product.get('features', [])) + ' ' +
                        ' '.join(product.get('targetAudience', []))
                    ).lower()
                    if search not in searchable_text:
                        continue
                
                # Apply category filter
                if category and category != 'all':
                    if category not in product.get('category', '').lower():
                        continue
                
                all_products.append(product_with_company)
        
        return jsonify({"products": all_products})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        # Check admin database first
        product = admin_db.get_product(product_id)
        if product:
            # Add company context
            company = admin_db.get_company(product['company_id'])
            if company:
                product_with_company = product.copy()
                product_with_company['company'] = company['company']
                product_with_company['parentCompany'] = company.get('parentCompany', '')
                product_with_company['industry'] = company.get('industry', '')
                return jsonify(product_with_company)
        
        # If not found in admin, check JSON data
        json_data = load_data()
        for company in json_data.get('companies', []):
            for product in company.get('products', []):
                if product.get('id') == product_id:
                    product_with_company = product.copy()
                    product_with_company['company'] = company['company']
                    product_with_company['parentCompany'] = company.get('parentCompany', '')
                    product_with_company['industry'] = company.get('industry', '')
                    return jsonify(product_with_company)
        
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    try:
        combined_data = admin_db.get_combined_data()
        categories = set()
        
        for company in combined_data.get('companies', []):
            for product in company.get('products', []):
                if 'category' in product:
                    categories.add(product['category'])
        
        return jsonify({"categories": sorted(list(categories))})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/audiences', methods=['GET'])
def get_audiences():
    """Get all unique target audiences"""
    try:
        combined_data = admin_db.get_combined_data()
        audiences = set()
        
        for company in combined_data.get('companies', []):
            for product in company.get('products', []):
                if 'targetAudience' in product:
                    for audience in product['targetAudience']:
                        audiences.add(audience)
        
        return jsonify({"audiences": sorted(list(audiences))})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Mount admin apps
admin_app = create_admin_app()
dashboard_app = create_dashboard_app()

app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(dashboard_app, url_prefix='/admin-dashboard')

if __name__ == '__main__':
    print("🚀 Starting Catalog API with Admin Panel...")
    print("📊 Main API: http://localhost:5000/api")
    print("🔧 Admin Dashboard: http://localhost:5000/admin-dashboard")
    print("📋 Secret Admin URLs:")
    print("   - Dashboard: http://localhost:5000/admin-dashboard")
    print("   - Companies: http://localhost:5000/admin/companies")
    print("   - Company Products: http://localhost:5000/admin/company/{company_id}/products")
    app.run(debug=True, host='0.0.0.0', port=5000)
