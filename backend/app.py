from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import sys
import datetime
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.market_analysis_service import MarketAnalysisService
from services.sales_analytics_service import SalesAnalyticsService
from services.faq_service import FAQService
from admin_db import admin_db
from admin_api import create_admin_app
from admin_dashboard import create_dashboard_app

app = Flask(__name__)
CORS(app)

# Initialize services
market_service = MarketAnalysisService()
sales_service = SalesAnalyticsService()
faq_service = FAQService()

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

@app.route('/api/product-comparison', methods=['POST'])
def compare_products():
    """Compare selected products for cross-selling analysis"""
    try:
        data = request.get_json()
        product_ids = data.get('product_ids', [])
        
        if len(product_ids) < 2:
            return jsonify({"error": "At least 2 products are required for comparison"}), 400
        
        # Get combined data
        combined_data = admin_db.get_combined_data()
        
        # Find products by IDs
        products = []
        for company in combined_data.get('companies', []):
            for product in company.get('products', []):
                if product.get('id') in product_ids:
                    product_with_company = product.copy()
                    product_with_company['company_name'] = company.get('company', '')
                    product_with_company['parent_company'] = company.get('parentCompany', '')
                    product_with_company['industry'] = company.get('industry', '')
                    products.append(product_with_company)
        
        if len(products) < 2:
            return jsonify({"error": "Could not find enough products for comparison"}), 404
        
        # Generate feature matrix
        feature_matrix = _generate_feature_matrix(products)
        
        # Generate pricing comparison
        pricing_comparison = _generate_pricing_comparison(products)
        
        # Generate cross-selling analysis
        cross_selling_potential = _generate_cross_selling_potential(products)
        
        # Generate target audience overlap
        target_audience_overlap = _generate_target_audience_overlap(products)
        
        # Generate recommendation summary
        recommendation_summary = _generate_recommendation_summary(products)
        
        return jsonify({
            "products": products,
            "feature_matrix": feature_matrix,
            "pricing_comparison": pricing_comparison,
            "cross_selling_potential": cross_selling_potential,
            "target_audience_overlap": target_audience_overlap,
            "recommendation_summary": recommendation_summary
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to compare products"}), 500

def _generate_feature_matrix(products):
    """Generate feature comparison matrix"""
    all_features = set()
    
    # Collect all unique features
    for product in products:
        features = product.get('features', [])
        all_features.update(features)
    
    # Create matrix
    matrix = []
    for feature in sorted(all_features):
        feature_row = {"feature": feature}
        for product in products:
            product_features = product.get('features', [])
            feature_row[product['id']] = feature in product_features
        matrix.append(feature_row)
    
    return matrix

def _generate_pricing_comparison(products):
    """Generate pricing comparison"""
    pricing_data = []
    for product in products:
        pricing = product.get('pricing', {})
        pricing_data.append({
            "product_id": product['id'],
            "product_name": product['name'],
            "pricing_model": pricing.get('model', 'Unknown'),
            "starting_price": pricing.get('startingPrice', 'Contact for pricing'),
            "currency": pricing.get('currency', '')
        })
    return pricing_data

def _generate_cross_selling_potential(products):
    """Generate cross-selling potential analysis"""
    potential = []
    for i, product1 in enumerate(products):
        for j, product2 in enumerate(products):
            if i < j:  # Avoid duplicates
                # Simple analysis based on feature overlap and target audience
                features1 = set(product1.get('features', []))
                features2 = set(product2.get('features', []))
                feature_overlap = len(features1.intersection(features2)) / max(len(features1.union(features2)), 1)
                
                audience1 = set(product1.get('targetAudience', []))
                audience2 = set(product2.get('targetAudience', []))
                audience_overlap = len(audience1.intersection(audience2)) / max(len(audience1.union(audience2)), 1)
                
                synergy_score = round((feature_overlap + audience_overlap) * 5, 1)  # Scale to 0-10
                
                if synergy_score >= 7:
                    potential_level = "High"
                elif synergy_score >= 4:
                    potential_level = "Medium"
                else:
                    potential_level = "Low"
                
                potential.append({
                    "product1": product1['name'],
                    "product2": product2['name'],
                    "potential_level": potential_level,
                    "synergy_score": synergy_score
                })
    
    return potential

def _generate_target_audience_overlap(products):
    """Generate target audience overlap analysis"""
    overlap = []
    for i, product1 in enumerate(products):
        for j, product2 in enumerate(products):
            if i < j:  # Avoid duplicates
                audience1 = set(product1.get('targetAudience', []))
                audience2 = set(product2.get('targetAudience', []))
                common_audiences = audience1.intersection(audience2)
                
                if audience1 and audience2:
                    overlap_percentage = round(len(common_audiences) / len(audience1.union(audience2)) * 100)
                else:
                    overlap_percentage = 0
                
                overlap.append({
                    "product1": product1['name'],
                    "product2": product2['name'],
                    "overlap_percentage": overlap_percentage,
                    "common_audiences": list(common_audiences)
                })
    
    return overlap

def _generate_recommendation_summary(products):
    """Generate high-level recommendations"""
    recommendations = []
    
    if len(products) >= 2:
        recommendations.append(f"Bundle opportunity: Consider creating a package deal combining {products[0]['name']} and {products[1]['name']}")
        recommendations.append("Cross-training: Train sales teams on complementary product features")
        recommendations.append("Joint marketing: Develop integrated marketing campaigns for selected products")
        
        # Check for same company products
        same_company_products = {}
        for product in products:
            company = product.get('company_name', '')
            if company not in same_company_products:
                same_company_products[company] = []
            same_company_products[company].append(product['name'])
        
        for company, product_names in same_company_products.items():
            if len(product_names) > 1:
                recommendations.append(f"Internal synergy: {company} can leverage integration between {' and '.join(product_names)}")
    
    return recommendations

# FAQ Routes
@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    """
    Get all FAQs with optional filtering
    Query parameters:
    - search: Search query string
    - category: Category ID filter
    - limit: Number of results to return
    """
    try:
        search_query = request.args.get('search', '')
        category_id = request.args.get('category', '')
        limit = request.args.get('limit', type=int)
        
        faqs = faq_service.get_faqs(
            search_query=search_query,
            category_id=category_id,
            limit=limit
        )
        
        return jsonify({
            'success': True,
            'data': faqs,
            'total': len(faqs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faqs/<faq_id>', methods=['GET'])
def get_faq(faq_id):
    """Get specific FAQ by ID"""
    try:
        faq = faq_service.get_faq_by_id(faq_id)
        if not faq:
            return jsonify({'error': 'FAQ not found'}), 404
            
        return jsonify({
            'success': True,
            'data': faq
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faq-categories', methods=['GET'])
def get_faq_categories():
    """Get all FAQ categories"""
    try:
        categories = faq_service.get_categories()
        return jsonify({
            'success': True,
            'data': categories
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faq-search', methods=['POST'])
def search_faqs():
    """Advanced FAQ search with analytics tracking"""
    try:
        data = request.get_json()
        search_query = data.get('query', '')
        filters = data.get('filters', {})
        
        results = faq_service.advanced_search(search_query, filters)
        
        # Track search analytics (optional)
        faq_service.track_search(search_query, len(results))
        
        return jsonify({
            'success': True,
            'data': results,
            'query': search_query,
            'total': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faqs/<faq_id>/related', methods=['GET'])
def get_faq_related_content(faq_id):
    """Get companies and products related to specific FAQ - demonstrates catalog integration"""
    try:
        related_content = faq_service.get_related_content(faq_id)
        return jsonify({
            'success': True,
            'data': related_content,
            'faq_id': faq_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/market-analysis/<industry>', methods=['GET'])
def get_market_analysis(industry):
    """Get market analysis for a specific industry"""
    try:
        combined_data = admin_db.get_combined_data()
        
        # Filter companies by industry
        industry_companies = []
        for company in combined_data.get('companies', []):
            if company.get('industry', '').lower() == industry.lower():
                industry_companies.append(company)
        
        if not industry_companies:
            return jsonify({"error": f"No companies found in {industry} industry"}), 404
        
        # Generate market analysis
        total_companies = len(industry_companies)
        total_products = sum(len(company.get('products', [])) for company in industry_companies)
        
        # Analyze categories
        categories = {}
        for company in industry_companies:
            for product in company.get('products', []):
                category = product.get('category', 'Other')
                categories[category] = categories.get(category, 0) + 1
        
        # Market trends (enhanced data)
        market_trends = [
            "Digital transformation driving increased software adoption",
            "Cloud-first strategies becoming standard", 
            "Integration capabilities are key differentiators",
            "Mobile-first solutions gaining traction",
            "AI and automation features driving competitive advantage",
            "Subscription-based models dominating the market"
        ]
        
        # Major market players analysis
        major_players = []
        for company in industry_companies[:5]:  # Top 5 companies
            products = company.get('products', [])
            company_categories = list(set(p.get('category', 'Other') for p in products))
            
            # Mock market share and pricing data
            market_shares = ["15%", "12%", "10%", "8%", "6%"]
            pricing_models = ["Subscription", "One-time", "Freemium", "Tiered", "Custom"]
            
            major_players.append({
                "name": company.get('company'),
                "market_share": market_shares[len(major_players)] if len(major_players) < len(market_shares) else "5%",
                "target_market": f"{company_categories[0] if company_categories else 'General'} sector",
                "pricing_model": pricing_models[len(major_players) % len(pricing_models)],
                "strengths": [
                    f"Strong {company_categories[0] if company_categories else 'software'} portfolio",
                    f"Comprehensive suite of {len(products)} products",
                    "Established market presence",
                    "Strong customer base"
                ][:2],
                "weaknesses": [
                    "Limited international presence",
                    "High pricing compared to competitors",
                    "Complex implementation process",
                    "Limited mobile capabilities"
                ][:2]
            })
        
        # Strategic recommendations
        recommendations = [
            "Focus on cloud-native solutions to meet market demand",
            "Invest in AI and automation capabilities for competitive advantage",
            "Develop comprehensive integration platforms",
            "Expand mobile-first product offerings",
            "Consider strategic partnerships for market expansion",
            "Implement flexible subscription pricing models"
        ]
        
        # Market overview structure
        market_overview = {
            "market_size": {
                "global": "$45.2B (2024)",
                "europe": "$12.8B (2024)"
            },
            "growth_rate": "12.5% CAGR",
            "key_trends": market_trends
        }
        
        # Competitive landscape
        competitive_landscape = {
            "major_players": major_players,
            "market_concentration": "Moderately concentrated with top 5 players holding 51% market share"
        }
        
        # Get AI-powered market analysis
        company_name = request.args.get('company')  # Optional company context
        try:
            ai_analysis = market_service.get_market_analysis(industry)
            
            # Merge AI analysis with local data
            enhanced_analysis = ai_analysis.copy()
            enhanced_analysis.update({
                "local_market_data": {
                    "total_companies": total_companies,
                    "total_products": total_products,
                    "top_categories": dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]),
                    "companies": [{"name": c.get('company'), "products_count": len(c.get('products', []))} for c in industry_companies]
                }
            })
            
            return jsonify(enhanced_analysis)
            
        except Exception as ai_error:
            # Fallback to traditional analysis if AI fails
            return jsonify({
                "industry": industry,
                "analysis_type": "Traditional Analysis (AI Unavailable)",
                "total_companies": total_companies,
                "total_products": total_products,
                "top_categories": dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]),
                "market_overview": market_overview,
                "competitive_landscape": competitive_landscape,
                "recommendations": recommendations,
                "companies": [{"name": c.get('company'), "products_count": len(c.get('products', []))} for c in industry_companies],
                "ai_error": str(ai_error)
            })
        
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to fetch market analysis"}), 500

@app.route('/api/competitive-position/<company_name>', methods=['GET'])
def get_competitive_position(company_name):
    """Get AI-powered competitive position analysis for a company"""
    try:
        combined_data = admin_db.get_combined_data()
        
        # Find the company
        target_company = None
        for company in combined_data.get('companies', []):
            if company.get('company', '').lower() == company_name.lower():
                target_company = company
                break
        
        if not target_company:
            return jsonify({"error": f"Company {company_name} not found"}), 404
        
        # Get AI-powered competitive position analysis
        industry = target_company.get('industry', 'Point of Sale Software')
        try:
            ai_analysis = market_service.get_company_competitive_position(company_name, industry, target_company)
            
            # Add local company data context
            ai_analysis["local_company_data"] = {
                "company": target_company.get('company'),
                "industry": industry,
                "products_count": len(target_company.get('products', [])),
                "parent_company": target_company.get('parentCompany'),
                "description": target_company.get('description')
            }
            
            return jsonify(ai_analysis)
            
        except Exception as ai_error:
            # Fallback to traditional analysis if AI fails
            pass  # Continue with traditional analysis below
        
        # Find competitors (same industry)
        industry = target_company.get('industry', '')
        competitors = []
        for company in combined_data.get('companies', []):
            if (company.get('industry', '').lower() == industry.lower() and 
                company.get('company', '').lower() != company_name.lower()):
                competitors.append({
                    "name": company.get('company'),
                    "products_count": len(company.get('products', [])),
                    "categories": list(set(p.get('category', 'Other') for p in company.get('products', [])))
                })
        
        # Analyze company's position
        company_products = target_company.get('products', [])
        company_categories = list(set(p.get('category', 'Other') for p in company_products))
        
        # Competitive advantages (mock analysis)
        advantages = [
            f"Strong presence in {company_categories[0] if company_categories else 'various'} category",
            f"Portfolio of {len(company_products)} products",
            "Established market position",
            "Comprehensive product suite"
        ]
        
        # Market opportunities
        opportunities = [
            "Potential for product bundling",
            "Cross-selling to existing customer base",
            "Market expansion possibilities",
            "Technology integration opportunities"
        ]
        
        return jsonify({
            "company": company_name,
            "industry": industry,
            "products_count": len(company_products),
            "categories": company_categories,
            "competitors": competitors[:5],  # Top 5 competitors
            "competitive_advantages": advantages,
            "market_opportunities": opportunities
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to fetch competitive position"}), 500

@app.route('/api/product-analysis/<product_id>', methods=['GET'])
def get_product_analysis(product_id):
    """Get detailed analysis for a specific product"""
    try:
        combined_data = admin_db.get_combined_data()
        
        # Find the product
        target_product = None
        product_company = None
        for company in combined_data.get('companies', []):
            for product in company.get('products', []):
                if product.get('id') == product_id:
                    target_product = product
                    product_company = company
                    break
            if target_product:
                break
        
        if not target_product:
            return jsonify({"error": f"Product {product_id} not found"}), 404
        
        # Find similar products (same category)
        category = target_product.get('category', '')
        similar_products = []
        for company in combined_data.get('companies', []):
            for product in company.get('products', []):
                if (product.get('category', '').lower() == category.lower() and 
                    product.get('id') != product_id):
                    similar_products.append({
                        "name": product.get('name'),
                        "company": company.get('company'),
                        "features_count": len(product.get('features', []))
                    })
        
        # Analysis insights
        features = target_product.get('features', [])
        target_audience = target_product.get('targetAudience', [])
        
        strengths = [
            f"Rich feature set with {len(features)} capabilities",
            f"Targets {len(target_audience)} market segments",
            "Well-positioned in market category",
            "Strong integration potential"
        ]
        
        recommendations = [
            "Consider feature bundling opportunities",
            "Explore adjacent market segments",
            "Enhance integration capabilities",
            "Develop partnership strategies"
        ]
        
        return jsonify({
            "product": target_product,
            "company": product_company.get('company'),
            "industry": product_company.get('industry'),
            "similar_products": similar_products[:5],
            "strengths": strengths,
            "recommendations": recommendations,
            "market_position": "Strong" if len(features) > 5 else "Moderate"
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to fetch product analysis"}), 500

@app.route('/api/cross-selling/<company_name>', methods=['GET'])
def get_cross_selling_recommendations(company_name):
    """Get cross-selling recommendations for a company"""
    try:
        combined_data = admin_db.get_combined_data()
        
        # Find the company
        target_company = None
        for company in combined_data.get('companies', []):
            if company.get('company', '').lower() == company_name.lower():
                target_company = company
                break
        
        if not target_company:
            return jsonify({"error": f"Company {company_name} not found"}), 404
        
        # Find parent company and group companies
        parent_company = target_company.get('parentCompany', '')
        group_companies = []
        
        if parent_company:
            for company in combined_data.get('companies', []):
                if (company.get('parentCompany', '').lower() == parent_company.lower() and 
                    company.get('company', '').lower() != company_name.lower()):
                    group_companies.append(company.get('company'))
        
        # Generate cross-selling opportunities
        company_products = target_company.get('products', [])
        company_categories = [p.get('category', '') for p in company_products]
        cross_selling_opportunities = []
        
        # Get all companies for cross-selling opportunities (not just group companies)
        all_companies = combined_data.get('companies', [])
        
        for potential_partner in all_companies:
            partner_name = potential_partner.get('company', '')
            
            # Skip the target company itself
            if partner_name.lower() == company_name.lower():
                continue
                
            partner_products = potential_partner.get('products', [])
            complementary_products = []
            
            # Find complementary products (products in different categories)
            for product in partner_products[:4]:  # Top 4 products per company
                product_category = product.get('category', '')
                
                # Check if this category complements target company's categories
                if product_category not in company_categories:
                    potential_level = "High"
                    synergy_score = 8
                    
                    # Adjust potential based on product features and target audience overlap
                    product_features = product.get('features', [])
                    if len(product_features) <= 3:
                        potential_level = "Medium"
                        synergy_score = 6
                    elif len(product_features) > 8:
                        potential_level = "High"
                        synergy_score = 9
                    
                    complementary_products.append({
                        "product_name": product.get('name'),
                        "category": product_category,
                        "cross_sell_potential": potential_level,
                        "synergy_score": synergy_score
                    })
            
            # Only include companies that have complementary products
            if complementary_products:
                # Determine partnership type based on group relationship
                is_group_company = partner_name in group_companies
                partnership_type = "Group Partnership" if is_group_company else "Strategic Partnership"
                
                partnership_opportunities = [
                    f"Joint sales initiatives with {partner_name}",
                    f"Integrated solution packages combining offerings",
                    f"Cross-referral programs between companies",
                    f"Shared marketing and customer success programs"
                ]
                
                if is_group_company:
                    partnership_opportunities.extend([
                        "Unified pricing and packaging strategies",
                        "Shared customer database and insights"
                    ])
                
                cross_selling_opportunities.append({
                    "company": partner_name,
                    "partnership_type": partnership_type,
                    "complementary_products": complementary_products,
                    "partnership_opportunities": partnership_opportunities[:4]  # Limit to 4 opportunities
                })
        
        # Sort by number of complementary products (most opportunities first)
        cross_selling_opportunities.sort(key=lambda x: len(x["complementary_products"]), reverse=True)
        
        return jsonify({
            "company": company_name,
            "parent_company": parent_company or "Independent",
            "group_companies": group_companies,
            "cross_selling_opportunities": cross_selling_opportunities
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to fetch cross-selling recommendations"}), 500

# ========================================
# NEW AI-POWERED ENDPOINTS
# ========================================

@app.route('/api/ai-market-intelligence/<industry>', methods=['GET'])
def get_ai_market_intelligence(industry):
    """Get real-time AI-powered market intelligence"""
    try:
        company_name = request.args.get('company')
        intelligence = market_service.get_ai_market_intelligence(industry, company_name)
        return jsonify(intelligence)
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to get AI market intelligence"}), 500

@app.route('/api/ai-trend-analysis/<industry>', methods=['GET'])
def get_ai_trend_analysis(industry):
    """Get AI-powered trend analysis and predictions"""
    try:
        time_horizon = request.args.get('horizon', '6_months')
        analysis = market_service.get_ai_trend_analysis(industry, time_horizon)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to get AI trend analysis"}), 500

@app.route('/api/ai-trend-alerts/<industry>', methods=['GET'])
def get_ai_trend_alerts(industry):
    """Get AI-powered trend alerts"""
    try:
        company_name = request.args.get('company')
        alerts = market_service.get_ai_trend_alerts(industry, company_name)
        return jsonify({"alerts": alerts, "count": len(alerts)})
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to get AI trend alerts"}), 500

@app.route('/api/real-time-insights/<industry>', methods=['GET'])
def get_real_time_insights(industry):
    """Get comprehensive real-time market insights"""
    try:
        company_name = request.args.get('company')
        insights = market_service.get_real_time_market_insights(industry, company_name)
        return jsonify(insights)
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to get real-time insights"}), 500

@app.route('/api/ai-competitive-intelligence/<company_name>', methods=['GET'])
def get_ai_competitive_intelligence(company_name):
    """Get AI-powered competitive intelligence for a company"""
    try:
        industry = request.args.get('industry', 'Point of Sale Software')
        
        # Get company data
        combined_data = admin_db.get_combined_data()
        company_data = None
        for company in combined_data.get('companies', []):
            if company.get('company').lower() == company_name.lower():
                company_data = company
                break
        
        if not company_data:
            company_data = {"company": company_name, "products": []}
        
        intelligence = market_service.get_ai_competitive_intelligence(company_name, industry, company_data)
        return jsonify(intelligence)
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to get AI competitive intelligence"}), 500

@app.route('/api/ai-competitive-scoring/<company_name>', methods=['GET'])
def get_ai_competitive_scoring(company_name):
    """Get AI-powered competitive scoring"""
    try:
        industry = request.args.get('industry', 'Point of Sale Software')
        scoring = market_service.get_ai_competitive_scoring(company_name, industry)
        return jsonify(scoring)
    except Exception as e:
        return jsonify({"error": str(e), "message": "Failed to get AI competitive scoring"}), 500

@app.route('/api/ai-analysis-status', methods=['GET'])
def get_ai_analysis_status():
    """Get AI analysis service status and capabilities"""
    try:
        return jsonify({
            "status": "active",
            "services": {
                "market_intelligence": "operational",
                "competitive_analysis": "operational", 
                "trend_analysis": "operational"
            },
            "capabilities": [
                "Real-time market data analysis",
                "AI-powered competitive intelligence",
                "Trend detection and prediction",
                "Market opportunity identification",
                "Competitive positioning analysis",
                "Investment and funding insights"
            ],
            "data_sources": [
                "Real-time market APIs",
                "News sentiment analysis",
                "Competitive intelligence gathering",
                "AI trend detection algorithms",
                "Machine learning predictions"
            ],
            "update_frequency": "Real-time with 5-minute cache",
            "confidence_score": 0.89,
            "last_updated": datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Register admin blueprints
admin_app = create_admin_app()
dashboard_app = create_dashboard_app()
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(dashboard_app, url_prefix='/admin-dashboard')

# Sales Analytics API Endpoints
@app.route('/api/sales/health', methods=['GET'])
def sales_health_check():
    """Sales service health check"""
    try:
        # Test data loading
        summary = sales_service.get_sales_summary()
        return jsonify({
            'status': 'healthy', 
            'message': 'Sales Analytics API is running',
            'data_loaded': True,
            'total_records': summary.get('total_records', 0)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Sales Analytics API error',
            'error': str(e)
        }), 500

@app.route('/api/sales/summary', methods=['GET'])
def get_sales_summary():
    """Get basic sales summary with optional filtering"""
    try:
        # Get query parameters
        product_id = request.args.get('product_id')
        sector = request.args.get('sector')
        region = request.args.get('region')
        period_start = request.args.get('period_start')
        period_end = request.args.get('period_end')
        
        summary = sales_service.get_sales_summary(
            product_id=product_id,
            sector=sector,
            region=region,
            period_start=period_start,
            period_end=period_end
        )
        
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch sales summary'}), 500

@app.route('/api/sales/test-data', methods=['GET'])
def get_sales_test_data():
    """Return sample data for frontend development"""
    try:
        # Get a subset of data for testing
        summary = sales_service.get_sales_summary()
        sector_performance = sales_service.get_sector_performance()
        
        # Get trend data for the first available product
        sales_service._load_data()
        if sales_service.data and sales_service.data.get('sales_data'):
            first_product = sales_service.data['sales_data'][0]
            trend_data = sales_service.get_trend_analysis(first_product.product_id)
        else:
            trend_data = {}
        
        test_data = {
            'summary': summary,
            'sector_performance': sector_performance[:3],  # Top 3 sectors
            'sample_trend': trend_data,
            'available_filters': {
                'sectors': list(set(entry.sector for entry in sales_service.data.get('sales_data', []))),
                'regions': list(set(entry.region for entry in sales_service.data.get('sales_data', []))),
                'products': list(set(entry.product_id for entry in sales_service.data.get('sales_data', [])))
            } if sales_service.data else {}
        }
        
        return jsonify(test_data)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch test data'}), 500

@app.route('/api/sales/sectors', methods=['GET'])
def get_sector_performance():
    """Get sales performance by sector"""
    try:
        region = request.args.get('region')
        sector_data = sales_service.get_sector_performance(region=region)
        
        return jsonify({
            'sectors': sector_data,
            'total_sectors': len(sector_data),
            'region_filter': region
        })
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch sector performance'}), 500

@app.route('/api/sales/trends/<product_id>', methods=['GET'])
def get_product_trends(product_id):
    """Get trend analysis for a specific product"""
    try:
        analysis_type = request.args.get('analysis_type', 'monthly')
        trend_data = sales_service.get_trend_analysis(product_id, analysis_type)
        
        return jsonify(trend_data)
    except ValueError as e:
        return jsonify({'error': str(e), 'message': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch trend analysis'}), 500

@app.route('/api/sales/validation', methods=['GET'])
def get_data_quality():
    """Get data quality validation results"""
    try:
        validation_results = sales_service.validate_data_quality()
        return jsonify(validation_results)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to validate data quality'}), 500

@app.route('/api/sales/reload', methods=['POST'])
def reload_sales_data():
    """Force reload of sales data (for development/testing)"""
    try:
        sales_service.reload_data()
        summary = sales_service.get_sales_summary()
        
        return jsonify({
            'message': 'Sales data reloaded successfully',
            'total_records': summary.get('total_records', 0),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to reload sales data'}), 500

# Advanced Sales Trends API Endpoints (Phase 2)
@app.route('/api/sales/trends', methods=['GET'])
def get_sales_trends():
    """Get time-series trend data with filtering"""
    try:
        # Get query parameters
        product_id = request.args.get('product_id')
        sector = request.args.get('sector')
        region = request.args.get('region')
        date_range = request.args.get('date_range')  # 'latest_quarter', 'latest_year', etc.
        period = request.args.get('period', 'monthly')  # monthly, quarterly, yearly
        
        if not product_id:
            return jsonify({'error': 'product_id parameter is required'}), 400
        
        # Get trend analysis
        trend_data = sales_service.get_trend_analysis(product_id, period)
        
        # Apply additional filtering if needed
        filtered_trend_data = trend_data.copy()
        if date_range:
            # Filter trend data based on date range
            filtered_points = []
            for point in trend_data['trend_data']:
                if sales_service._is_in_time_period(point['period'], date_range):
                    filtered_points.append(point)
            filtered_trend_data['trend_data'] = filtered_points
        
        return jsonify({
            'trend_analysis': filtered_trend_data,
            'filters_applied': {
                'product_id': product_id,
                'sector': sector,
                'region': region,
                'date_range': date_range,
                'period': period
            }
        })
    except ValueError as e:
        return jsonify({'error': str(e), 'message': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch trends data'}), 500

@app.route('/api/sales/trends/all', methods=['GET'])
def get_all_products_trends():
    """Get trend data for all products"""
    try:
        # Get query parameters
        sector = request.args.get('sector')
        region = request.args.get('region')
        limit = int(request.args.get('limit', 10))
        
        # Get all available products first
        sales_service._load_data()
        if not sales_service.data or not sales_service.data.get('sales_data'):
            return jsonify({'trends': [], 'message': 'No sales data available'})
        
        # Filter products based on criteria
        filtered_data = sales_service._filter_sales_data(
            sales_service.data['sales_data'], 
            sector=sector, 
            region=region
        )
        
        # Get unique product IDs
        product_ids = list(set(entry.product_id for entry in filtered_data))[:limit]
        
        # Get trend data for each product
        all_trends = []
        for product_id in product_ids:
            try:
                trend_data = sales_service.get_trend_analysis(product_id)
                all_trends.append(trend_data)
            except Exception as e:
                logger.warning(f"Failed to get trends for product {product_id}: {e}")
                continue
        
        return jsonify({
            'trends': all_trends,
            'total_products': len(product_ids),
            'filters_applied': {
                'sector': sector,
                'region': region,
                'limit': limit
            }
        })
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch all trends data'}), 500

# Advanced Sector Analysis API Endpoints
@app.route('/api/sales/by-sector', methods=['GET'])
def get_sales_by_sector():
    """Get sales breakdown by sector with advanced analytics"""
    try:
        region = request.args.get('region')
        time_period = request.args.get('time_period')  # latest_quarter, latest_year, etc.
        
        sector_data = sales_service.get_sector_analysis_advanced(
            region=region, 
            time_period=time_period
        )
        
        return jsonify(sector_data)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch sector breakdown'}), 500

@app.route('/api/sales/sector-trends', methods=['GET'])
def get_sector_trends():
    """Get sector performance trends over time"""
    try:
        region = request.args.get('region')
        
        # Get basic sector performance
        sector_performance = sales_service.get_sector_performance(region=region)
        
        # Get advanced sector analysis
        advanced_analysis = sales_service.get_sector_analysis_advanced(region=region)
        
        return jsonify({
            'basic_performance': sector_performance,
            'advanced_analysis': advanced_analysis,
            'filters_applied': {
                'region': region
            }
        })
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch sector trends'}), 500

@app.route('/api/sales/sector-comparison', methods=['POST'])
def compare_sectors():
    """Compare multiple sectors performance"""
    try:
        request_data = request.get_json()
        sectors = request_data.get('sectors', [])
        region = request_data.get('region')
        
        if not sectors or len(sectors) < 2:
            return jsonify({'error': 'At least 2 sectors required for comparison'}), 400
        
        # Get advanced sector analysis
        all_sectors_data = sales_service.get_sector_analysis_advanced(region=region)
        
        # Filter for requested sectors
        comparison_data = []
        for sector_info in all_sectors_data['sectors']:
            if sector_info['sector'] in sectors:
                comparison_data.append(sector_info)
        
        if len(comparison_data) < 2:
            return jsonify({'error': 'Could not find enough sectors for comparison'}), 404
        
        # Calculate comparison metrics
        total_revenue = sum(s['total_revenue'] for s in comparison_data)
        comparison_metrics = {
            'revenue_leader': max(comparison_data, key=lambda x: x['total_revenue'])['sector'],
            'growth_leader': max(comparison_data, key=lambda x: x['average_growth_rate'])['sector'],
            'market_share_leader': max(comparison_data, key=lambda x: x['market_penetration'])['sector'],
            'most_diverse': max(comparison_data, key=lambda x: x['product_count'])['sector'],
            'total_combined_revenue': round(total_revenue, 2)
        }
        
        return jsonify({
            'comparison_data': comparison_data,
            'comparison_metrics': comparison_metrics,
            'sectors_compared': sectors,
            'filters_applied': {
                'region': region
            }
        })
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to compare sectors'}), 500

# Product Performance API Endpoints
@app.route('/api/sales/top-products', methods=['GET'])
def get_top_products():
    """Get best performing products"""
    try:
        sector = request.args.get('sector')
        region = request.args.get('region')
        limit = int(request.args.get('limit', 10))
        metric = request.args.get('metric', 'revenue')  # revenue, units, growth_rate
        
        # Get product performance analytics
        analytics = sales_service.get_product_performance_analytics(
            sector=sector, 
            region=region, 
            limit=limit
        )
        
        # Sort by requested metric
        if metric == 'revenue':
            top_products = analytics['top_performers']
        elif metric == 'units':
            top_products = sorted(analytics['top_performers'], key=lambda x: x['total_units'], reverse=True)[:limit]
        elif metric == 'growth_rate':
            top_products = sorted(analytics['top_performers'], key=lambda x: x['average_growth_rate'], reverse=True)[:limit]
        else:
            top_products = analytics['top_performers']
        
        return jsonify({
            'top_products': top_products,
            'metric_used': metric,
            'summary_stats': analytics['summary_stats'],
            'filters_applied': {
                'sector': sector,
                'region': region,
                'limit': limit,
                'metric': metric
            }
        })
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch top products'}), 500

@app.route('/api/sales/product-rankings', methods=['GET'])
def get_product_rankings():
    """Get ranked product performance across all metrics"""
    try:
        sector = request.args.get('sector')
        region = request.args.get('region')
        limit = int(request.args.get('limit', 20))
        
        analytics = sales_service.get_product_performance_analytics(
            sector=sector, 
            region=region, 
            limit=limit
        )
        
        return jsonify({
            'rankings': {
                'by_revenue': analytics['top_performers'],
                'by_lifecycle': analytics['lifecycle_analysis'],
                'by_efficiency': analytics['revenue_vs_units_analysis'][:limit]
            },
            'cross_sector_analysis': analytics['cross_sector_performance'],
            'summary_stats': analytics['summary_stats'],
            'filters_applied': analytics['filters_applied']
        })
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch product rankings'}), 500

@app.route('/api/sales/performance/<product_id>', methods=['GET'])
def get_product_performance_detail(product_id):
    """Get detailed performance analytics for a specific product"""
    try:
        # Get trend analysis
        trend_data = sales_service.get_trend_analysis(product_id)
        
        # Get product performance analytics (filtered to this product)
        sales_service._load_data()
        filtered_data = sales_service._filter_sales_data(
            sales_service.data['sales_data'], 
            product_id=product_id
        )
        
        if not filtered_data:
            return jsonify({'error': 'Product not found'}), 404
        
        # Calculate cross-sector performance for this product
        cross_sector_data = {}
        for sales_entry in filtered_data:
            sector = sales_entry.sector
            if sector not in cross_sector_data:
                cross_sector_data[sector] = {
                    'revenue': 0,
                    'units': 0,
                    'growth_rates': []
                }
            
            for record in sales_entry.sales_records:
                cross_sector_data[sector]['revenue'] += record.revenue
                cross_sector_data[sector]['units'] += record.units_sold
                cross_sector_data[sector]['growth_rates'].append(record.growth_rate)
        
        # Calculate averages for each sector
        for sector, data in cross_sector_data.items():
            data['average_growth_rate'] = sum(data['growth_rates']) / len(data['growth_rates']) if data['growth_rates'] else 0
            data['revenue_per_unit'] = data['revenue'] / data['units'] if data['units'] > 0 else 0
        
        return jsonify({
            'product_id': product_id,
            'trend_analysis': trend_data,
            'cross_sector_performance': cross_sector_data,
            'sector_count': len(cross_sector_data),
            'best_performing_sector': max(cross_sector_data.items(), key=lambda x: x[1]['revenue'])[0] if cross_sector_data else None,
            'total_revenue': sum(data['revenue'] for data in cross_sector_data.values()),
            'total_units': sum(data['units'] for data in cross_sector_data.values())
        })
    except ValueError as e:
        return jsonify({'error': str(e), 'message': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch product performance'}), 500

@app.route('/api/sales/cross-sector/<product_id>', methods=['GET'])
def get_product_cross_sector_performance(product_id):
    """Get product performance across different sectors"""
    try:
        # This is essentially the same as the detailed performance endpoint
        # but focused specifically on cross-sector analysis
        return get_product_performance_detail(product_id)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch cross-sector performance'}), 500

# Advanced Query API Endpoints (Phase 2)
@app.route('/api/sales/advanced-query', methods=['POST'])
def advanced_sales_query():
    """Perform advanced multi-dimensional queries with statistical analysis"""
    try:
        request_data = request.get_json()
        
        # Extract query parameters
        filters = request_data.get('filters', {})
        aggregations = request_data.get('aggregations', ['sum', 'avg', 'count'])
        sort_by = request_data.get('sort_by', 'revenue')
        limit = request_data.get('limit')
        include_stats = request_data.get('include_statistical_significance', False)
        
        # Validate filters
        if not filters:
            return jsonify({'error': 'At least one filter must be provided'}), 400
        
        # Execute advanced query
        results = sales_service.advanced_multi_dimensional_query(
            filters=filters,
            aggregations=aggregations,
            sort_by=sort_by,
            limit=limit,
            include_statistical_significance=include_stats
        )
        
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to execute advanced query'}), 500

@app.route('/api/sales/quick-filters', methods=['GET'])
def get_quick_filter_options():
    """Get available filter options for quick filtering"""
    try:
        sales_service._load_data()
        if not sales_service.data or not sales_service.data.get('sales_data'):
            return jsonify({
                'products': [],
                'sectors': [],
                'regions': [],
                'date_ranges': []
            })
        
        # Extract unique values for filters
        products = list(sales_service._product_index.keys())
        sectors = list(sales_service._sector_index.keys())
        regions = list(sales_service._region_index.keys())
        
        # Extract date range information
        periods = sorted(sales_service._period_index.keys())
        date_ranges = []
        if periods:
            date_ranges = [
                {'key': 'latest_quarter', 'label': 'Last 3 Months', 'value': 'latest_quarter'},
                {'key': 'latest_6_months', 'label': 'Last 6 Months', 'value': 'latest_6_months'},
                {'key': 'latest_year', 'label': 'Last 12 Months', 'value': 'latest_year'},
                {'key': 'custom', 'label': 'Custom Range', 'value': 'custom', 'min_date': periods[0], 'max_date': periods[-1]}
            ]
        
        return jsonify({
            'products': [{'id': p, 'label': p} for p in sorted(products)],
            'sectors': [{'id': s, 'label': s} for s in sorted(sectors)],
            'regions': [{'id': r, 'label': r} for r in sorted(regions)],
            'date_ranges': date_ranges,
            'aggregation_options': [
                {'key': 'sum', 'label': 'Sum'},
                {'key': 'avg', 'label': 'Average'},
                {'key': 'count', 'label': 'Count'},
                {'key': 'min', 'label': 'Minimum'},
                {'key': 'max', 'label': 'Maximum'}
            ],
            'sort_options': [
                {'key': 'revenue', 'label': 'Revenue'},
                {'key': 'units', 'label': 'Units Sold'},
                {'key': 'growth_rate', 'label': 'Growth Rate'},
                {'key': 'market_share', 'label': 'Market Share'}
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch filter options'}), 500

# Performance optimization endpoint
@app.route('/api/sales/cache-stats', methods=['GET'])
def get_cache_statistics():
    """Get cache performance statistics"""
    try:
        stats = {
            'data_cache': {
                'is_cached': sales_service._cache_timestamp is not None,
                'cache_age_seconds': (datetime.now() - sales_service._cache_timestamp).total_seconds() if sales_service._cache_timestamp else 0,
                'cache_ttl_seconds': sales_service._cache_ttl
            },
            'analytics_cache': {
                'cached_queries': len(sales_service._analytics_cache),
                'cache_ttl_seconds': sales_service._analytics_cache_ttl,
                'cached_methods': list(set(key.split('_')[0] for key in sales_service._analytics_cache.keys()))
            },
            'indexes': {
                'products_indexed': len(sales_service._product_index),
                'sectors_indexed': len(sales_service._sector_index),
                'regions_indexed': len(sales_service._region_index),
                'periods_indexed': len(sales_service._period_index)
            }
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch cache statistics'}), 500

@app.route('/api/sales/cache/clear', methods=['POST'])
def clear_sales_cache():
    """Clear all sales analytics caches"""
    try:
        sales_service.invalidate_cache()
        return jsonify({
            'message': 'All caches cleared successfully',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to clear cache'}), 500

if __name__ == '__main__':
    print("🚀 Starting Catalog API with Admin Panel...")
    print("📊 Main API: http://localhost:5000/api")
    print("🔧 Admin Dashboard: http://localhost:5000/admin-dashboard")
    print("📋 Secret Admin URLs:")
    print("   - Dashboard: http://localhost:5000/admin-dashboard")
    print("   - Companies: http://localhost:5000/admin/companies")
    print("   - Company Products: http://localhost:5000/admin/company/{company_id}/products")
    app.run(debug=True, host='0.0.0.0', port=5000)
