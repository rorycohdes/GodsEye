"""
Test script to demonstrate AI insights functionality.
This script shows how to retrieve companies with their AI-generated pitch and feature summaries.
"""

from database.vector_store import VectorStore

def test_ai_insights():
    """Test the AI insights functionality."""
    # Initialize VectorStore
    vec = VectorStore(table_name="sample_companies")
    
    print("=== Testing AI Insights Functionality ===\n")
    
    # Get companies with AI insights
    print("1. Retrieving companies with AI insights:")
    companies_df = vec.get_companies_with_ai_insights(limit=3)
    
    if len(companies_df) > 0:
        for idx, row in companies_df.iterrows():
            print(f"\n--- Company: {row['company_name']} ---")
            print(f"Location: {row['location']}")
            print(f"URL: {row['url']}")
            print(f"AI Pitch: {row['pitch']}")
            print(f"Feature Summary: {row['feature_summary']}")
            print(f"Created: {row['created_at']}")
            print("-" * 50)
    else:
        print("No companies with AI insights found. Run insert_vectors.py first.")
    
    # Test detailed retrieval
    print("\n2. Retrieving latest entries with detailed info:")
    latest_df = vec.get_latest_with_details(limit=2)
    
    if len(latest_df) > 0:
        for idx, row in latest_df.iterrows():
            print(f"\n--- Latest Entry {idx+1} ---")
            print(f"Company: {row['company_name']}")
            print(f"AI Pitch: {row['ai_pitch']}")
            print(f"AI Features: {row['ai_feature_summary']}")
            print(f"Content Preview: {row['contents'][:100]}...")
    else:
        print("No entries found.")

if __name__ == "__main__":
    test_ai_insights() 