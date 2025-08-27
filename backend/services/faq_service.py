import json
import os
from typing import List, Dict, Optional

class FAQService:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faqs.json')
        self._load_data()
    
    def _load_data(self):
        """Load FAQ data from JSON file"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.faqs = data.get('faqs', [])
                self.categories = data.get('categories', [])
        except FileNotFoundError:
            self.faqs = []
            self.categories = []
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in FAQ data file: {e}")
    
    def get_faqs(self, search_query: str = '', category_id: str = '', limit: Optional[int] = None) -> List[Dict]:
        """Get filtered FAQs"""
        results = self.faqs.copy()
        
        # Filter by category
        if category_id:
            results = [faq for faq in results if faq.get('categoryId') == category_id]
        
        # Filter by search query
        if search_query:
            query_lower = search_query.lower()
            filtered_results = []
            
            for faq in results:
                # Search in question, answer, keywords, and search terms
                searchable_text = ' '.join([
                    faq.get('question', ''),
                    faq.get('answer', ''),
                    ' '.join(faq.get('keywords', [])),
                    ' '.join(faq.get('searchTerms', []))
                ]).lower()
                
                if query_lower in searchable_text:
                    filtered_results.append(faq)
            
            results = filtered_results
        
        # Apply limit
        if limit:
            results = results[:limit]
        
        # Enrich with category information
        for faq in results:
            category = next((cat for cat in self.categories if cat['id'] == faq.get('categoryId')), None)
            if category:
                faq['categoryName'] = category['name']
        
        return results
    
    def get_faq_by_id(self, faq_id: str) -> Optional[Dict]:
        """Get specific FAQ by ID"""
        faq = next((f for f in self.faqs if f['id'] == faq_id), None)
        
        if faq:
            # Enrich with category information
            category = next((cat for cat in self.categories if cat['id'] == faq.get('categoryId')), None)
            if category:
                faq['categoryName'] = category['name']
        
        return faq
    
    def get_categories(self) -> List[Dict]:
        """Get all categories with FAQ counts"""
        categories_with_counts = []
        
        for category in self.categories:
            faq_count = len([faq for faq in self.faqs if faq.get('categoryId') == category['id']])
            category_with_count = category.copy()
            category_with_count['faqCount'] = faq_count
            categories_with_counts.append(category_with_count)
        
        return categories_with_counts
    
    def advanced_search(self, query: str, filters: Dict) -> List[Dict]:
        """Advanced search with multiple filters"""
        results = self.faqs.copy()
        
        # Apply category filter
        if filters.get('category'):
            results = [faq for faq in results if faq.get('categoryId') == filters['category']]
        
        # Apply keyword filter
        if filters.get('keywords'):
            keyword_filter = [kw.lower() for kw in filters['keywords']]
            results = [
                faq for faq in results 
                if any(kw in ' '.join(faq.get('keywords', [])).lower() for kw in keyword_filter)
            ]
        
        # Apply text search
        if query:
            query_lower = query.lower()
            scored_results = []
            
            for faq in results:
                score = 0
                
                # Score based on query location
                if query_lower in faq.get('question', '').lower():
                    score += 10
                if query_lower in faq.get('answer', '').lower():
                    score += 5
                if any(query_lower in kw.lower() for kw in faq.get('keywords', [])):
                    score += 8
                if any(query_lower in term.lower() for term in faq.get('searchTerms', [])):
                    score += 6
                
                if score > 0:
                    faq_copy = faq.copy()
                    faq_copy['searchScore'] = score
                    scored_results.append(faq_copy)
            
            # Sort by score descending
            results = sorted(scored_results, key=lambda x: x['searchScore'], reverse=True)
        
        return results
    
    def get_related_content(self, faq_id: str) -> Dict:
        """Get related companies and products for FAQ cross-referencing"""
        faq = self.get_faq_by_id(faq_id)
        if not faq:
            return {}
        
        # This method demonstrates how FAQ integrates with catalog data
        # Load company data (reusing existing data loading patterns)
        try:
            company_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'companies.json')
            with open(company_data_path, 'r', encoding='utf-8') as f:
                company_data = json.load(f)
            
            companies = company_data.get('companies', [])
            
            related_companies = []
            related_products = []
            
            # Find companies/products mentioned in FAQ keywords
            faq_keywords = [kw.lower() for kw in faq.get('keywords', [])]
            
            for company in companies:
                # Check if company is mentioned in FAQ
                company_terms = [
                    company.get('company', '').lower(),
                    company.get('parentCompany', '').lower()
                ]
                
                if any(term for term in company_terms if term and any(kw in term for kw in faq_keywords)):
                    related_companies.append({
                        'company': company.get('company'),
                        'description': company.get('description', ''),
                        'industry': company.get('industry', '')
                    })
                
                # Check products
                for product in company.get('products', []):
                    product_terms = [
                        product.get('name', '').lower(),
                        product.get('category', '').lower()
                    ] + [feature.lower() for feature in product.get('features', [])]
                    
                    if any(term for term in product_terms if term and any(kw in term for kw in faq_keywords)):
                        related_products.append({
                            'id': product.get('id'),
                            'name': product.get('name'),
                            'company': company.get('company'),
                            'category': product.get('category', ''),
                            'description': product.get('description', '')
                        })
            
            return {
                'companies': related_companies[:5],  # Limit to 5 most relevant
                'products': related_products[:5]
            }
            
        except Exception as e:
            print(f"Error loading related content: {e}")
            return {'companies': [], 'products': []}
    
    def track_search(self, query: str, result_count: int):
        """Track search analytics (implement as needed)"""
        # This could log to a file, database, or analytics service
        print(f"FAQ Search: '{query}' returned {result_count} results")
