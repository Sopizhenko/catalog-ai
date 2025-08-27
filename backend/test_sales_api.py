#!/usr/bin/env python3
"""
Test script for Sales Analytics API endpoints

This script tests all the basic sales API endpoints to ensure they are working correctly.
Run this script after starting the Flask server to validate Phase 1 implementation.

Usage:
    python test_sales_api.py
"""

import requests
import json
import sys
from datetime import datetime

# Base URL for the API
BASE_URL = "http://localhost:5000"

def test_endpoint(endpoint, method="GET", data=None, description=""):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'='*60}")
    print(f"Testing: {method} {endpoint}")
    print(f"Description: {description}")
    print(f"URL: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print(f"Unsupported method: {method}")
            return False
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                json_data = response.json()
                print("✅ SUCCESS - Valid JSON response")
                
                # Print relevant data excerpts
                if isinstance(json_data, dict):
                    if 'total_records' in json_data:
                        print(f"   📊 Total Records: {json_data['total_records']}")
                    if 'total_revenue' in json_data:
                        print(f"   💰 Total Revenue: {json_data['total_revenue']} EUR")
                    if 'sectors' in json_data:
                        print(f"   🏢 Sectors Found: {len(json_data['sectors'])}")
                    if 'status' in json_data:
                        print(f"   🔄 Status: {json_data['status']}")
                
                return True
                
            except json.JSONDecodeError:
                print("❌ FAILED - Invalid JSON response")
                print(f"Response: {response.text[:200]}...")
                return False
        else:
            print(f"❌ FAILED - HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"Response: {response.text[:200]}...")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ FAILED - Connection Error")
        print("   Make sure the Flask server is running on port 5000")
        return False
    except requests.exceptions.Timeout:
        print("❌ FAILED - Timeout")
        return False
    except Exception as e:
        print(f"❌ FAILED - Unexpected error: {e}")
        return False

def main():
    """Run all API tests"""
    print("🚀 Sales Analytics API Test Suite")
    print(f"Started at: {datetime.now()}")
    print(f"Testing API at: {BASE_URL}")
    
    tests = [
        # Basic health checks
        ("/api/health", "GET", None, "Main API health check"),
        ("/api/sales/health", "GET", None, "Sales service health check"),
        
        # Sales data endpoints
        ("/api/sales/summary", "GET", None, "Basic sales summary"),
        ("/api/sales/test-data", "GET", None, "Test data for frontend development"),
        ("/api/sales/sectors", "GET", None, "Sector performance data"),
        ("/api/sales/validation", "GET", None, "Data quality validation"),
        
        # Filtered endpoints
        ("/api/sales/summary?sector=Retail", "GET", None, "Sales summary filtered by Retail sector"),
        ("/api/sales/summary?period_start=2024-06&period_end=2024-12", "GET", None, "Sales summary for H2 2024"),
        ("/api/sales/sectors?region=Nordic", "GET", None, "Sector performance for Nordic region"),
        
        # Product-specific endpoints
        ("/api/sales/trends/jeemly-pos", "GET", None, "Trend analysis for Jeemly POS"),
        ("/api/sales/trends/flowvy-ecommerce?analysis_type=monthly", "GET", None, "Monthly trend analysis for Flowvy"),
        
        # Management endpoints
        ("/api/sales/reload", "POST", {}, "Force reload sales data"),
    ]
    
    passed = 0
    failed = 0
    
    for endpoint, method, data, description in tests:
        success = test_endpoint(endpoint, method, data, description)
        if success:
            passed += 1
        else:
            failed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("🏁 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total:  {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Phase 1 API is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {failed} tests failed. Please check the server and fix issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
