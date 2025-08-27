"""
Sales Analytics Service for Catalog AI

This service provides comprehensive sales data analysis capabilities including:
- Data loading and caching
- Basic aggregations (sum, average, growth rate)
- Sector-based filtering logic
- Time-period calculations (monthly, quarterly, yearly)
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SalesRecord:
    """Data class for sales record"""
    period: str
    units_sold: int
    revenue: float
    currency: str
    growth_rate: float
    market_share: float


@dataclass
class SalesData:
    """Data class for complete sales data entry"""
    product_id: str
    company: str
    sector: str
    region: str
    sales_records: List[SalesRecord]
    metadata: Dict[str, Any]


class SalesAnalyticsService:
    """Main service class for sales analytics operations"""
    
    def __init__(self, data_file_path: str = 'data/sales_data.json'):
        """
        Initialize the sales analytics service
        
        Args:
            data_file_path: Path to the sales data JSON file
        """
        self.data_file_path = data_file_path
        self._cache = {}
        self._cache_timestamp = None
        self._cache_ttl = 300  # 5 minutes cache TTL
        self.data = None
        self.validation_schema = None
        
        # Load initial data
        self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """
        Load sales data from JSON file with caching
        
        Returns:
            Dict containing sales data
        """
        try:
            # Check if cache is still valid
            if (self._cache_timestamp and 
                datetime.now() - self._cache_timestamp < timedelta(seconds=self._cache_ttl) and
                self.data):
                logger.info("Using cached sales data")
                return self.data
            
            # Load fresh data
            if not os.path.exists(self.data_file_path):
                logger.warning(f"Sales data file not found: {self.data_file_path}")
                return {"sales_data": [], "schema_version": "1.0", "metadata": {}}
            
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # Validate and process data
            self.data = self._process_raw_data(raw_data)
            self.validation_schema = raw_data.get('data_validation', {})
            self._cache_timestamp = datetime.now()
            
            logger.info(f"Loaded {len(self.data.get('sales_data', []))} sales records")
            return self.data
            
        except FileNotFoundError:
            logger.error(f"Sales data file not found: {self.data_file_path}")
            return {"sales_data": [], "schema_version": "1.0", "metadata": {}}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in sales data file: {e}")
            return {"sales_data": [], "schema_version": "1.0", "metadata": {}}
        except Exception as e:
            logger.error(f"Error loading sales data: {e}")
            return {"sales_data": [], "schema_version": "1.0", "metadata": {}}
    
    def _process_raw_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and validate raw data from JSON
        
        Args:
            raw_data: Raw data from JSON file
            
        Returns:
            Processed data with validation
        """
        processed_data = raw_data.copy()
        
        # Process sales records into structured objects
        sales_data = []
        for entry in raw_data.get('sales_data', []):
            try:
                # Convert sales records to SalesRecord objects
                sales_records = []
                for record in entry.get('sales_records', []):
                    sales_record = SalesRecord(
                        period=record['period'],
                        units_sold=record['units_sold'],
                        revenue=record['revenue'],
                        currency=record['currency'],
                        growth_rate=record['growth_rate'],
                        market_share=record['market_share']
                    )
                    sales_records.append(sales_record)
                
                # Create SalesData object
                sales_entry = SalesData(
                    product_id=entry['product_id'],
                    company=entry['company'],
                    sector=entry['sector'],
                    region=entry['region'],
                    sales_records=sales_records,
                    metadata=entry.get('metadata', {})
                )
                
                sales_data.append(sales_entry)
                
            except KeyError as e:
                logger.warning(f"Missing required field in sales entry: {e}")
                continue
            except Exception as e:
                logger.warning(f"Error processing sales entry: {e}")
                continue
        
        processed_data['sales_data'] = sales_data
        return processed_data
    
    def invalidate_cache(self):
        """Invalidate the data cache"""
        self._cache = {}
        self._cache_timestamp = None
        logger.info("Sales data cache invalidated")
    
    def reload_data(self):
        """Force reload of sales data"""
        self.invalidate_cache()
        return self._load_data()
    
    def get_sales_summary(self, 
                         product_id: Optional[str] = None,
                         sector: Optional[str] = None,
                         region: Optional[str] = None,
                         period_start: Optional[str] = None,
                         period_end: Optional[str] = None) -> Dict[str, Any]:
        """
        Get sales summary with optional filtering
        
        Args:
            product_id: Filter by specific product
            sector: Filter by sector
            region: Filter by region
            period_start: Start period (YYYY-MM format)
            period_end: End period (YYYY-MM format)
            
        Returns:
            Sales summary with aggregated metrics
        """
        try:
            data = self._load_data()
            filtered_data = self._filter_sales_data(
                data['sales_data'], product_id, sector, region, period_start, period_end
            )
            
            if not filtered_data:
                return {
                    'total_revenue': 0,
                    'total_units': 0,
                    'average_growth_rate': 0,
                    'total_records': 0,
                    'filters_applied': {
                        'product_id': product_id,
                        'sector': sector,
                        'region': region,
                        'period_start': period_start,
                        'period_end': period_end
                    }
                }
            
            # Calculate aggregations
            total_revenue = 0
            total_units = 0
            growth_rates = []
            record_count = 0
            
            for sales_entry in filtered_data:
                for record in sales_entry.sales_records:
                    # Apply period filtering
                    if period_start and record.period < period_start:
                        continue
                    if period_end and record.period > period_end:
                        continue
                    
                    total_revenue += record.revenue
                    total_units += record.units_sold
                    growth_rates.append(record.growth_rate)
                    record_count += 1
            
            average_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0
            
            return {
                'total_revenue': round(total_revenue, 2),
                'total_units': total_units,
                'average_growth_rate': round(average_growth, 2),
                'total_records': record_count,
                'unique_products': len(set(entry.product_id for entry in filtered_data)),
                'sectors_covered': len(set(entry.sector for entry in filtered_data)),
                'filters_applied': {
                    'product_id': product_id,
                    'sector': sector,
                    'region': region,
                    'period_start': period_start,
                    'period_end': period_end
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating sales summary: {e}")
            raise
    
    def _filter_sales_data(self, 
                          sales_data: List[SalesData],
                          product_id: Optional[str] = None,
                          sector: Optional[str] = None,
                          region: Optional[str] = None,
                          period_start: Optional[str] = None,
                          period_end: Optional[str] = None) -> List[SalesData]:
        """
        Filter sales data based on provided criteria
        
        Args:
            sales_data: List of SalesData objects
            product_id: Filter by product ID
            sector: Filter by sector
            region: Filter by region
            period_start: Start period filter
            period_end: End period filter
            
        Returns:
            Filtered list of SalesData objects
        """
        filtered_data = sales_data
        
        if product_id:
            filtered_data = [entry for entry in filtered_data if entry.product_id == product_id]
        
        if sector:
            filtered_data = [entry for entry in filtered_data if entry.sector.lower() == sector.lower()]
        
        if region:
            filtered_data = [entry for entry in filtered_data if entry.region.lower() == region.lower()]
        
        return filtered_data
    
    def get_sector_performance(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get performance metrics by sector
        
        Args:
            region: Optional region filter
            
        Returns:
            List of sector performance metrics
        """
        try:
            data = self._load_data()
            filtered_data = self._filter_sales_data(data['sales_data'], region=region)
            
            # Group by sector
            sector_data = {}
            for sales_entry in filtered_data:
                sector = sales_entry.sector
                if sector not in sector_data:
                    sector_data[sector] = {
                        'total_revenue': 0,
                        'total_units': 0,
                        'growth_rates': [],
                        'market_shares': [],
                        'product_count': 0,
                        'products': set()
                    }
                
                sector_data[sector]['products'].add(sales_entry.product_id)
                
                for record in sales_entry.sales_records:
                    sector_data[sector]['total_revenue'] += record.revenue
                    sector_data[sector]['total_units'] += record.units_sold
                    sector_data[sector]['growth_rates'].append(record.growth_rate)
                    sector_data[sector]['market_shares'].append(record.market_share)
            
            # Calculate final metrics
            sector_performance = []
            for sector, metrics in sector_data.items():
                avg_growth = sum(metrics['growth_rates']) / len(metrics['growth_rates']) if metrics['growth_rates'] else 0
                avg_market_share = sum(metrics['market_shares']) / len(metrics['market_shares']) if metrics['market_shares'] else 0
                
                sector_performance.append({
                    'sector': sector,
                    'total_revenue': round(metrics['total_revenue'], 2),
                    'total_units': metrics['total_units'],
                    'average_growth_rate': round(avg_growth, 2),
                    'average_market_share': round(avg_market_share, 2),
                    'product_count': len(metrics['products']),
                    'products': list(metrics['products'])
                })
            
            # Sort by total revenue (descending)
            sector_performance.sort(key=lambda x: x['total_revenue'], reverse=True)
            
            return sector_performance
            
        except Exception as e:
            logger.error(f"Error calculating sector performance: {e}")
            raise
    
    def get_trend_analysis(self, 
                          product_id: str,
                          analysis_type: str = 'monthly') -> Dict[str, Any]:
        """
        Get trend analysis for a specific product
        
        Args:
            product_id: Product ID to analyze
            analysis_type: Type of analysis ('monthly', 'quarterly', 'yearly')
            
        Returns:
            Trend analysis data
        """
        try:
            data = self._load_data()
            product_data = self._filter_sales_data(data['sales_data'], product_id=product_id)
            
            if not product_data:
                raise ValueError(f"No data found for product: {product_id}")
            
            # Combine all sales records for the product across sectors/regions
            all_records = []
            for sales_entry in product_data:
                all_records.extend(sales_entry.sales_records)
            
            # Sort by period
            all_records.sort(key=lambda x: x.period)
            
            # Calculate trends
            trend_data = []
            for i, record in enumerate(all_records):
                trend_point = {
                    'period': record.period,
                    'revenue': record.revenue,
                    'units_sold': record.units_sold,
                    'growth_rate': record.growth_rate,
                    'market_share': record.market_share
                }
                
                # Calculate moving averages if we have enough data
                if i >= 2:  # 3-period moving average
                    recent_records = all_records[max(0, i-2):i+1]
                    trend_point['revenue_3ma'] = sum(r.revenue for r in recent_records) / len(recent_records)
                    trend_point['units_3ma'] = sum(r.units_sold for r in recent_records) / len(recent_records)
                
                trend_data.append(trend_point)
            
            # Calculate overall trend metrics
            if len(all_records) >= 2:
                total_growth = ((all_records[-1].revenue - all_records[0].revenue) / all_records[0].revenue) * 100
                avg_monthly_growth = sum(r.growth_rate for r in all_records) / len(all_records)
            else:
                total_growth = 0
                avg_monthly_growth = 0
            
            return {
                'product_id': product_id,
                'analysis_type': analysis_type,
                'period_range': {
                    'start': all_records[0].period if all_records else None,
                    'end': all_records[-1].period if all_records else None
                },
                'trend_data': trend_data,
                'summary_metrics': {
                    'total_growth_percentage': round(total_growth, 2),
                    'average_monthly_growth': round(avg_monthly_growth, 2),
                    'total_periods': len(all_records),
                    'latest_revenue': all_records[-1].revenue if all_records else 0,
                    'latest_units': all_records[-1].units_sold if all_records else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating trend analysis: {e}")
            raise
    
    def validate_data_quality(self) -> Dict[str, Any]:
        """
        Validate data quality and return quality metrics
        
        Returns:
            Data quality assessment
        """
        try:
            data = self._load_data()
            validation_results = {
                'overall_score': 0,
                'issues': [],
                'metrics': {
                    'total_records': 0,
                    'complete_records': 0,
                    'missing_fields': 0,
                    'invalid_values': 0
                },
                'recommendations': []
            }
            
            sales_data = data.get('sales_data', [])
            validation_results['metrics']['total_records'] = len(sales_data)
            
            # Check required fields and data quality
            required_fields = self.validation_schema.get('required_fields', [])
            sales_record_fields = self.validation_schema.get('sales_record_fields', [])
            
            complete_records = 0
            for entry in sales_data:
                entry_complete = True
                
                # Check main fields
                for field in required_fields:
                    if not hasattr(entry, field) or getattr(entry, field) is None:
                        validation_results['metrics']['missing_fields'] += 1
                        validation_results['issues'].append(f"Missing {field} in product {getattr(entry, 'product_id', 'unknown')}")
                        entry_complete = False
                
                # Check sales records
                for record in entry.sales_records:
                    for field in sales_record_fields:
                        if not hasattr(record, field) or getattr(record, field) is None:
                            validation_results['metrics']['missing_fields'] += 1
                            validation_results['issues'].append(f"Missing {field} in sales record for {entry.product_id}")
                            entry_complete = False
                        
                        # Validate specific field types
                        if field in ['units_sold'] and hasattr(record, field):
                            if getattr(record, field) < 0:
                                validation_results['metrics']['invalid_values'] += 1
                                validation_results['issues'].append(f"Negative units_sold in {entry.product_id}")
                                entry_complete = False
                        
                        if field in ['revenue'] and hasattr(record, field):
                            if getattr(record, field) < 0:
                                validation_results['metrics']['invalid_values'] += 1
                                validation_results['issues'].append(f"Negative revenue in {entry.product_id}")
                                entry_complete = False
                
                if entry_complete:
                    complete_records += 1
            
            validation_results['metrics']['complete_records'] = complete_records
            
            # Calculate overall score
            if validation_results['metrics']['total_records'] > 0:
                completeness_score = (complete_records / validation_results['metrics']['total_records']) * 100
                validation_results['overall_score'] = completeness_score
            
            # Generate recommendations
            if validation_results['metrics']['missing_fields'] > 0:
                validation_results['recommendations'].append("Address missing required fields in sales data")
            
            if validation_results['metrics']['invalid_values'] > 0:
                validation_results['recommendations'].append("Fix invalid values (negative numbers, etc.)")
            
            if validation_results['overall_score'] < 90:
                validation_results['recommendations'].append("Improve data quality to achieve >90% completeness")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error validating data quality: {e}")
            raise
