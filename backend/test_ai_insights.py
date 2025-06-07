"""
Test script to demonstrate AI insights functionality.
This script shows how to retrieve companies with their AI-generated pitch and feature summaries.
AI insights are now generated using DeepSeek on Groq Cloud.
"""

from database.vector_store import VectorStore

def test_ai_insights():
    """Test the AI insights functionality with DeepSeek on Groq Cloud."""
    # Initialize VectorStore
    vec = VectorStore(table_name="sample_companies")
    
    print("=== Testing AI Insights Functionality (DeepSeek on Groq Cloud) ===\n")
    
    # Get companies with AI insights
    print("1. Retrieving companies with DeepSeek (Groq Cloud) generated AI insights:")
    companies_df = vec.get_companies_with_ai_insights(limit=3)
    
    if len(companies_df) > 0:
        for idx, row in companies_df.iterrows():
            print(f"\n--- Company: {row['company_name']} ---")
            print(f"Location: {row['location']}")
            print(f"URL: {row['url']}")
            print(f"DeepSeek AI Pitch (via Groq): {row['pitch']}")
            print(f"DeepSeek Feature Summary (via Groq): {row['feature_summary']}")
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
            print(f"DeepSeek AI Pitch (via Groq): {row['ai_pitch']}")
            print(f"DeepSeek AI Features (via Groq): {row['ai_feature_summary']}")
            print(f"Content Preview: {row['contents'][:100]}...")
    else:
        print("No entries found.")

    # Test direct AI insights generation
    print("\n3. Testing direct DeepSeek (Groq Cloud) AI insights generation:")
    test_content = "Company: TestCorp. Location: San Francisco. Description: A revolutionary AI-powered analytics platform that helps businesses make data-driven decisions. Tags: AI, Analytics, SaaS"
    
    try:
        insights = vec.generate_ai_insights(test_content)
        print(f"Test Content: {test_content}")
        print(f"Generated Pitch (DeepSeek via Groq): {insights['pitch']}")
        print(f"Generated Features (DeepSeek via Groq): {insights['feature_summary']}")
    except Exception as e:
        print(f"Error testing AI insights generation: {e}")

if __name__ == "__main__":
    test_ai_insights() 