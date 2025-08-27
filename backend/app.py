from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import sys
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.market_analysis_service import MarketAnalysisService
from services.sales_analytics_service import SalesAnalyticsService

app = Flask(__name__)
CORS(app)

# Initialize services
market_service = MarketAnalysisService()
sales_service = SalesAnalyticsService()

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

@app.route('/api/market-analysis/<industry>', methods=['GET'])
def get_market_analysis(industry):
    """Get comprehensive market analysis for an industry"""
    try:
        analysis = market_service.get_market_analysis(industry)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch market analysis'}), 500

@app.route('/api/competitive-position/<company_name>', methods=['GET'])
def get_competitive_position(company_name):
    """Get competitive position analysis for a company"""
    try:
        # Get company data to determine industry
        data = load_data()
        company = next((c for c in data.get('companies', []) if c['company'].lower() == company_name.lower()), None)
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        industry = company.get('industry', 'Software')
        analysis = market_service.get_company_competitive_position(company_name, industry)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch competitive position'}), 500

@app.route('/api/product-analysis/<product_id>', methods=['GET'])
def get_product_analysis(product_id):
    """Get competitive analysis for a specific product"""
    try:
        # Find the product
        data = load_data()
        product = None
        for company in data.get('companies', []):
            for p in company.get('products', []):
                if p.get('id') == product_id:
                    product = p
                    break
            if product:
                break
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        category = product.get('category', 'Software')
        analysis = market_service.get_product_competitive_analysis(product, category)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch product analysis'}), 500

@app.route('/api/cross-selling/<company_name>', methods=['GET'])
def get_cross_selling_recommendations(company_name):
    """Get cross-selling recommendations for a company"""
    try:
        data = load_data()
        company = next((c for c in data.get('companies', []) if c['company'].lower() == company_name.lower()), None)
        
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        all_companies = data.get('companies', [])
        recommendations = market_service.get_cross_selling_recommendations(company, all_companies)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to fetch cross-selling recommendations'}), 500

@app.route('/api/product-comparison', methods=['POST'])
def compare_products():
    """Compare multiple products for cross-selling analysis"""
    try:
        request_data = request.get_json()
        product_ids = request_data.get('product_ids', [])
        
        if not product_ids or len(product_ids) < 2:
            return jsonify({'error': 'At least 2 product IDs required for comparison'}), 400
        
        # Get product data
        data = load_data()
        products = []
        for company in data.get('companies', []):
            for product in company.get('products', []):
                if product.get('id') in product_ids:
                    product_with_company = product.copy()
                    product_with_company['company_name'] = company['company']
                    product_with_company['parent_company'] = company.get('parentCompany')
                    products.append(product_with_company)
        
        if len(products) < 2:
            return jsonify({'error': 'Could not find enough products for comparison'}), 404
        
        # Generate comparison analysis
        comparison = {
            'products': products,
            'feature_matrix': _generate_feature_matrix(products),
            'pricing_comparison': _generate_pricing_comparison(products),
            'target_audience_overlap': _analyze_audience_overlap(products),
            'cross_selling_potential': _calculate_cross_selling_potential(products),
            'recommendation_summary': _generate_comparison_recommendations(products)
        }
        
        return jsonify(comparison)
    except Exception as e:
        return jsonify({'error': str(e), 'message': 'Failed to compare products'}), 500

def _generate_feature_matrix(products):
    """Generate feature comparison matrix"""
    all_features = set()
    for product in products:
        all_features.update(product.get('features', []))
    
    matrix = []
    for feature in sorted(all_features):
        feature_row = {'feature': feature}
        for product in products:
            feature_row[product['id']] = feature in product.get('features', [])
        matrix.append(feature_row)
    
    return matrix

def _generate_pricing_comparison(products):
    """Generate pricing comparison"""
    pricing_data = []
    for product in products:
        pricing = product.get('pricing', {})
        pricing_data.append({
            'product_id': product['id'],
            'product_name': product['name'],
            'pricing_model': pricing.get('model', 'N/A'),
            'starting_price': pricing.get('startingPrice', 0),
            'currency': pricing.get('currency', 'EUR')
        })
    
    return pricing_data

def _analyze_audience_overlap(products):
    """Analyze target audience overlap"""
    audience_sets = []
    for product in products:
        audience_sets.append(set(product.get('targetAudience', [])))
    
    overlaps = []
    for i, product1 in enumerate(products):
        for j, product2 in enumerate(products):
            if i < j:
                overlap = audience_sets[i].intersection(audience_sets[j])
                overlap_percentage = len(overlap) / len(audience_sets[i].union(audience_sets[j])) * 100 if audience_sets[i].union(audience_sets[j]) else 0
                overlaps.append({
                    'product1': product1['name'],
                    'product2': product2['name'],
                    'common_audiences': list(overlap),
                    'overlap_percentage': round(overlap_percentage, 1)
                })
    
    return overlaps

def _calculate_cross_selling_potential(products):
    """Calculate cross-selling potential between products"""
    potentials = []
    categories = [p.get('category', '') for p in products]
    
    # Define category synergy scores
    synergy_scores = {
        ('Point of Sale', 'ERP'): 9.0,
        ('Point of Sale', 'CRM'): 8.5,
        ('ERP', 'CRM'): 8.0,
        ('Point of Sale', 'Inventory Management'): 9.5
    }
    
    for i, product1 in enumerate(products):
        for j, product2 in enumerate(products):
            if i < j:
                cat1, cat2 = categories[i], categories[j]
                synergy = synergy_scores.get((cat1, cat2), synergy_scores.get((cat2, cat1), 5.0))
                
                potentials.append({
                    'product1': product1['name'],
                    'product2': product2['name'],
                    'synergy_score': synergy,
                    'potential_level': 'High' if synergy >= 8.0 else 'Medium' if synergy >= 6.0 else 'Low'
                })
    
    return potentials

def _generate_comparison_recommendations(products):
    """Generate recommendations based on product comparison"""
    recommendations = []
    
    if len(products) >= 2:
        recommendations.extend([
            'Create bundled solution packages for enhanced value proposition',
            'Develop integrated workflows between complementary products',
            'Train sales teams on cross-selling opportunities',
            'Design joint marketing campaigns highlighting synergies'
        ])
    
    # Check for same parent company
    parent_companies = set(p.get('parent_company') for p in products if p.get('parent_company'))
    if len(parent_companies) == 1:
        recommendations.append('Leverage shared company brand for unified go-to-market strategy')
    
    return recommendations

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Catalog API is running'})

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
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
