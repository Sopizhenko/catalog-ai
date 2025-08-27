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
        
        # Performance optimization caches
        self._analytics_cache = {}
        self._analytics_cache_ttl = 180  # 3 minutes for analytics cache
        self._analytics_cache_timestamp = {}
        
        # Simulated indexing for faster queries
        self._product_index = {}
        self._sector_index = {}
        self._region_index = {}
        self._period_index = {}
        
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
            
            # Build indexes for performance optimization
            self._build_indexes()
            
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
        self._analytics_cache = {}
        self._analytics_cache_timestamp = {}
        logger.info("Sales data cache invalidated")
    
    def _build_indexes(self):
        """
        Build indexes for performance optimization
        """
        if not self.data or not self.data.get('sales_data'):
            return
        
        # Reset indexes
        self._product_index = {}
        self._sector_index = {}
        self._region_index = {}
        self._period_index = {}
        
        for i, sales_entry in enumerate(self.data['sales_data']):
            # Product index
            product_id = sales_entry.product_id
            if product_id not in self._product_index:
                self._product_index[product_id] = []
            self._product_index[product_id].append(i)
            
            # Sector index
            sector = sales_entry.sector
            if sector not in self._sector_index:
                self._sector_index[sector] = []
            self._sector_index[sector].append(i)
            
            # Region index
            region = sales_entry.region
            if region not in self._region_index:
                self._region_index[region] = []
            self._region_index[region].append(i)
            
            # Period index (for all sales records within this entry)
            for record in sales_entry.sales_records:
                period = record.period
                if period not in self._period_index:
                    self._period_index[period] = []
                self._period_index[period].append((i, record))
        
        logger.info(f"Built indexes: {len(self._product_index)} products, {len(self._sector_index)} sectors, {len(self._region_index)} regions, {len(self._period_index)} periods")
    
    def _get_analytics_cache_key(self, method_name: str, **kwargs) -> str:
        """
        Generate cache key for analytics methods
        
        Args:
            method_name: Name of the analytics method
            **kwargs: Parameters used in the method
            
        Returns:
            Cache key string
        """
        # Sort kwargs for consistent key generation
        sorted_params = sorted(kwargs.items())
        params_str = '_'.join(f"{k}:{v}" for k, v in sorted_params if v is not None)
        return f"{method_name}_{params_str}"
    
    def _get_cached_analytics(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Get cached analytics result if available and not expired
        
        Args:
            cache_key: Cache key to look up
            
        Returns:
            Cached result or None if not available/expired
        """
        if cache_key not in self._analytics_cache:
            return None
        
        cache_time = self._analytics_cache_timestamp.get(cache_key)
        if not cache_time:
            return None
        
        # Check if cache is expired
        if datetime.now() - cache_time > timedelta(seconds=self._analytics_cache_ttl):
            # Remove expired cache
            del self._analytics_cache[cache_key]
            del self._analytics_cache_timestamp[cache_key]
            return None
        
        return self._analytics_cache[cache_key]
    
    def _set_cached_analytics(self, cache_key: str, result: Dict[str, Any]):
        """
        Cache analytics result
        
        Args:
            cache_key: Cache key
            result: Result to cache
        """
        self._analytics_cache[cache_key] = result
        self._analytics_cache_timestamp[cache_key] = datetime.now()
    
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
            
            # Calculate advanced trends
            trend_data = []
            for i, record in enumerate(all_records):
                trend_point = {
                    'period': record.period,
                    'revenue': record.revenue,
                    'units_sold': record.units_sold,
                    'growth_rate': record.growth_rate,
                    'market_share': record.market_share
                }
                
                # Calculate month-over-month growth
                if i > 0:
                    prev_record = all_records[i-1]
                    trend_point['mom_revenue_growth'] = ((record.revenue - prev_record.revenue) / prev_record.revenue * 100) if prev_record.revenue > 0 else 0
                    trend_point['mom_units_growth'] = ((record.units_sold - prev_record.units_sold) / prev_record.units_sold * 100) if prev_record.units_sold > 0 else 0
                
                # Calculate quarter-over-quarter growth (if we have 3+ months data)
                if i >= 3:
                    quarter_ago = all_records[i-3]
                    trend_point['qoq_revenue_growth'] = ((record.revenue - quarter_ago.revenue) / quarter_ago.revenue * 100) if quarter_ago.revenue > 0 else 0
                    trend_point['qoq_units_growth'] = ((record.units_sold - quarter_ago.units_sold) / quarter_ago.units_sold * 100) if quarter_ago.units_sold > 0 else 0
                
                # Calculate year-over-year growth (if we have 12+ months data)
                if i >= 12:
                    year_ago = all_records[i-12]
                    trend_point['yoy_revenue_growth'] = ((record.revenue - year_ago.revenue) / year_ago.revenue * 100) if year_ago.revenue > 0 else 0
                    trend_point['yoy_units_growth'] = ((record.units_sold - year_ago.units_sold) / year_ago.units_sold * 100) if year_ago.units_sold > 0 else 0
                
                # Calculate moving averages
                if i >= 2:  # 3-month moving average
                    recent_3 = all_records[max(0, i-2):i+1]
                    trend_point['revenue_3ma'] = sum(r.revenue for r in recent_3) / len(recent_3)
                    trend_point['units_3ma'] = sum(r.units_sold for r in recent_3) / len(recent_3)
                
                if i >= 5:  # 6-month moving average
                    recent_6 = all_records[max(0, i-5):i+1]
                    trend_point['revenue_6ma'] = sum(r.revenue for r in recent_6) / len(recent_6)
                    trend_point['units_6ma'] = sum(r.units_sold for r in recent_6) / len(recent_6)
                
                if i >= 11:  # 12-month moving average
                    recent_12 = all_records[max(0, i-11):i+1]
                    trend_point['revenue_12ma'] = sum(r.revenue for r in recent_12) / len(recent_12)
                    trend_point['units_12ma'] = sum(r.units_sold for r in recent_12) / len(recent_12)
                
                # Seasonal adjustment (simple method)
                trend_point['seasonal_adjusted_revenue'] = self._calculate_seasonal_adjustment(all_records, i, 'revenue')
                trend_point['seasonal_adjusted_units'] = self._calculate_seasonal_adjustment(all_records, i, 'units_sold')
                
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
    
    def _calculate_seasonal_adjustment(self, all_records: List[SalesRecord], current_index: int, field: str) -> float:
        """
        Calculate seasonal adjustment for a given field
        
        Args:
            all_records: All sales records for the product
            current_index: Current record index
            field: Field to adjust ('revenue' or 'units_sold')
            
        Returns:
            Seasonally adjusted value
        """
        if current_index < 12:  # Not enough data for seasonal adjustment
            return getattr(all_records[current_index], field)
        
        # Simple seasonal adjustment using 12-month average
        current_value = getattr(all_records[current_index], field)
        
        # Get same month values from previous years
        same_month_values = []
        for i in range(current_index - 12, -1, -12):
            if i >= 0:
                same_month_values.append(getattr(all_records[i], field))
        
        if len(same_month_values) >= 2:
            seasonal_factor = sum(same_month_values) / len(same_month_values)
            overall_average = sum(getattr(r, field) for r in all_records[:current_index+1]) / (current_index + 1)
            
            if overall_average > 0 and seasonal_factor > 0:
                adjustment_factor = overall_average / seasonal_factor
                return current_value * adjustment_factor
        
        return current_value
    
    def get_sector_analysis_advanced(self, region: Optional[str] = None, time_period: Optional[str] = None) -> Dict[str, Any]:
        """
        Get advanced sector analysis with rankings, market share, and growth rates
        
        Args:
            region: Optional region filter
            time_period: Optional time period filter (latest_quarter, latest_year, etc.)
            
        Returns:
            Advanced sector analysis data
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
                        'products': set(),
                        'monthly_revenue': {},
                        'monthly_units': {}
                    }
                
                sector_data[sector]['products'].add(sales_entry.product_id)
                
                for record in sales_entry.sales_records:
                    # Apply time period filter if specified
                    if time_period and not self._is_in_time_period(record.period, time_period):
                        continue
                    
                    sector_data[sector]['total_revenue'] += record.revenue
                    sector_data[sector]['total_units'] += record.units_sold
                    sector_data[sector]['growth_rates'].append(record.growth_rate)
                    sector_data[sector]['market_shares'].append(record.market_share)
                    
                    # Track monthly data for trend calculation
                    if record.period not in sector_data[sector]['monthly_revenue']:
                        sector_data[sector]['monthly_revenue'][record.period] = 0
                        sector_data[sector]['monthly_units'][record.period] = 0
                    
                    sector_data[sector]['monthly_revenue'][record.period] += record.revenue
                    sector_data[sector]['monthly_units'][record.period] += record.units_sold
            
            # Calculate sector metrics and rankings
            sector_performance = []
            total_market_revenue = sum(metrics['total_revenue'] for metrics in sector_data.values())
            
            for sector, metrics in sector_data.items():
                avg_growth = sum(metrics['growth_rates']) / len(metrics['growth_rates']) if metrics['growth_rates'] else 0
                avg_market_share = sum(metrics['market_shares']) / len(metrics['market_shares']) if metrics['market_shares'] else 0
                
                # Calculate market penetration
                market_penetration = (metrics['total_revenue'] / total_market_revenue * 100) if total_market_revenue > 0 else 0
                
                # Calculate sector growth trend
                monthly_revenues = list(metrics['monthly_revenue'].values())
                if len(monthly_revenues) >= 2:
                    sector_growth_trend = ((monthly_revenues[-1] - monthly_revenues[0]) / monthly_revenues[0] * 100) if monthly_revenues[0] > 0 else 0
                else:
                    sector_growth_trend = 0
                
                sector_performance.append({
                    'sector': sector,
                    'total_revenue': round(metrics['total_revenue'], 2),
                    'total_units': metrics['total_units'],
                    'average_growth_rate': round(avg_growth, 2),
                    'average_market_share': round(avg_market_share, 2),
                    'market_penetration': round(market_penetration, 2),
                    'sector_growth_trend': round(sector_growth_trend, 2),
                    'product_count': len(metrics['products']),
                    'products': list(metrics['products']),
                    'performance_ranking': 0  # Will be set after sorting
                })
            
            # Sort and rank sectors
            sector_performance.sort(key=lambda x: x['total_revenue'], reverse=True)
            for i, sector in enumerate(sector_performance):
                sector['performance_ranking'] = i + 1
            
            return {
                'sectors': sector_performance,
                'total_sectors': len(sector_performance),
                'market_overview': {
                    'total_market_revenue': round(total_market_revenue, 2),
                    'top_sector': sector_performance[0]['sector'] if sector_performance else None,
                    'most_diverse_sector': max(sector_performance, key=lambda x: x['product_count'])['sector'] if sector_performance else None,
                    'fastest_growing_sector': max(sector_performance, key=lambda x: x['sector_growth_trend'])['sector'] if sector_performance else None
                },
                'filters_applied': {
                    'region': region,
                    'time_period': time_period
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating advanced sector analysis: {e}")
            raise
    
    def _is_in_time_period(self, period: str, time_period_filter: str) -> bool:
        """
        Check if a period falls within the specified time period filter
        
        Args:
            period: Period string (YYYY-MM format)
            time_period_filter: Time period filter (latest_quarter, latest_year, etc.)
            
        Returns:
            True if period is within the filter range
        """
        if not time_period_filter:
            return True
        
        try:
            from datetime import datetime, timedelta
            period_date = datetime.strptime(period, '%Y-%m')
            current_date = datetime.now()
            
            if time_period_filter == 'latest_quarter':
                # Last 3 months
                cutoff_date = current_date - timedelta(days=90)
                return period_date >= cutoff_date
            elif time_period_filter == 'latest_year':
                # Last 12 months
                cutoff_date = current_date - timedelta(days=365)
                return period_date >= cutoff_date
            elif time_period_filter == 'latest_6_months':
                # Last 6 months
                cutoff_date = current_date - timedelta(days=180)
                return period_date >= cutoff_date
            
            return True
        except:
            return True
    
    def get_product_performance_analytics(self, 
                                        sector: Optional[str] = None, 
                                        region: Optional[str] = None,
                                        limit: int = 10) -> Dict[str, Any]:
        """
        Get comprehensive product performance analytics
        
        Args:
            sector: Optional sector filter
            region: Optional region filter
            limit: Number of top/bottom products to return
            
        Returns:
            Product performance analytics data
        """
        try:
            data = self._load_data()
            filtered_data = self._filter_sales_data(data['sales_data'], sector=sector, region=region)
            
            if not filtered_data:
                return {
                    'top_performers': [],
                    'bottom_performers': [],
                    'lifecycle_analysis': [],
                    'cross_sector_performance': {},
                    'revenue_vs_units_analysis': []
                }
            
            # Calculate product metrics
            product_metrics = {}
            for sales_entry in filtered_data:
                product_id = sales_entry.product_id
                
                if product_id not in product_metrics:
                    product_metrics[product_id] = {
                        'product_id': product_id,
                        'company': sales_entry.company,
                        'sectors': set(),
                        'regions': set(),
                        'total_revenue': 0,
                        'total_units': 0,
                        'growth_rates': [],
                        'market_shares': [],
                        'monthly_data': [],
                        'latest_period': None
                    }
                
                product_metrics[product_id]['sectors'].add(sales_entry.sector)
                product_metrics[product_id]['regions'].add(sales_entry.region)
                
                for record in sales_entry.sales_records:
                    product_metrics[product_id]['total_revenue'] += record.revenue
                    product_metrics[product_id]['total_units'] += record.units_sold
                    product_metrics[product_id]['growth_rates'].append(record.growth_rate)
                    product_metrics[product_id]['market_shares'].append(record.market_share)
                    product_metrics[product_id]['monthly_data'].append({
                        'period': record.period,
                        'revenue': record.revenue,
                        'units': record.units_sold,
                        'growth_rate': record.growth_rate
                    })
                    
                    if (product_metrics[product_id]['latest_period'] is None or 
                        record.period > product_metrics[product_id]['latest_period']):
                        product_metrics[product_id]['latest_period'] = record.period
            
            # Calculate derived metrics for each product
            for product_id, metrics in product_metrics.items():
                avg_growth = sum(metrics['growth_rates']) / len(metrics['growth_rates']) if metrics['growth_rates'] else 0
                avg_market_share = sum(metrics['market_shares']) / len(metrics['market_shares']) if metrics['market_shares'] else 0
                
                # Sort monthly data by period
                metrics['monthly_data'].sort(key=lambda x: x['period'])
                
                # Calculate lifecycle stage
                lifecycle_stage = self._determine_lifecycle_stage(metrics['monthly_data'])
                
                # Calculate revenue per unit
                revenue_per_unit = metrics['total_revenue'] / metrics['total_units'] if metrics['total_units'] > 0 else 0
                
                # Update metrics with calculated values
                metrics.update({
                    'average_growth_rate': round(avg_growth, 2),
                    'average_market_share': round(avg_market_share, 2),
                    'lifecycle_stage': lifecycle_stage,
                    'revenue_per_unit': round(revenue_per_unit, 2),
                    'sector_count': len(metrics['sectors']),
                    'region_count': len(metrics['regions']),
                    'sectors': list(metrics['sectors']),
                    'regions': list(metrics['regions'])
                })
            
            # Create performance lists
            product_list = list(product_metrics.values())
            
            # Top performers by revenue
            top_performers = sorted(product_list, key=lambda x: x['total_revenue'], reverse=True)[:limit]
            
            # Bottom performers by revenue (excluding zero revenue)
            bottom_performers = sorted([p for p in product_list if p['total_revenue'] > 0], 
                                     key=lambda x: x['total_revenue'])[:limit]
            
            # Lifecycle analysis
            lifecycle_analysis = self._analyze_product_lifecycles(product_list)
            
            # Cross-sector performance analysis
            cross_sector_performance = self._analyze_cross_sector_performance(filtered_data)
            
            # Revenue vs units analysis
            revenue_vs_units = self._analyze_revenue_vs_units(product_list)
            
            return {
                'top_performers': top_performers,
                'bottom_performers': bottom_performers,
                'lifecycle_analysis': lifecycle_analysis,
                'cross_sector_performance': cross_sector_performance,
                'revenue_vs_units_analysis': revenue_vs_units,
                'summary_stats': {
                    'total_products_analyzed': len(product_list),
                    'average_revenue_per_product': sum(p['total_revenue'] for p in product_list) / len(product_list) if product_list else 0,
                    'average_units_per_product': sum(p['total_units'] for p in product_list) / len(product_list) if product_list else 0,
                    'most_diversified_product': max(product_list, key=lambda x: x['sector_count'])['product_id'] if product_list else None
                },
                'filters_applied': {
                    'sector': sector,
                    'region': region,
                    'limit': limit
                }
            }
            
        except Exception as e:
            logger.error(f"Error calculating product performance analytics: {e}")
            raise
    
    def _determine_lifecycle_stage(self, monthly_data: List[Dict[str, Any]]) -> str:
        """
        Determine product lifecycle stage based on revenue trends
        
        Args:
            monthly_data: List of monthly data points
            
        Returns:
            Lifecycle stage string
        """
        if len(monthly_data) < 3:
            return 'new'
        
        # Calculate trend over recent periods
        recent_data = monthly_data[-6:] if len(monthly_data) >= 6 else monthly_data
        
        # Calculate average growth rate
        growth_rates = []
        for i in range(1, len(recent_data)):
            if recent_data[i-1]['revenue'] > 0:
                growth_rate = ((recent_data[i]['revenue'] - recent_data[i-1]['revenue']) / recent_data[i-1]['revenue']) * 100
                growth_rates.append(growth_rate)
        
        if not growth_rates:
            return 'stable'
        
        avg_growth = sum(growth_rates) / len(growth_rates)
        
        if avg_growth > 15:
            return 'growth'
        elif avg_growth > 5:
            return 'mature'
        elif avg_growth > -5:
            return 'stable'
        else:
            return 'decline'
    
    def _analyze_product_lifecycles(self, product_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze product lifecycle distribution
        
        Args:
            product_list: List of product metrics
            
        Returns:
            Lifecycle analysis data
        """
        lifecycle_counts = {}
        lifecycle_revenue = {}
        
        for product in product_list:
            stage = product['lifecycle_stage']
            lifecycle_counts[stage] = lifecycle_counts.get(stage, 0) + 1
            lifecycle_revenue[stage] = lifecycle_revenue.get(stage, 0) + product['total_revenue']
        
        return {
            'stage_distribution': lifecycle_counts,
            'revenue_by_stage': lifecycle_revenue,
            'stage_percentages': {stage: (count / len(product_list) * 100) for stage, count in lifecycle_counts.items()} if product_list else {}
        }
    
    def _analyze_cross_sector_performance(self, filtered_data: List) -> Dict[str, Any]:
        """
        Analyze product performance across different sectors
        
        Args:
            filtered_data: Filtered sales data
            
        Returns:
            Cross-sector performance analysis
        """
        product_sector_performance = {}
        
        for sales_entry in filtered_data:
            product_id = sales_entry.product_id
            sector = sales_entry.sector
            
            if product_id not in product_sector_performance:
                product_sector_performance[product_id] = {}
            
            if sector not in product_sector_performance[product_id]:
                product_sector_performance[product_id][sector] = {
                    'revenue': 0,
                    'units': 0,
                    'periods': 0
                }
            
            for record in sales_entry.sales_records:
                product_sector_performance[product_id][sector]['revenue'] += record.revenue
                product_sector_performance[product_id][sector]['units'] += record.units_sold
                product_sector_performance[product_id][sector]['periods'] += 1
        
        # Find products with multi-sector presence
        multi_sector_products = {}
        for product_id, sectors in product_sector_performance.items():
            if len(sectors) > 1:
                multi_sector_products[product_id] = {
                    'sectors': sectors,
                    'sector_count': len(sectors),
                    'total_revenue': sum(s['revenue'] for s in sectors.values()),
                    'best_sector': max(sectors.items(), key=lambda x: x[1]['revenue'])[0],
                    'worst_sector': min(sectors.items(), key=lambda x: x[1]['revenue'])[0]
                }
        
        return {
            'multi_sector_products': multi_sector_products,
            'products_by_sector_count': {
                sector_count: len([p for p in product_sector_performance.values() if len(p) == sector_count])
                for sector_count in range(1, max(len(p) for p in product_sector_performance.values()) + 1)
            } if product_sector_performance else {}
        }
    
    def _analyze_revenue_vs_units(self, product_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze revenue vs units sold relationship
        
        Args:
            product_list: List of product metrics
            
        Returns:
            Revenue vs units analysis
        """
        analysis = []
        
        for product in product_list:
            revenue_per_unit = product['revenue_per_unit']
            
            # Categorize products by revenue per unit
            if revenue_per_unit > 150:
                category = 'premium'
            elif revenue_per_unit > 75:
                category = 'mid-market'
            else:
                category = 'value'
            
            analysis.append({
                'product_id': product['product_id'],
                'total_revenue': product['total_revenue'],
                'total_units': product['total_units'],
                'revenue_per_unit': revenue_per_unit,
                'category': category,
                'efficiency_score': (product['total_revenue'] * product['total_units']) / 1000  # Arbitrary efficiency metric
            })
        
        # Sort by efficiency score
        analysis.sort(key=lambda x: x['efficiency_score'], reverse=True)
        
        return analysis
    
    def advanced_multi_dimensional_query(self, 
                                       filters: Dict[str, Any],
                                       aggregations: List[str] = None,
                                       sort_by: str = 'revenue',
                                       limit: int = None,
                                       include_statistical_significance: bool = False) -> Dict[str, Any]:
        """
        Perform advanced multi-dimensional queries with statistical analysis
        
        Args:
            filters: Multi-dimensional filter criteria
            aggregations: List of aggregation functions to apply
            sort_by: Field to sort results by
            limit: Maximum number of results to return
            include_statistical_significance: Whether to include statistical significance calculations
            
        Returns:
            Advanced query results with optional statistical analysis
        """
        try:
            # Generate cache key
            cache_key = self._get_analytics_cache_key(
                'advanced_query',
                filters=str(sorted(filters.items())),
                aggregations=aggregations,
                sort_by=sort_by,
                limit=limit,
                include_stats=include_statistical_significance
            )
            
            # Check cache
            cached_result = self._get_cached_analytics(cache_key)
            if cached_result:
                logger.info(f"Returning cached advanced query result")
                return cached_result
            
            data = self._load_data()
            
            # Apply multi-dimensional filters efficiently using indexes
            filtered_data = self._apply_indexed_filters(data['sales_data'], filters)
            
            if not filtered_data:
                result = {
                    'results': [],
                    'total_count': 0,
                    'aggregations': {},
                    'filters_applied': filters,
                    'statistical_significance': {}
                }
                self._set_cached_analytics(cache_key, result)
                return result
            
            # Prepare aggregation functions
            if aggregations is None:
                aggregations = ['sum', 'avg', 'count', 'min', 'max']
            
            # Calculate aggregations
            aggregation_results = self._calculate_aggregations(filtered_data, aggregations)
            
            # Prepare results data structure
            results = []
            for sales_entry in filtered_data:
                entry_data = {
                    'product_id': sales_entry.product_id,
                    'company': sales_entry.company,
                    'sector': sales_entry.sector,
                    'region': sales_entry.region,
                    'total_revenue': sum(r.revenue for r in sales_entry.sales_records),
                    'total_units': sum(r.units_sold for r in sales_entry.sales_records),
                    'average_growth_rate': sum(r.growth_rate for r in sales_entry.sales_records) / len(sales_entry.sales_records) if sales_entry.sales_records else 0,
                    'average_market_share': sum(r.market_share for r in sales_entry.sales_records) / len(sales_entry.sales_records) if sales_entry.sales_records else 0,
                    'record_count': len(sales_entry.sales_records)
                }
                results.append(entry_data)
            
            # Sort results
            if sort_by in ['revenue', 'total_revenue']:
                results.sort(key=lambda x: x['total_revenue'], reverse=True)
            elif sort_by in ['units', 'total_units']:
                results.sort(key=lambda x: x['total_units'], reverse=True)
            elif sort_by == 'growth_rate':
                results.sort(key=lambda x: x['average_growth_rate'], reverse=True)
            elif sort_by == 'market_share':
                results.sort(key=lambda x: x['average_market_share'], reverse=True)
            
            # Apply limit
            if limit:
                results = results[:limit]
            
            # Calculate statistical significance if requested
            statistical_significance = {}
            if include_statistical_significance and len(results) > 1:
                statistical_significance = self._calculate_statistical_significance(results)
            
            result = {
                'results': results,
                'total_count': len(results),
                'aggregations': aggregation_results,
                'filters_applied': filters,
                'statistical_significance': statistical_significance,
                'sort_by': sort_by,
                'limit_applied': limit
            }
            
            # Cache the result
            self._set_cached_analytics(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error in advanced multi-dimensional query: {e}")
            raise
    
    def _apply_indexed_filters(self, sales_data: List[SalesData], filters: Dict[str, Any]) -> List[SalesData]:
        """
        Apply filters using built indexes for performance
        
        Args:
            sales_data: Sales data to filter
            filters: Filter criteria
            
        Returns:
            Filtered sales data
        """
        # Start with all data indexes
        candidate_indexes = set(range(len(sales_data)))
        
        # Apply product filter using index
        if 'product_id' in filters or 'product_ids' in filters:
            product_ids = filters.get('product_ids', [filters.get('product_id')]) if 'product_ids' in filters else [filters.get('product_id')]
            product_indexes = set()
            for product_id in product_ids:
                if product_id and product_id in self._product_index:
                    product_indexes.update(self._product_index[product_id])
            candidate_indexes = candidate_indexes.intersection(product_indexes)
        
        # Apply sector filter using index
        if 'sector' in filters or 'sectors' in filters:
            sectors = filters.get('sectors', [filters.get('sector')]) if 'sectors' in filters else [filters.get('sector')]
            sector_indexes = set()
            for sector in sectors:
                if sector and sector in self._sector_index:
                    sector_indexes.update(self._sector_index[sector])
            candidate_indexes = candidate_indexes.intersection(sector_indexes)
        
        # Apply region filter using index
        if 'region' in filters or 'regions' in filters:
            regions = filters.get('regions', [filters.get('region')]) if 'regions' in filters else [filters.get('region')]
            region_indexes = set()
            for region in regions:
                if region and region in self._region_index:
                    region_indexes.update(self._region_index[region])
            candidate_indexes = candidate_indexes.intersection(region_indexes)
        
        # Apply custom date range filters
        if 'date_range_start' in filters or 'date_range_end' in filters:
            date_start = filters.get('date_range_start')
            date_end = filters.get('date_range_end')
            
            if date_start or date_end:
                date_filtered_indexes = set()
                for period, period_data in self._period_index.items():
                    if date_start and period < date_start:
                        continue
                    if date_end and period > date_end:
                        continue
                    
                    for entry_index, record in period_data:
                        date_filtered_indexes.add(entry_index)
                
                candidate_indexes = candidate_indexes.intersection(date_filtered_indexes)
        
        # Apply revenue range filters
        if 'min_revenue' in filters or 'max_revenue' in filters:
            min_revenue = filters.get('min_revenue', 0)
            max_revenue = filters.get('max_revenue', float('inf'))
            
            revenue_filtered_indexes = set()
            for i in candidate_indexes:
                entry = sales_data[i]
                total_revenue = sum(r.revenue for r in entry.sales_records)
                if min_revenue <= total_revenue <= max_revenue:
                    revenue_filtered_indexes.add(i)
            
            candidate_indexes = revenue_filtered_indexes
        
        # Apply units range filters
        if 'min_units' in filters or 'max_units' in filters:
            min_units = filters.get('min_units', 0)
            max_units = filters.get('max_units', float('inf'))
            
            units_filtered_indexes = set()
            for i in candidate_indexes:
                entry = sales_data[i]
                total_units = sum(r.units_sold for r in entry.sales_records)
                if min_units <= total_units <= max_units:
                    units_filtered_indexes.add(i)
            
            candidate_indexes = units_filtered_indexes
        
        # Return filtered data
        return [sales_data[i] for i in sorted(candidate_indexes)]
    
    def _calculate_aggregations(self, filtered_data: List[SalesData], aggregations: List[str]) -> Dict[str, Any]:
        """
        Calculate aggregations on filtered data
        
        Args:
            filtered_data: Filtered sales data
            aggregations: List of aggregation functions
            
        Returns:
            Aggregation results
        """
        results = {}
        
        if not filtered_data:
            return {agg: 0 for agg in aggregations}
        
        # Collect all values for calculations
        revenues = []
        units = []
        growth_rates = []
        market_shares = []
        
        for entry in filtered_data:
            for record in entry.sales_records:
                revenues.append(record.revenue)
                units.append(record.units_sold)
                growth_rates.append(record.growth_rate)
                market_shares.append(record.market_share)
        
        # Calculate aggregations
        for agg in aggregations:
            if agg == 'sum':
                results['sum_revenue'] = sum(revenues)
                results['sum_units'] = sum(units)
            elif agg == 'avg':
                results['avg_revenue'] = sum(revenues) / len(revenues) if revenues else 0
                results['avg_units'] = sum(units) / len(units) if units else 0
                results['avg_growth_rate'] = sum(growth_rates) / len(growth_rates) if growth_rates else 0
                results['avg_market_share'] = sum(market_shares) / len(market_shares) if market_shares else 0
            elif agg == 'count':
                results['count_records'] = len(revenues)
                results['count_products'] = len(filtered_data)
            elif agg == 'min':
                results['min_revenue'] = min(revenues) if revenues else 0
                results['min_units'] = min(units) if units else 0
            elif agg == 'max':
                results['max_revenue'] = max(revenues) if revenues else 0
                results['max_units'] = max(units) if units else 0
        
        return results
    
    def _calculate_statistical_significance(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistical significance measures
        
        Args:
            results: Results data for statistical analysis
            
        Returns:
            Statistical significance measures
        """
        if len(results) < 2:
            return {}
        
        # Extract revenue data for statistical analysis
        revenues = [r['total_revenue'] for r in results]
        units = [r['total_units'] for r in results]
        
        # Calculate basic statistics
        import statistics
        
        try:
            revenue_stats = {
                'mean': statistics.mean(revenues),
                'median': statistics.median(revenues),
                'stdev': statistics.stdev(revenues) if len(revenues) > 1 else 0,
                'variance': statistics.variance(revenues) if len(revenues) > 1 else 0
            }
            
            units_stats = {
                'mean': statistics.mean(units),
                'median': statistics.median(units),
                'stdev': statistics.stdev(units) if len(units) > 1 else 0,
                'variance': statistics.variance(units) if len(units) > 1 else 0
            }
            
            # Calculate correlation coefficient (simple Pearson correlation)
            if len(revenues) == len(units) and len(revenues) > 1:
                correlation = self._calculate_correlation(revenues, units)
            else:
                correlation = 0
            
            return {
                'revenue_statistics': revenue_stats,
                'units_statistics': units_stats,
                'revenue_units_correlation': correlation,
                'sample_size': len(results),
                'confidence_interval_95': {
                    'revenue_lower': revenue_stats['mean'] - (1.96 * revenue_stats['stdev'] / (len(revenues) ** 0.5)) if revenue_stats['stdev'] > 0 else revenue_stats['mean'],
                    'revenue_upper': revenue_stats['mean'] + (1.96 * revenue_stats['stdev'] / (len(revenues) ** 0.5)) if revenue_stats['stdev'] > 0 else revenue_stats['mean']
                }
            }
        except Exception as e:
            logger.warning(f"Error calculating statistical significance: {e}")
            return {'error': 'Could not calculate statistical measures'}
    
    def _calculate_correlation(self, x_values: List[float], y_values: List[float]) -> float:
        """
        Calculate Pearson correlation coefficient
        
        Args:
            x_values: First set of values
            y_values: Second set of values
            
        Returns:
            Correlation coefficient
        """
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return 0
        
        n = len(x_values)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_x_sq = sum(x * x for x in x_values)
        sum_y_sq = sum(y * y for y in y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = ((n * sum_x_sq - sum_x * sum_x) * (n * sum_y_sq - sum_y * sum_y)) ** 0.5
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
