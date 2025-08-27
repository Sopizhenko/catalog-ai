"""
Market Analysis Service
Provides market intelligence, competitive analysis, and cross-selling recommendations
"""

import json
import datetime
from typing import Dict, List, Any

class MarketAnalysisService:
    def __init__(self):
        self.market_data = self._load_market_data()
        self.competitor_data = self._load_competitor_data()
        
    def _load_market_data(self) -> Dict:
        """Load market intelligence data"""
        return {
            "Point of Sale Software": {
                "market_size": {"global": "$19.6B", "europe": "$4.2B"},
                "growth_rate": "11.9% CAGR (2023-2030)",
                "key_trends": [
                    "Cloud-based solutions adoption",
                    "Mobile payment integration",
                    "AI-powered analytics",
                    "Omnichannel commerce",
                    "Contactless payments"
                ],
                "market_drivers": [
                    "Digital transformation in retail",
                    "Growth of e-commerce",
                    "Need for real-time analytics",
                    "Customer experience enhancement"
                ],
                "challenges": [
                    "Data security concerns",
                    "Integration complexity",
                    "High switching costs",
                    "Regulatory compliance"
                ]
            },
            "ERP Software": {
                "market_size": {"global": "$35.8B", "europe": "$8.9B"},
                "growth_rate": "13.4% CAGR (2023-2030)",
                "key_trends": [
                    "Cloud ERP adoption",
                    "AI and ML integration",
                    "Industry-specific solutions",
                    "Mobile-first design",
                    "Low-code/no-code platforms"
                ],
                "market_drivers": [
                    "Business process automation",
                    "Real-time data insights",
                    "Scalability requirements",
                    "Cost optimization"
                ],
                "challenges": [
                    "Implementation complexity",
                    "Change management",
                    "Data migration issues",
                    "Vendor lock-in concerns"
                ]
            },
            "CRM Software": {
                "market_size": {"global": "$58.2B", "europe": "$12.1B"},
                "growth_rate": "12.1% CAGR (2023-2030)",
                "key_trends": [
                    "AI-powered customer insights",
                    "Social CRM integration",
                    "Predictive analytics",
                    "Voice and chatbot integration",
                    "Customer journey mapping"
                ],
                "market_drivers": [
                    "Customer-centric business models",
                    "Sales automation needs",
                    "Data-driven decision making",
                    "Remote work trends"
                ],
                "challenges": [
                    "Data quality issues",
                    "User adoption",
                    "Integration complexity",
                    "Privacy regulations"
                ]
            }
        }
    
    def _load_competitor_data(self) -> Dict:
        """Load competitive intelligence data"""
        return {
            "Point of Sale": {
                "major_players": [
                    {
                        "name": "Square",
                        "market_share": "28.5%",
                        "strengths": ["Easy setup", "Integrated payments", "Strong mobile app"],
                        "weaknesses": ["Limited advanced features", "Transaction fees"],
                        "key_products": ["Square POS", "Square Register"],
                        "target_market": "Small to medium businesses",
                        "pricing_model": "Transaction-based fees"
                    },
                    {
                        "name": "Shopify POS",
                        "market_share": "22.1%",
                        "strengths": ["E-commerce integration", "Scalable", "Great for online-to-offline"],
                        "weaknesses": ["Complex for beginners", "Higher costs"],
                        "key_products": ["Shopify POS", "Shopify Plus"],
                        "target_market": "E-commerce focused retailers",
                        "pricing_model": "Subscription + transaction fees"
                    },
                    {
                        "name": "Toast",
                        "market_share": "15.3%",
                        "strengths": ["Restaurant focused", "Comprehensive features", "Good analytics"],
                        "weaknesses": ["Expensive", "Complex setup"],
                        "key_products": ["Toast POS", "Toast Online Ordering"],
                        "target_market": "Restaurants and food service",
                        "pricing_model": "Subscription-based"
                    }
                ]
            },
            "ERP": {
                "major_players": [
                    {
                        "name": "SAP",
                        "market_share": "24.2%",
                        "strengths": ["Enterprise-grade", "Comprehensive modules", "Strong integration"],
                        "weaknesses": ["Complex implementation", "High costs", "Steep learning curve"],
                        "key_products": ["SAP S/4HANA", "SAP Business One"],
                        "target_market": "Large enterprises",
                        "pricing_model": "License + maintenance"
                    },
                    {
                        "name": "Oracle",
                        "market_share": "18.7%",
                        "strengths": ["Cloud-native", "AI capabilities", "Scalable"],
                        "weaknesses": ["Expensive", "Complex licensing"],
                        "key_products": ["Oracle Cloud ERP", "Oracle NetSuite"],
                        "target_market": "Medium to large enterprises",
                        "pricing_model": "Subscription-based"
                    },
                    {
                        "name": "Microsoft Dynamics",
                        "market_share": "15.2%",
                        "strengths": ["Office integration", "User-friendly", "Flexible deployment"],
                        "weaknesses": ["Limited customization", "Module dependencies"],
                        "key_products": ["Dynamics 365", "Dynamics GP"],
                        "target_market": "Small to medium enterprises",
                        "pricing_model": "Subscription per user"
                    }
                ]
            }
        }
    
    def get_market_analysis(self, industry: str) -> Dict[str, Any]:
        """Get comprehensive market analysis for an industry"""
        market_info = self.market_data.get(industry, {})
        competitor_info = self.competitor_data.get(industry.split()[0], {})  # Use first word for matching
        
        return {
            "industry": industry,
            "market_overview": market_info,
            "competitive_landscape": competitor_info,
            "analysis_date": datetime.datetime.now().isoformat(),
            "recommendations": self._generate_market_recommendations(industry, market_info, competitor_info)
        }
    
    def get_company_competitive_position(self, company_name: str, industry: str) -> Dict[str, Any]:
        """Analyze a company's competitive position"""
        market_info = self.market_data.get(industry, {})
        competitors = self.competitor_data.get(industry.split()[0], {}).get("major_players", [])
        
        # Generate positioning analysis
        positioning = self._analyze_company_positioning(company_name, industry, competitors)
        
        return {
            "company": company_name,
            "industry": industry,
            "positioning": positioning,
            "market_opportunities": self._identify_opportunities(company_name, market_info),
            "competitive_threats": self._identify_threats(company_name, competitors),
            "analysis_date": datetime.datetime.now().isoformat()
        }
    
    def get_product_competitive_analysis(self, product_data: Dict, category: str) -> Dict[str, Any]:
        """Analyze product against competitors"""
        competitors = self.competitor_data.get(category, {}).get("major_players", [])
        
        return {
            "product": product_data.get("name"),
            "category": category,
            "competitive_comparison": self._compare_product_features(product_data, competitors),
            "pricing_analysis": self._analyze_pricing_position(product_data, competitors),
            "differentiation_opportunities": self._identify_differentiation(product_data, competitors),
            "analysis_date": datetime.datetime.now().isoformat()
        }
    
    def get_cross_selling_recommendations(self, company_data: Dict, all_companies: List[Dict]) -> Dict[str, Any]:
        """Generate cross-selling recommendations within company groups"""
        parent_company = company_data.get("parentCompany")
        current_products = company_data.get("products", [])
        
        # Find related companies in the same group
        group_companies = [
            c for c in all_companies 
            if c.get("parentCompany") == parent_company and c["company"] != company_data["company"]
        ] if parent_company else []
        
        recommendations = self._generate_cross_selling_recommendations(
            current_products, group_companies
        )
        
        return {
            "company": company_data["company"],
            "parent_company": parent_company,
            "cross_selling_opportunities": recommendations,
            "group_companies": [c["company"] for c in group_companies],
            "analysis_date": datetime.datetime.now().isoformat()
        }
    
    def _generate_market_recommendations(self, industry: str, market_info: Dict, competitor_info: Dict) -> List[str]:
        """Generate strategic recommendations based on market analysis"""
        recommendations = []
        
        if "trends" in market_info.get("key_trends", []):
            recommendations.append("Focus on cloud-based solutions to align with market trends")
            recommendations.append("Invest in AI/ML capabilities for competitive advantage")
        
        if competitor_info.get("major_players"):
            recommendations.append("Differentiate through specialized industry features")
            recommendations.append("Consider partnership opportunities with complementary vendors")
        
        recommendations.extend([
            "Develop mobile-first solutions for better user adoption",
            "Implement robust security measures to address market concerns",
            "Create industry-specific workflows to stand out from generic solutions"
        ])
        
        return recommendations
    
    def _analyze_company_positioning(self, company_name: str, industry: str, competitors: List[Dict]) -> Dict[str, Any]:
        """Analyze company's market positioning"""
        return {
            "market_segment": "Mid-market specialized solutions",
            "competitive_advantages": [
                "Industry-specific features",
                "Flexible deployment options",
                "Strong customer support",
                "Competitive pricing"
            ],
            "areas_for_improvement": [
                "Brand recognition",
                "Market penetration",
                "Feature breadth",
                "Integration ecosystem"
            ],
            "positioning_score": 7.2,  # Out of 10
            "market_presence": "Growing regional player"
        }
    
    def _identify_opportunities(self, company_name: str, market_info: Dict) -> List[str]:
        """Identify market opportunities"""
        return [
            "Expand into emerging markets with high growth potential",
            "Develop AI-powered analytics features",
            "Create mobile-first solutions for remote work trends",
            "Build integration partnerships with major platforms",
            "Target underserved niche markets"
        ]
    
    def _identify_threats(self, company_name: str, competitors: List[Dict]) -> List[str]:
        """Identify competitive threats"""
        return [
            "Large players with extensive resources entering market",
            "Price competition from low-cost providers",
            "Technology disruption from emerging platforms",
            "Customer consolidation reducing market size",
            "Regulatory changes affecting business models"
        ]
    
    def _compare_product_features(self, product: Dict, competitors: List[Dict]) -> List[Dict]:
        """Compare product features against competitors"""
        comparisons = []
        product_features = set(product.get("features", []))
        
        for competitor in competitors[:3]:  # Top 3 competitors
            comparison = {
                "competitor": competitor["name"],
                "feature_overlap": len(product_features.intersection(set(competitor.get("key_products", [])))),
                "unique_features": list(product_features - set(competitor.get("key_products", []))),
                "missing_features": ["Advanced analytics", "Multi-location support", "Custom reporting"],
                "competitive_score": 7.5  # Out of 10
            }
            comparisons.append(comparison)
        
        return comparisons
    
    def _analyze_pricing_position(self, product: Dict, competitors: List[Dict]) -> Dict[str, Any]:
        """Analyze pricing position vs competitors"""
        product_price = product.get("pricing", {}).get("startingPrice", 0)
        
        return {
            "current_price": product_price,
            "market_position": "Competitive" if product_price < 150 else "Premium",
            "price_recommendations": [
                "Consider value-based pricing tiers",
                "Offer volume discounts for enterprise customers",
                "Bundle additional services for higher value"
            ],
            "pricing_flexibility": "High"
        }
    
    def _identify_differentiation(self, product: Dict, competitors: List[Dict]) -> List[str]:
        """Identify differentiation opportunities"""
        return [
            "Develop industry-specific workflows",
            "Enhance user experience and interface design",
            "Create advanced automation features",
            "Build comprehensive integration ecosystem",
            "Offer superior customer support and training"
        ]
    
    def _generate_cross_selling_recommendations(self, current_products: List[Dict], group_companies: List[Dict]) -> List[Dict]:
        """Generate cross-selling recommendations"""
        recommendations = []
        current_categories = set(p.get("category", "") for p in current_products)
        
        for company in group_companies:
            company_products = company.get("products", [])
            complementary_products = []
            
            for product in company_products:
                product_category = product.get("category", "")
                if product_category not in current_categories:
                    complementary_products.append({
                        "product_name": product.get("name"),
                        "category": product_category,
                        "synergy_score": self._calculate_synergy_score(current_categories, product_category),
                        "cross_sell_potential": "High" if product_category in ["ERP", "CRM", "Analytics"] else "Medium"
                    })
            
            if complementary_products:
                recommendations.append({
                    "company": company["company"],
                    "complementary_products": complementary_products,
                    "partnership_opportunities": [
                        "Joint sales campaigns",
                        "Integrated solution packages",
                        "Cross-training sales teams",
                        "Shared customer success programs"
                    ]
                })
        
        return recommendations
    
    def _calculate_synergy_score(self, current_categories: set, new_category: str) -> float:
        """Calculate synergy score between product categories"""
        synergy_matrix = {
            ("Point of Sale", "ERP"): 9.0,
            ("Point of Sale", "CRM"): 8.5,
            ("Point of Sale", "Inventory Management"): 9.5,
            ("ERP", "CRM"): 8.0,
            ("CRM", "Marketing Automation"): 9.0,
            ("ERP", "Analytics"): 8.5
        }
        
        max_score = 0.0
        for current_cat in current_categories:
            score = synergy_matrix.get((current_cat, new_category), 5.0)
            max_score = max(max_score, score)
        
        return max_score
