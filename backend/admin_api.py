import json
import os
from flask import Blueprint, render_template_string, request, jsonify
from admin_db import admin_db

def create_admin_app():
    admin_bp = Blueprint('admin', __name__)
    
    def load_json_company_products(company_id):
        """Load products for a JSON company from the companies.json file"""
        try:
            # Extract company name from the JSON company ID
            company_name = company_id.replace('json_', '').replace('_', ' ')
            
            json_path = os.path.join(os.path.dirname(__file__), 'data', 'companies.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                companies = data.get('companies', [])
                
                # Find the company by name
                for company in companies:
                    if company['company'].lower().replace(' ', '_') == company_name:
                        # Transform products to match the expected format
                        products = []
                        for product in company.get('products', []):
                            products.append({
                                'id': product.get('id', f"json_{product['name'].lower().replace(' ', '_')}"),
                                'name': product['name'],
                                'description': product.get('description', ''),
                                'category': product.get('category', ''),
                                'features': product.get('features', []),
                                'targetAudience': product.get('targetAudience', []),
                                'pricing': product.get('pricing', {}),
                                'version': product.get('version', ''),
                                'integrations': product.get('integrations', []),
                                'supportedPlatforms': product.get('supportedPlatforms', []),
                                'lastUpdated': product.get('lastUpdated', ''),
                                'source': 'json',
                                'readonly': True
                            })
                        return products
                return []
        except Exception as e:
            print(f"Error loading JSON company products: {e}")
            return []
    
    def load_json_company(company_id):
        """Load company data for a JSON company from the companies.json file"""
        try:
            # Extract company name from the JSON company ID
            company_name = company_id.replace('json_', '').replace('_', ' ')
            
            json_path = os.path.join(os.path.dirname(__file__), 'data', 'companies.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                companies = data.get('companies', [])
                
                # Find the company by name
                for company in companies:
                    if company['company'].lower().replace(' ', '_') == company_name:
                        # Extract tags from products
                        tags = set()
                        for product in company.get('products', []):
                            if 'category' in product:
                                tags.add(product['category'])
                        
                        return {
                            'id': company_id,
                            'company': company['company'],
                            'parentCompany': company.get('parentCompany', ''),
                            'description': company.get('description', ''),
                            'industry': company.get('industry', ''),
                            'tags': list(tags),
                            'source': 'json',
                            'readonly': True
                        }
                return None
        except Exception as e:
            print(f"Error loading JSON company: {e}")
            return None

    @admin_bp.route('/companies', methods=['GET'])
    def admin_companies_page():
        """Admin page for managing companies"""
        companies = admin_db.get_all_companies()
        existing_tags = admin_db.get_existing_tags()
        
        html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin - Manage Companies</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
                .header { background: #009607; color: white; padding: 20px; margin-bottom: 30px; border-radius: 8px; }
                .header h1 { margin: 0; }
                .form-section { background: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .form-section h2 { margin-bottom: 20px; color: #333; }
                .form-group { margin-bottom: 20px; }
                .form-group label { display: block; margin-bottom: 5px; font-weight: 600; color: #555; }
                .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 16px; }
                .form-group input:focus, .form-group textarea:focus, .form-group select:focus { outline: none; border-color: #009607; }
                .form-group textarea { height: 100px; resize: vertical; }
                .btn { background: #009607; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }
                .btn:hover { background: #008005; }
                .btn-secondary { background: #6c757d; }
                .btn-secondary:hover { background: #5a6268; }
                .btn-danger { background: #dc3545; }
                .btn-danger:hover { background: #c82333; }
                .table-section { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .table-section h2 { margin-bottom: 20px; color: #333; }
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #f8f9fa; font-weight: 600; color: #555; }
                tr:hover { background: #f8f9fa; }
                .actions { display: flex; gap: 10px; }
                .tag { background: #e9ecef; color: #495057; padding: 4px 8px; border-radius: 4px; font-size: 12px; margin: 2px; display: inline-block; }
                .company-link { color: #009607; text-decoration: none; font-weight: 600; }
                .company-link:hover { text-decoration: underline; }
                .alert { padding: 15px; border-radius: 6px; margin-bottom: 20px; }
                .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
                .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div style="display: flex; align-items: center; gap: 20px;">
                        <a href="/admin-dashboard" class="btn btn-secondary" style="text-decoration: none; display: flex; align-items: center; gap: 8px;">
                            ← Back to Dashboard
                        </a>
                        <h1>🔧 Admin Panel - Manage Companies</h1>
                    </div>
                </div>
                
                <div class="form-section">
                    <h2>➕ Add New Company</h2>
                    <form id="companyForm">
                        <div class="form-group">
                            <label for="company">Company Name *</label>
                            <input type="text" id="company" name="company" required>
                        </div>
                        <div class="form-group">
                            <label for="description">Description *</label>
                            <textarea id="description" name="description" required></textarea>
                        </div>
                        <div class="form-group">
                            <label for="industry">Industry</label>
                            <input type="text" id="industry" name="industry">
                        </div>
                        <div class="form-group">
                            <label for="tags">Tags</label>
                            <select id="tags" name="tags" multiple>
                                {% for tag in existing_tags %}
                                <option value="{{ tag }}">{{ tag }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        <button type="submit" class="btn">Add Company</button>
                    </form>
                </div>
                
                <div class="table-section">
                    <h2>📋 Companies List</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Company Name</th>
                                <th>Description</th>
                                <th>Industry</th>
                                <th>Tags</th>
                                <th>Products</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for company in companies %}
                            <tr>
                                <td>
                                    <a href="/admin/company/{{ company.id }}/products" class="company-link">
                                        {{ company.company }}
                                    </a>
                                </td>
                                <td>{{ company.description[:100] }}{% if company.description|length > 100 %}...{% endif %}</td>
                                <td>{{ company.industry or '-' }}</td>
                                <td>
                                    {% for tag in company.tags %}
                                    <span class="tag">{{ tag }}</span>
                                    {% endfor %}
                                </td>
                                <td>{{ company.products|length if company.products else 0 }}</td>
                                <td class="actions">
                                    <button class="btn btn-secondary" onclick="editCompany('{{ company.id }}')">Edit</button>
                                    <button class="btn btn-danger" onclick="deleteCompany('{{ company.id }}')">Delete</button>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <script>
                // Form submission
                document.getElementById('companyForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const formData = new FormData(e.target);
                    const tags = Array.from(document.getElementById('tags').selectedOptions).map(opt => opt.value);
                    
                    const data = {
                        company: formData.get('company'),
                        description: formData.get('description'),
                        industry: formData.get('industry'),
                        tags: tags
                    };
                    
                    try {
                        const response = await fetch('/admin/api/companies', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(data)
                        });
                        
                        if (response.ok) {
                            location.reload();
                        } else {
                            alert('Error adding company');
                        }
                    } catch (error) {
                        alert('Error adding company');
                    }
                });
                
                async function deleteCompany(companyId) {
                    if (!confirm('Are you sure you want to delete this company? This will also delete all its products.')) {
                        return;
                    }
                    
                    try {
                        const response = await fetch(`/admin/api/companies/${companyId}`, {
                            method: 'DELETE'
                        });
                        
                        if (response.ok) {
                            location.reload();
                        } else {
                            alert('Error deleting company');
                        }
                    } catch (error) {
                        alert('Error deleting company');
                    }
                }
                
                function editCompany(companyId) {
                    // TODO: Implement edit functionality
                    alert('Edit functionality coming soon!');
                }
            </script>
        </body>
        </html>
        '''
        
        return render_template_string(html, companies=companies, existing_tags=existing_tags)
    
    @admin_bp.route('/company/<company_id>/products', methods=['GET'])
    def admin_company_products_page(company_id):
        """Admin page for managing products of a specific company"""
        # Check if this is a JSON company
        if company_id.startswith('json_'):
            company = load_json_company(company_id)
            products = load_json_company_products(company_id)
        else:
            company = admin_db.get_company(company_id)
            products = admin_db.get_products_by_company(company_id)
        
        if not company:
            return "Company not found", 404
        
        existing_tags = admin_db.get_existing_tags()
        
        html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin - Manage Products for {{ company.company }}</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; }
                .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
                .header { text-align: center; margin-bottom: 30px; }
                .header h1 { font-size: 2.5rem; color: #2c3e50; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
                .back-links { display: flex; justify-content: center; gap: 20px; margin-bottom: 20px; }
                .back-links a { background: #6c757d; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; transition: all 0.3s ease; }
                .back-links a:hover { background: #5a6268; transform: translateY(-2px); }
                
                .company-info { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }
                .company-info h2 { color: #2c3e50; margin-bottom: 10px; }
                .source-indicator { display: inline-block; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 600; margin-left: 8px; }
                .source-json { background: #fff3e0; color: #f57c00; }
                .readonly-note { font-size: 0.9rem; color: #6c757d; font-style: italic; margin-top: 10px; }
                
                .add-button { background: #009607; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin-bottom: 20px; transition: all 0.3s ease; }
                .add-button:hover { background: #008005; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
                .add-button:disabled { background: #e9ecef; color: #6c757d; cursor: not-allowed; transform: none; box-shadow: none; }
                
                .products-table { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #f8f9fa; font-weight: 600; color: #555; }
                tr:hover { background: #f8f9fa; }
                .actions { display: flex; gap: 10px; }
                .tag { background: #e8f5e8; color: #009607; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; margin: 2px; display: inline-block; }
                .btn { padding: 8px 16px; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; }
                .btn-secondary { background: #6c757d; color: white; }
                .btn-danger { background: #dc3545; color: white; }
                .btn-disabled { background: #e9ecef; color: #6c757d; cursor: not-allowed; }
                
                /* Modal Styles */
                .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); overflow-y: auto; }
                .modal-content { background-color: white; margin: 20px auto; padding: 30px; border-radius: 15px; width: 90%; max-width: 600px; position: relative; max-height: calc(100vh - 40px); overflow-y: auto; }
                .close { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
                .close:hover { color: #000; }
                .form-group { margin-bottom: 20px; }
                .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #555; }
                .form-group input, .form-group textarea, .form-group select { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 6px; font-size: 16px; }
                .form-group input:focus, .form-group textarea:focus, .form-group select:focus { outline: none; border-color: #009607; }
                .form-group textarea { height: 100px; resize: vertical; }
                .modal-footer { text-align: right; margin-top: 20px; }
                .btn-primary { background: #009607; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }
                .btn-primary:hover { background: #008005; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📦 Products in {{ company.company }}</h1>
                </div>
                
                <div class="back-links">
                    <a href="/admin-dashboard">← Back to Dashboard</a>
                </div>
                
                <div class="company-info">
                    <h2>{{ company.company }}</h2>
                    <p><strong>Description:</strong> {{ company.description }}</p>
                    <p><strong>Industry:</strong> {{ company.industry or 'Not specified' }}</p>
                    <p><strong>Tags:</strong> 
                        {% for tag in company.tags %}
                        <span class="tag">{{ tag }}</span>
                        {% endfor %}
                    </p>
                    {% if company.source == 'json' %}
                    <span class="source-indicator source-json">JSON SOURCE</span>
                    <div class="readonly-note">This company and its products are read-only (loaded from companies.json)</div>
                    {% endif %}
                </div>
                
                <div class="products-table">
                    <button class="add-button" onclick="openAddProductModal()" {% if company.readonly %}disabled{% endif %}>
                        {% if company.readonly %}➕ Add New Product (Disabled for JSON companies){% else %}➕ Add New Product{% endif %}
                    </button>
                    
                    <table>
                        <thead>
                            <tr>
                                <th>Product Name</th>
                                <th>Description</th>
                                <th>Category</th>
                                <th>Features</th>
                                <th>Target Audience</th>
                                <th>Pricing</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for product in products %}
                            <tr>
                                <td>{{ product.name }}</td>
                                <td>{{ product.description[:100] }}{% if product.description|length > 100 %}...{% endif %}</td>
                                <td><span class="tag">{{ product.category }}</span></td>
                                <td>
                                    {% for feature in product.features %}
                                    <span class="tag">{{ feature }}</span>
                                    {% endfor %}
                                </td>
                                <td>
                                    {% for audience in product.targetAudience %}
                                    <span class="tag">{{ audience }}</span>
                                    {% endfor %}
                                </td>
                                <td>
                                    {% if product.pricing %}
                                        <strong>{{ product.pricing.model }}</strong><br>
                                        {% if product.pricing.startingPrice %}
                                        From {{ product.pricing.startingPrice }}{% if product.pricing.currency %} {{ product.pricing.currency }}{% endif %}
                                        {% endif %}
                                    {% else %}
                                        Not specified
                                    {% endif %}
                                </td>
                                <td class="actions">
                                    {% if not product.readonly %}
                                    <button class="btn btn-secondary" onclick="editProduct('{{ product.id }}')">Edit</button>
                                    <button class="btn btn-danger" onclick="deleteProduct('{{ product.id }}')">Delete</button>
                                    {% else %}
                                    <button class="btn btn-secondary btn-disabled" disabled title="JSON products cannot be edited">Edit</button>
                                    <button class="btn btn-danger btn-disabled" disabled title="JSON products cannot be deleted">Delete</button>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                            {% if products|length == 0 %}
                            <tr>
                                <td colspan="7" style="text-align: center; padding: 40px; color: #7f8c8d;">
                                    {% if company.readonly %}
                                    No products found for this company in the JSON file.
                                    {% else %}
                                    No products added yet. Click "Add New Product" to get started.
                                    {% endif %}
                                </td>
                            </tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- Add Product Modal -->
            <div id="addProductModal" class="modal">
                <div class="modal-content">
                    <span class="close" onclick="closeAddProductModal()">&times;</span>
                    <h2>➕ Add New Product</h2>
                    <form id="productForm">
                        <div class="form-group">
                            <label for="name">Product Name *</label>
                            <input type="text" id="name" name="name" required>
                        </div>
                        <div class="form-group">
                            <label for="description">Description *</label>
                            <textarea id="description" name="description" required></textarea>
                        </div>
                        <div class="form-group">
                            <label for="category">Category *</label>
                            <input type="text" id="category" name="category" required>
                        </div>
                        <div class="form-group">
                            <label for="features">Features (comma-separated)</label>
                            <input type="text" id="features" name="features" placeholder="feature1, feature2, feature3">
                        </div>
                        <div class="form-group">
                            <label for="targetAudience">Target Audience (comma-separated)</label>
                            <input type="text" id="targetAudience" name="targetAudience" placeholder="audience1, audience2">
                        </div>
                        <div class="form-group">
                            <label for="pricingModel">Pricing Model</label>
                            <select id="pricingModel" name="pricingModel">
                                <option value="subscription">Subscription</option>
                                <option value="one-time">One-time</option>
                                <option value="freemium">Freemium</option>
                                <option value="custom">Custom</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="startingPrice">Starting Price</label>
                            <input type="number" id="startingPrice" name="startingPrice" min="0" step="0.01">
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" onclick="closeAddProductModal()">Cancel</button>
                            <button type="submit" class="btn btn-primary">Add Product</button>
                        </div>
                    </form>
                </div>
            </div>
            
            <script>
                // Modal functions
                function openAddProductModal() {
                    document.getElementById('addProductModal').style.display = 'block';
                }
                
                function closeAddProductModal() {
                    document.getElementById('addProductModal').style.display = 'none';
                    document.getElementById('productForm').reset();
                }
                
                // Close modal when clicking outside
                window.onclick = function(event) {
                    const modal = document.getElementById('addProductModal');
                    if (event.target == modal) {
                        closeAddProductModal();
                    }
                }
                
                // Form submission
                document.getElementById('productForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const formData = new FormData(e.target);
                    const features = formData.get('features') ? formData.get('features').split(',').map(f => f.trim()) : [];
                    const targetAudience = formData.get('targetAudience') ? formData.get('targetAudience').split(',').map(a => a.trim()) : [];
                    
                    const data = {
                        company_id: '{{ company.id }}',
                        company_name: '{{ company.company }}',
                        name: formData.get('name'),
                        description: formData.get('description'),
                        category: formData.get('category'),
                        features: features,
                        targetAudience: targetAudience,
                        pricing: {
                            model: formData.get('pricingModel'),
                            startingPrice: parseFloat(formData.get('startingPrice')) || 0
                        }
                    };
                    
                    try {
                        const response = await fetch('/admin/api/products', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(data)
                        });
                        
                        if (response.ok) {
                            location.reload();
                        } else {
                            alert('Error adding product');
                        }
                    } catch (error) {
                        alert('Error adding product');
                    }
                });
                
                async function deleteProduct(productId) {
                    if (!confirm('Are you sure you want to delete this product?')) {
                        return;
                    }
                    
                    try {
                        const response = await fetch(`/admin/api/products/${productId}`, {
                            method: 'DELETE'
                        });
                        
                        if (response.ok) {
                            location.reload();
                        } else {
                            alert('Error deleting product');
                        }
                    } catch (error) {
                        alert('Error deleting product');
                    }
                }
                
                function editProduct(productId) {
                    // TODO: Implement edit functionality
                    alert('Edit functionality coming soon!');
                }
            </script>
        </body>
        </html>
        '''
        
        return render_template_string(html, company=company, products=products, existing_tags=existing_tags)
    
    # API endpoints
    @admin_bp.route('/api/companies', methods=['POST'])
    def api_add_company():
        """API endpoint to add a new company"""
        try:
            data = request.get_json()
            company_id = admin_db.add_company(data)
            return jsonify({'success': True, 'company_id': company_id}), 201
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    @admin_bp.route('/api/companies/<company_id>', methods=['DELETE'])
    def api_delete_company(company_id):
        """API endpoint to delete a company"""
        try:
            success = admin_db.delete_company(company_id)
            if success:
                return jsonify({'success': True}), 200
            else:
                return jsonify({'success': False, 'error': 'Company not found'}), 404
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    @admin_bp.route('/api/products', methods=['POST'])
    def api_add_product():
        """API endpoint to add a new product"""
        try:
            data = request.get_json()
            product_id = admin_db.add_product(data)
            return jsonify({'success': True, 'product_id': product_id}), 201
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    @admin_bp.route('/api/products/<product_id>', methods=['DELETE'])
    def api_delete_product(product_id):
        """API endpoint to delete a product"""
        try:
            success = admin_db.delete_product(product_id)
            if success:
                return jsonify({'success': True}), 200
            else:
                return jsonify({'success': False, 'error': 'Product not found'}), 404
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    @admin_bp.route('/api/tags', methods=['GET'])
    def api_get_tags():
        """API endpoint to get all available tags"""
        try:
            tags = admin_db.get_existing_tags()
            return jsonify({'success': True, 'tags': tags}), 200
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400
    
    return admin_bp
