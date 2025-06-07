"""
Debug script to test Groq Cloud API connection and DeepSeek model.
This will help identify issues with the AI insights generation.
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(dotenv_path="./.env")

def test_groq_connection():
    """Test basic connection to Groq Cloud API."""
    print("=== Testing Groq Cloud Connection ===")
    
    api_key = os.getenv("GROQ_CLOUD_API_KEY")
    if not api_key:
        print("❌ ERROR: GROQ_CLOUD_API_KEY not found in environment variables")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        # Test with a simple message
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": "Hello, can you respond with just 'Hello back!'?"}],
            temperature=0.3,
            max_tokens=100
        )
        
        response_text = response.choices[0].message.content.strip()
        print(f"✅ Basic API test successful: {response_text}")
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_ai_insights_generation():
    """Test AI insights generation with DeepSeek on Groq Cloud."""
    print("\n=== Testing AI Insights Generation ===")
    
    api_key = os.getenv("GROQ_CLOUD_API_KEY")
    if not api_key:
        print("❌ ERROR: GROQ_CLOUD_API_KEY not found")
        return False
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        test_content = "Company: TestCorp. Location: San Francisco. Description: A revolutionary AI-powered analytics platform that helps businesses make data-driven decisions. Tags: AI, Analytics, SaaS"
        
        prompt = f"""
        Based on the following company information, generate:
        1. A compelling 2-sentence pitch for the company
        2. A brief feature summary (3-4 key features/capabilities)

        Company Information: {test_content}

        Please respond in JSON format:
        {{
            "pitch": "Your 2-sentence pitch here",
            "feature_summary": "Key features and capabilities summary here"
        }}
        """
        
        print(f"Sending request to DeepSeek model...")
        print(f"Content: {test_content}")
        
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        
        response_text = response.choices[0].message.content.strip()
        print(f"\n✅ Raw response received:")
        print(f"{response_text}")
        
        # Try to parse JSON
        if response_text.startswith('```json'):
            clean_text = response_text[7:-3]
            print(f"\n📝 Cleaned JSON (removed markdown):")
            print(f"{clean_text}")
        elif response_text.startswith('```'):
            clean_text = response_text[3:-3]
            print(f"\n📝 Cleaned text (removed markdown):")
            print(f"{clean_text}")
        else:
            clean_text = response_text
            print(f"\n📝 No markdown formatting detected")
        
        try:
            result = json.loads(clean_text)
            print(f"\n✅ JSON parsing successful:")
            print(f"Pitch: {result.get('pitch', 'Not found')}")
            print(f"Feature Summary: {result.get('feature_summary', 'Not found')}")
            return True
            
        except json.JSONDecodeError as e:
            print(f"\n❌ JSON parsing failed: {str(e)}")
            print(f"Attempted to parse: {clean_text}")
            return False
        
    except Exception as e:
        print(f"❌ AI insights generation failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_environment_variables():
    """Test all required environment variables."""
    print("=== Testing Environment Variables ===")
    
    # Required for AI insights functionality
    required_vars = [
        "GROQ_CLOUD_API_KEY",
        "OPENAI_API_KEY", 
        "TIMESCALE_SERVICE_URL"
    ]
    
    # Optional for some features
    optional_vars = [
        "COHERE_API_KEY"
    ]
    
    all_required_good = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:10]}...{value[-4:] if len(value) > 14 else value}")
        else:
            print(f"❌ {var}: Not found")
            all_required_good = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:10]}...{value[-4:] if len(value) > 14 else value}")
        else:
            print(f"⚠️  {var}: Not found (optional - only needed for reranking)")
    
    return all_required_good

if __name__ == "__main__":
    print("🚀 DeepSeek on Groq Cloud Debug Script\n")
    
    # Test environment variables
    env_ok = test_environment_variables()
    
    # Test basic API connection
    if env_ok:
        api_ok = test_groq_connection()
        
        # Test AI insights generation
        if api_ok:
            insights_ok = test_ai_insights_generation()
            
            if insights_ok:
                print("\n🎉 All tests passed! Your setup should work correctly.")
            else:
                print("\n⚠️  AI insights generation failed. Check the error messages above.")
        else:
            print("\n⚠️  Basic API connection failed. Check your API key and network.")
    else:
        print("\n⚠️  Missing required environment variables. Check your .env file.")
    
    print("\n" + "="*50) 