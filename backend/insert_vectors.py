from datetime import datetime
import json

import pandas as pd

from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")

print(f"open ai api key {os.getenv('OPENAI_API_KEY')}")
# Initialize VectorStore
vec = VectorStore(table_name="sample_companies")  # Pass table name during initialization

# Load the company dataset
def load_company_dataset(file_path="data/sample_companies.json"):
    """Load company data from JSON file"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data['companies'])

def generate_pitch_and_features(content: str) -> dict:
    """
    Generate pitch and feature summary based on company content using AI.
    
    Args:
        content (str): The company content to analyze
        
    Returns:
        dict: Dictionary containing 'pitch' and 'feature_summary' fields
        
    Note:
        Currently using OpenAI. TODO: Replace with DeepSeek on Grok integration
    """
    try:
        prompt = f"""
        Based on the following company information, generate:
        1. A compelling 2-sentence pitch for the company
        2. A brief feature summary (3-4 key features/capabilities)

        Company Information: {content}

        Please respond in JSON format:
        {{
            "pitch": "Your 2-sentence pitch here",
            "feature_summary": "Key features and capabilities summary here"
        }}
        """
        
        response = vec.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        
        # Parse the JSON response
        response_text = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:-3]
        elif response_text.startswith('```'):
            response_text = response_text[3:-3]
            
        result = json.loads(response_text)
        return {
            "pitch": result.get("pitch", ""),
            "feature_summary": result.get("feature_summary", "")
        }
        
    except Exception as e:
        print(f"Error generating pitch and features: {str(e)}")
        return {
            "pitch": "AI-generated pitch unavailable",
            "feature_summary": "AI-generated feature summary unavailable"
        }

# Load the dataset
df = load_company_dataset()
print(f"Loaded {len(df)} companies from dataset")

# Prepare data for insertion
def prepare_company_record(row):
    """Prepare a company record for insertion into the vector store.

    Args:
        row (pandas.Series): A row from the dataset containing company information.
    Returns:
        pandas.Series: A series containing the prepared record for insertion.

    Note:
        This function creates embeddings from the company's description and metadata.
        It uses the current time for the UUID. To use a specific time,
        create a datetime object and use uuid_from_time(your_datetime).
    """
    # Create content for embedding from company description and key info
    content = f"Company: {row['name']}. Location: {row['location']}. Description: {row['description']}. Tags: {', '.join(row['tags'])}"
    
    embedding = vec.get_embedding(content)
    
    # Generate AI-powered pitch and feature summary
    ai_insights = generate_pitch_and_features(content)
    
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "company_name": row['name'],
                "location": row['location'],
                "tags": row['tags'],
                "url": row['url'],
                "logo_url": row['logo_url'],
                "extraction_method": row['extraction_method'],
                "created_at": datetime.now().isoformat(),
                "ai_insights": ai_insights  # New field containing pitch and feature_summary
            },
            "contents": content,
            "embedding": embedding,
        }
    )

records_df = df.apply(prepare_company_record, axis=1)

# Create tables and insert data
vec.create_tables()  # Create tables if they don't exist
vec.create_index()  # DiskAnnIndex
vec.create_keyword_search_index()  # GIN Index
vec.upsert(records_df)

print(f"Successfully inserted {len(records_df)} company records into vector store")

