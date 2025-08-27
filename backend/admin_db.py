import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class AdminDatabase:
    def __init__(self):
        self.companies: Dict[str, dict] = {}
        self.products: Dict[str, dict] = {}
        self._load_existing_data()
    
    def _load_existing_data(self):
        """Load existing companies from JSON to extract available tags"""
        try:
            with open('data/companies.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.existing_tags = set()
                for company in data.get('companies', []):
                    for product in company.get('products', []):
                        if 'category' in product:
                            self.existing_tags.add(product['category'])
        except FileNotFoundError:
            self.existing_tags = set()
    
    def get_existing_tags(self) -> List[str]:
        """Get all available tags from existing data"""
        return sorted(list(self.existing_tags))
    
    def add_company(self, company_data: dict) -> str:
        """Add a new company and return its ID"""
        company_id = str(uuid.uuid4())
        company = {
            'id': company_id,
            'company': company_data['company'],
            'parentCompany': company_data.get('parentCompany', ''),
            'description': company_data['description'],
            'industry': company_data.get('industry', ''),
            'tags': company_data.get('tags', []),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.companies[company_id] = company
        return company_id
    
    def update_company(self, company_id: str, company_data: dict) -> bool:
        """Update an existing company"""
        if company_id not in self.companies:
            return False
        
        company = self.companies[company_id]
        company.update({
            'company': company_data['company'],
            'parentCompany': company_data.get('parentCompany', ''),
            'description': company_data['description'],
            'industry': company_data.get('industry', ''),
            'tags': company_data.get('tags', []),
            'updated_at': datetime.now().isoformat()
        })
        return True
    
    def delete_company(self, company_id: str) -> bool:
        """Delete a company and all its products"""
        if company_id not in self.companies:
            return False
        
        # Delete all products associated with this company
        products_to_delete = [
            product_id for product_id, product in self.products.items()
            if product.get('company_id') == company_id
        ]
        for product_id in products_to_delete:
            del self.products[product_id]
        
        # Delete the company
        del self.companies[company_id]
        return True
    
    def get_company(self, company_id: str) -> Optional[dict]:
        """Get a company by ID"""
        return self.companies.get(company_id)
    
    def get_all_companies(self) -> List[dict]:
        """Get all companies"""
        return list(self.companies.values())
    
    def add_product(self, product_data: dict) -> str:
        """Add a new product and return its ID"""
        product_id = str(uuid.uuid4())
        product = {
            'id': product_id,
            'company_id': product_data.get('company_id', ''),
            'company_name': product_data.get('company_name', ''),
            'name': product_data['name'],
            'description': product_data['description'],
            'category': product_data['category'],
            'features': product_data.get('features', []),
            'targetAudience': product_data.get('targetAudience', []),
            'pricing': product_data.get('pricing', {
                'model': 'subscription',
                'startingPrice': 0,
                'currency': 'USD'
            }),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.products[product_id] = product
        return product_id
    
    def update_product(self, product_id: str, product_data: dict) -> bool:
        """Update an existing product"""
        if product_id not in self.products:
            return False
        
        product = self.products[product_id]
        product.update({
            'name': product_data['name'],
            'description': product_data['description'],
            'category': product_data['category'],
            'features': product_data.get('features', []),
            'targetAudience': product_data.get('targetAudience', []),
            'pricing': product_data.get('pricing', {
                'model': 'subscription',
                'startingPrice': 0,
                'currency': 'USD'
            }),
            'updated_at': datetime.now().isoformat()
        })
        return True
    
    def delete_product(self, product_id: str) -> bool:
        """Delete a product"""
        if product_id not in self.products:
            return False
        
        del self.products[product_id]
        return True
    
    def get_product(self, product_id: str) -> Optional[dict]:
        """Get a product by ID"""
        return self.products.get(product_id)
    
    def get_products_by_company(self, company_id: str) -> List[dict]:
        """Get all products for a specific company"""
        # First try to find products by company_id (for admin companies)
        products_by_id = [
            product for product in self.products.values()
            if product.get('company_id') == company_id
        ]
        
        if products_by_id:
            return products_by_id
        
        # If no products found by ID, try to find the company and get products by name
        company = self.get_company(company_id)
        if company:
            return self.get_products_by_company_name(company['company'])
        
        return []
    
    def get_products_by_company_name(self, company_name: str) -> List[dict]:
        """Get all products for a specific company by name (for JSON companies)"""
        return [
            product for product in self.products.values()
            if product.get('company_name') == company_name
        ]
    
    def get_all_products(self) -> List[dict]:
        """Get all products"""
        return list(self.products.values())
    
    def get_combined_data(self) -> dict:
        """Get combined data from JSON and admin database"""
        try:
            with open('data/companies.json', 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            json_data = {'companies': []}
        
        # Create a copy of JSON companies
        combined_companies = []
        
        # Add JSON companies
        for company in json_data.get('companies', []):
            company_copy = company.copy()
            company_copy['source'] = 'json'
            company_copy['products'] = self.get_products_by_company_name(company['company'])
            combined_companies.append(company_copy)
        
        # Add admin companies with their products
        for company in self.companies.values():
            company_copy = company.copy()
            company_copy['source'] = 'admin'
            company_copy['products'] = self.get_products_by_company(company['id'])
            combined_companies.append(company_copy)
        
        return {'companies': combined_companies}

# Global instance
admin_db = AdminDatabase()
