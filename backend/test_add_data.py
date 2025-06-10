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
    
    # Create a new test company with more detailed information for AI insights
    test_company = {
        "name": f"InnovateTech Solutions {int(time.time())}",
        "location": "San Francisco, CA", 
        "description": f"A cutting-edge AI-powered SaaS platform that revolutionizes business decision-making through advanced analytics and machine learning. Founded in 2024, we help companies turn their data into actionable insights for better strategic planning. Our platform offers real-time dashboards, predictive analytics, and automated reporting features.",
        "tags": ["AI", "SaaS", "Analytics", "Machine Learning", "Data Science"],
        "url": "https://innovatetech-solutions.com",
        "logo_url": "https://innovatetech-solutions.com/logo.png",
        "extraction_method": "manual_test_with_ai_insights"
    }
    
    # Prepare the record for insertion
    content = f"Company: {test_company['name']}. Location: {test_company['location']}. Description: {test_company['description']}. Tags: {', '.join(test_company['tags'])}"
    
    embedding = vec.get_embedding(content)
    
    # Generate AI-powered pitch and feature summary using DeepSeek
    print("🤖 Generating AI insights...")
    ai_insights = vec.generate_ai_insights(content)
    print(f"✨ AI Pitch: {ai_insights.get('pitch', 'N/A')}")
    print(f"📋 AI Features: {ai_insights.get('feature_summary', [])}")
    
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
            "ai_insights": ai_insights  # Generated using DeepSeek on Groq Cloud
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
    print("🚀 Adding a new test company with AI-generated insights...")
    new_company = add_test_company()
    print(f"🎯 Company ID: {new_company['id']}")
    print(f"📍 Location: {new_company['metadata']['location']}")
    print(f"🤖 AI Insights: {new_company['metadata']['ai_insights']}")
    print("\n💡 Now check your real-time endpoints:")
    print("   - curl 'http://127.0.0.1:8000/api/realtime/latest?limit=1'")
    print("   - curl 'http://127.0.0.1:8000/api/realtime/count'")
    print("   - Check AI insights with: curl 'http://127.0.0.1:8000/api/companies/ai-insights?limit=1'") 