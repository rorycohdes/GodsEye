#!/usr/bin/env python3
"""Test script to add new data and observe real-time updates"""

import pandas as pd
from datetime import datetime
from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time
import time

def add_test_company():
    """Add a new test company to the database"""
    vec = VectorStore(table_name="sample_companies")
    
    # Create a new test company
    test_company = {
        "name": f"Test Company {int(time.time())}",
        "location": "Test City, TS", 
        "description": f"A test company added at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "tags": ["Test", "Demo", "API"],
        "url": "https://test-company.com",
        "logo_url": "https://test-company.com/logo.png",
        "extraction_method": "manual_test"
    }
    
    # Prepare the record for insertion
    content = f"Company: {test_company['name']}. Location: {test_company['location']}. Description: {test_company['description']}. Tags: {', '.join(test_company['tags'])}"
    
    embedding = vec.get_embedding(content)
    
    record_data = {
        "id": str(uuid_from_time(datetime.now())),
        "metadata": {
            "company_name": test_company['name'],
            "location": test_company['location'],
            "tags": test_company['tags'],
            "url": test_company['url'],
            "logo_url": test_company['logo_url'],
            "extraction_method": test_company['extraction_method'],
            "created_at": datetime.now().isoformat(),
        },
        "contents": content,
        "embedding": embedding,
    }
    
    # Create DataFrame and insert
    df = pd.DataFrame([record_data])
    vec.upsert(df)
    
    print(f"✅ Added test company: {test_company['name']}")
    return record_data

if __name__ == "__main__":
    print("🚀 Adding a new test company...")
    new_company = add_test_company()
    print(f"🎯 Company ID: {new_company['id']}")
    print(f"📍 Location: {new_company['metadata']['location']}")
    print("\n💡 Now check your real-time endpoints:")
    print("   - curl 'http://127.0.0.1:8000/api/realtime/latest?limit=1'")
    print("   - curl 'http://127.0.0.1:8000/api/realtime/count'") 