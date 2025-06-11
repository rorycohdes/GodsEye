"""
Example usage of database integration utilities.

This script demonstrates how to use the database integration functions
for processing and inserting company data from various sources.
"""

import asyncio
import json
from typing import List, Dict

from utils.database_integration import (
    insert_companies_to_database,
    batch_process_companies,
    get_database_company_count,
    validate_scraped_company
)
from config.settings import get_settings


def load_sample_companies() -> List[Dict]:
    """Load sample company data for testing."""
    return [
        {
            "index": 1,
            "name": "TechCorp Solutions",
            "location": "San Francisco, CA",
            "description": "AI-powered business automation platform",
            "tags": ["AI", "Automation", "B2B", "SaaS"],
            "url": "https://example.com/techcorp",
            "logo_url": "https://example.com/logos/techcorp.png",
            "extraction_method": "manual_entry"
        },
        {
            "index": 2,
            "name": "GreenTech Innovations",
            "location": "Austin, TX", 
            "description": "Sustainable energy management solutions",
            "tags": ["GreenTech", "Energy", "Sustainability"],
            "url": "https://example.com/greentech",
            "logo_url": None,
            "extraction_method": "api_import"
        },
        {
            "index": 3,
            "name": "DataFlow Analytics",
            "location": "Boston, MA",
            "description": "Real-time data processing and analytics",
            "tags": ["Analytics", "Data", "Real-time"],
            "url": "https://example.com/dataflow",
            "logo_url": "https://example.com/logos/dataflow.png",
            "extraction_method": "csv_import"
        }
    ]


async def example_single_insert():
    """Example: Insert companies using the standard function."""
    print("=" * 60)
    print("EXAMPLE 1: Single insert operation")
    print("=" * 60)
    
    companies = load_sample_companies()
    
    # Insert into a test table
    stats = await insert_companies_to_database(
        companies=companies,
        table_name="example_companies_test", 
        source_name="example_script"
    )
    
    print(f"\n📊 Insertion complete:")
    print(f"   Inserted: {stats['inserted']}")
    print(f"   Errors: {stats['errors']}")
    print(f"   Total: {stats['total']}")


def example_batch_processing():
    """Example: Process companies in batches."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Batch processing")
    print("=" * 60)
    
    # Create a larger dataset for batch processing
    companies = []
    for i in range(25):  # Create 25 sample companies
        companies.append({
            "index": i + 1,
            "name": f"Company {i + 1}",
            "location": f"City {i + 1}",
            "description": f"Description for company {i + 1}",
            "tags": ["Tag1", "Tag2"],
            "url": f"https://example.com/company{i + 1}",
            "logo_url": None,
            "extraction_method": "batch_generation"
        })
    
    # Process in batches of 10
    stats = batch_process_companies(
        companies=companies,
        batch_size=10,
        table_name="example_batch_test",
        source_name="batch_example"
    )
    
    print(f"\n📊 Batch processing complete:")
    print(f"   Total processed: {stats['total']}")
    print(f"   Successfully inserted: {stats['inserted']}")
    print(f"   Errors: {stats['errors']}")


def example_validation():
    """Example: Validate company data before processing."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Data validation")
    print("=" * 60)
    
    # Test with both valid and invalid data
    test_companies = [
        {
            "name": "Valid Company",
            "location": "Valid Location",
            "description": "Valid description",
            "tags": ["Valid", "Tags"],
            "url": "https://valid.com",
            "extraction_method": "test"
        },
        {
            # Missing name and URL - should be rejected
            "location": "Some Location",
            "description": "No name or URL",
            "tags": ["Invalid"],
            "extraction_method": "test"
        },
        {
            "name": "Another Valid Company",
            "description": "Another valid description",
            # Missing some optional fields - should be accepted
            "extraction_method": "test"
        }
    ]
    
    valid_count = 0
    invalid_count = 0
    
    for i, company in enumerate(test_companies, 1):
        print(f"\nValidating company {i}:")
        validated = validate_scraped_company(company)
        
        if validated:
            valid_count += 1
            print(f"  ✅ Valid: {validated.name or 'Unnamed'}")
        else:
            invalid_count += 1
            print(f"  ❌ Invalid company data")
    
    print(f"\n📊 Validation results:")
    print(f"   Valid companies: {valid_count}")
    print(f"   Invalid companies: {invalid_count}")


def example_database_count():
    """Example: Check database table statistics."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Database statistics")
    print("=" * 60)
    
    # Check different tables
    tables_to_check = [
        "example_companies_test",
        "example_batch_test", 
        "ycombinator_companies",
        "nonexistent_table"
    ]
    
    for table_name in tables_to_check:
        print(f"\nChecking table: {table_name}")
        try:
            count = get_database_company_count(table_name)
            print(f"  📊 Company count: {count}")
        except Exception as e:
            print(f"  ❌ Error: {e}")


async def main():
    """Run all examples."""
    print("🚀 Database Integration Utilities - Usage Examples")
    print("=" * 60)
    
    # Load settings
    settings = get_settings()
    print(f"Using database: {settings.database.service_url[:50]}...")
    print(f"Default table: {settings.scraper.default_table_name}")
    
    # Run examples
    await example_single_insert()
    example_batch_processing() 
    example_validation()
    example_database_count()
    
    print("\n" + "=" * 60)
    print("✅ All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main()) 