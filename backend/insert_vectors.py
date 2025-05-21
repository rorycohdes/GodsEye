from datetime import datetime

import pandas as pd

from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time

import os
from dotenv import load_dotenv

# --- Debugging .env loading ---
print(f"Current Working Directory (CWD): {os.getcwd()}")
dotenv_target_path = "./.env"
absolute_dotenv_path = os.path.abspath(dotenv_target_path)
print(f"Attempting to load .env from: {absolute_dotenv_path}")

if os.path.exists(absolute_dotenv_path):
    print(f".env file found at: {absolute_dotenv_path}")
else:
    print(f"WARNING: .env file NOT found at: {absolute_dotenv_path}")

# Add verbose=True to see detailed output from dotenv
# Add override=True if you want to ensure .env values replace any existing environment variables
loaded_successfully = load_dotenv(dotenv_path=dotenv_target_path, verbose=True, override=True)
if loaded_successfully:
    print("load_dotenv reported SUCCESS.")
else:
    print("load_dotenv reported FAILURE (file might be unreadable, empty, or not found despite os.path.exists).")
# --- End Debugging .env loading ---


# Your existing print statement to check the key
api_key = os.getenv('OPENAI_API_KEY')
print(f"open ai api key: '{api_key}' (Type: {type(api_key)})")

# Initialize VectorStore
vec = VectorStore()

# Read the CSV file
df = pd.read_csv("data/faq_dataset.csv", sep=";")



# Prepare data for insertion
def prepare_record(row):
    """Prepare a record for insertion into the vector store.

    This function creates a record with a UUID version 1 as the ID, which captures
    the current time or a specified time.

    Note:
        - By default, this function uses the current time for the UUID.
        - To use a specific time:
          1. Import the datetime module.
          2. Create a datetime object for your desired time.
          3. Use uuid_from_time(your_datetime) instead of uuid_from_time(datetime.now()).

        Example:
            from datetime import datetime
            specific_time = datetime(2023, 1, 1, 12, 0, 0)
            id = str(uuid_from_time(specific_time))

        This is useful when your content already has an associated datetime.
    """
    content = f"Question: {row['question']}\nAnswer: {row['answer']}"
    embedding = vec.get_embedding(content)
    return pd.Series(
        {
            "id": str(uuid_from_time(datetime.now())),
            "metadata": {
                "category": row["category"],
                "created_at": datetime.now().isoformat(),
            },
            "contents": content,
            "embedding": embedding,
        }
    )


records_df = df.apply(prepare_record, axis=1)
#Create tables and insert data
vec.create_tables()
vec.create_index()  # DiskAnnIndex
vec.upsert(records_df)

