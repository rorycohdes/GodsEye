import asyncio
import json
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Optional
from pydantic import BaseModel
from database.vector_store import VectorStore
import time

router = APIRouter()

class LatestDataResponse(BaseModel):
    id: str
    company_name: Optional[str] = None
    location: Optional[str] = None
    url: Optional[str] = None
    created_at: Optional[str] = None
    contents: str

# Store for tracking last known data state
last_data_cache = {}

@router.get("/latest")
async def get_latest_data(limit: int = 10):
    """Get the latest data from the database"""
    try:
        vec = VectorStore(table_name="sample_companies")
        latest_df = vec.get_latest_with_details(limit=limit)
        
        # Convert DataFrame to list of dictionaries
        latest_data = []
        for _, row in latest_df.iterrows():
            latest_data.append({
                "id": row["id"],
                "company_name": row["company_name"],
                "location": row["location"],
                "url": row["url"],
                "created_at": row["created_at"],
                "contents": row["contents"]
            })
        
        return {"data": latest_data, "timestamp": time.time()}
    except Exception as e:
        return {"error": str(e)}

@router.get("/latest/stream")
async def stream_latest_data():
    """Stream latest data updates using Server-Sent Events"""
    async def event_stream():
        vec = VectorStore(table_name="sample_companies")
        last_id = None
        
        while True:
            try:
                # Get the latest row
                latest_df = vec.get_latest_with_details(limit=1)
                
                if not latest_df.empty:
                    current_id = latest_df.iloc[0]["id"]
                    
                    # Only send if we have new data
                    if current_id != last_id:
                        latest_data = {
                            "id": str(latest_df.iloc[0]["id"]),
                            "company_name": latest_df.iloc[0]["company_name"],
                            "location": latest_df.iloc[0]["location"],
                            "url": latest_df.iloc[0]["url"],
                            "created_at": latest_df.iloc[0]["created_at"],
                            "contents": latest_df.iloc[0]["contents"],
                            "timestamp": time.time()
                        }
                        
                        yield f"data: {json.dumps(latest_data)}\n\n"
                        last_id = current_id
                
                # Wait 5 seconds before checking again
                await asyncio.sleep(5)
                
            except Exception as e:
                error_data = {"error": str(e), "timestamp": time.time()}
                yield f"data: {json.dumps(error_data)}\n\n"
                await asyncio.sleep(5)
    
    return StreamingResponse(
        event_stream(), 
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )

@router.get("/latest/poll")
async def poll_for_updates(last_id: Optional[str] = None):
    """Polling endpoint that only returns data if there are updates"""
    try:
        vec = VectorStore(table_name="sample_companies")
        latest_df = vec.get_latest_with_details(limit=1)
        
        if latest_df.empty:
            return {"has_updates": False}
        
        current_id = latest_df.iloc[0]["id"]
        
        # Return data only if it's different from last_id
        if current_id != last_id:
            latest_data = {
                "id": latest_df.iloc[0]["id"],
                "company_name": latest_df.iloc[0]["company_name"],
                "location": latest_df.iloc[0]["location"],
                "url": latest_df.iloc[0]["url"],
                "created_at": latest_df.iloc[0]["created_at"],
                "contents": latest_df.iloc[0]["contents"],
                "timestamp": time.time()
            }
            return {"has_updates": True, "data": latest_data}
        else:
            return {"has_updates": False}
            
    except Exception as e:
        return {"error": str(e)}

@router.get("/count")
async def get_total_count():
    """Get total count of records in the database"""
    try:
        vec = VectorStore(table_name="sample_companies")
        
        # Quick count query
        sql = f"SELECT COUNT(*) FROM {vec.table_name}"
        
        import psycopg
        with psycopg.connect(vec.settings.database.service_url) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                count = cur.fetchone()[0]
        
        return {"count": count, "timestamp": time.time()}
    except Exception as e:
        return {"error": str(e)} 