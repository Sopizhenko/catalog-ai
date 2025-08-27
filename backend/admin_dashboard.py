from flask import Blueprint, render_template_string
from admin_db import admin_db
import json
import os

def create_dashboard_app():
    dashboard_bp = Blueprint('dashboard', __name__)
    
    def load_json_companies():
        """Load companies from the JSON file"""
        try:
            json_path = os.path.join(os.path.dirname(__file__), 'data', 'companies.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                companies = data.get('companies', [])
                
                # Transform JSON companies to match the expected format
                json_companies = []
                for company in companies:
                    # Extract tags from products
                    tags = set()
                    for product in company.get('products', []):
                        if 'category' in product:
                            tags.add(product['category'])
                    
                    json_companies.append({
                        'id': f"json_{company['company'].lower().replace(' ', '_')}",
                        'company': company['company'],
                        'parentCompany': company.get('parentCompany', ''),
                        'description': company.get('description', ''),
                        'industry': company.get('industry', ''),
                        'tags': list(tags),
                        'source': 'json',
                        'readonly': True
                    })
                return json_companies
        except Exception as e:
            print(f"Error loading JSON companies: {e}")
            return []
    
    @dashboard_bp.route('/', methods=['GET'])
    def admin_dashboard():
        """Main admin dashboard - shows companies table with add modal"""
        # Get companies from database
        db_companies = admin_db.get_all_companies()
        
        # Add source and readonly flags to database companies
        for company in db_companies:
            company['source'] = 'database'
            company['readonly'] = False
        
        # Get companies from JSON file
        json_companies = load_json_companies()
        
        # Combine both lists, with database companies first
        all_companies = db_companies + json_companies
        
        existing_tags = admin_db.get_existing_tags()
        
        html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin Dashboard - Catalog System</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; }
                .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
                .header { text-align: center; margin-bottom: 30px; }
                .header h1 { font-size: 2.5rem; color: #2c3e50; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
                .header p { font-size: 1.1rem; color: #7f8c8d; }
                .add-button { background: #009607; color: white; padding: 15px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; margin-bottom: 20px; transition: all 0.3s ease; }
                .add-button:hover { background: #008005; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
                .companies-table { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
                .companies-table h2 { font-size: 1.8rem; color: #2c3e50; margin-bottom: 25px; text-align: center; }
                .source-indicator { display: inline-block; padding: 4px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 600; margin-left: 8px; }
                .source-database { background: #e3f2fd; color: #1976d2; }
                .source-json { background: #fff3e0; color: #f57c00; }
                
                /* Table styling with proper alignment */
                table { width: 100%; border-collapse: collapse; }
                th, td { padding: 15px; text-align: left; border-bottom: 1px solid #ddd; vertical-align: top; }
                th { background: #f8f9fa; font-weight: 600; color: #555; }
                tr:hover { background: #f8f9fa; cursor: pointer; }
                
                .company-link { color: #009607; text-decoration: none; font-weight: 600; }
                .company-link:hover { text-decoration: underline; }
                .tag { background: #e8f5e8; color: #009607; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; margin: 2px; display: inline-block; }
                
                /* Actions column styling - simple table alignment */
                .actions { 
                    text-align: center;
                    vertical-align: middle;
                }
                .actions .btn { 
                    margin: 2px;
                    display: inline-block;
                }
                .btn { padding: 8px 16px; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; white-space: nowrap; }
                .btn-secondary { background: #6c757d; color: white; }
                .btn-danger { background: #dc3545; color: white; }
                .btn-disabled { background: #e9ecef; color: #6c757d; cursor: not-allowed; }
                .readonly-note { font-size: 0.8rem; color: #6c757d; font-style: italic; }
                
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
                    <h1>🔧 Admin Dashboard</h1>
                    <p>Manage companies and their products</p>
                </div>
                
                <div class="companies-table">
                    <h2>🏢 Companies</h2>
                    <button class="add-button" onclick="openAddCompanyModal()">➕ Add New Company</button>
                    
                    <table>
                        <thead>
                            <tr>
                                <th>Company Name</th>
                                <th>Description</th>
                                <th>Industry</th>
                                <th>Tags</th>
                                <th>Source</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for company in all_companies %}
                            <tr onclick="{% if not company.readonly %}window.location.href='/admin/company/{{ company.id }}/products'{% endif %}">
                                <td>
                                    {% if not company.readonly %}
                                    <a href="/admin/company/{{ company.id }}/products" class="company-link">
                                        {{ company.company }}
                                    </a>
                                    {% else %}
                                    <span class="company-link">{{ company.company }}</span>
                                    {% endif %}
                                </td>
                                <td>{{ company.description[:80] }}{% if company.description|length > 80 %}...{% endif %}</td>
                                <td>{{ company.industry or '-' }}</td>
                                <td>
                                    {% for tag in company.tags %}
                                    <span class="tag">{{ tag }}</span>
                                    {% endfor %}
                                </td>
                                <td>
                                    <span class="source-indicator source-{{ company.source }}">
                                        {{ company.source.upper() }}
                                    </span>
                                    {% if company.readonly %}
                                    <div class="readonly-note">Read-only</div>
                                    {% endif %}
                                </td>
                                <td class="actions">
                                    {% if not company.readonly %}
                                    <button class="btn btn-secondary" onclick="editCompany('{{ company.id }}')">Edit</button>
                                    <button class="btn btn-danger" onclick="deleteCompany('{{ company.id }}')">Delete</button>
                                    {% else %}
                                    <button class="btn btn-secondary btn-disabled" disabled title="JSON companies cannot be edited">Edit</button>
                                    <button class="btn btn-danger btn-disabled" disabled title="JSON companies cannot be deleted">Delete</button>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                            {% if all_companies|length == 0 %}
                            <tr>
                                <td colspan="6" style="text-align: center; padding: 40px; color: #7f8c8d;">
                                    No companies found.
                                </td>
                            </tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- Add Company Modal -->
            <div id="addCompanyModal" class="modal">
                <div class="modal-content">
                    <span class="close" onclick="closeAddCompanyModal()">&times;</span>
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
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" onclick="closeAddCompanyModal()">Cancel</button>
                            <button type="submit" class="btn btn-primary">Add Company</button>
                        </div>
                    </form>
                </div>
            </div>
            
            <script>
                // Modal functions
                function openAddCompanyModal() {
                    document.getElementById('addCompanyModal').style.display = 'block';
                }
                
                function closeAddCompanyModal() {
                    document.getElementById('addCompanyModal').style.display = 'none';
                    document.getElementById('companyForm').reset();
                }
                
                // Close modal when clicking outside
                window.onclick = function(event) {
                    const modal = document.getElementById('addCompanyModal');
                    if (event.target == modal) {
                        closeAddCompanyModal();
                    }
                }
                
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
        
        return render_template_string(html, all_companies=all_companies, existing_tags=existing_tags)
    
    return dashboard_bp
