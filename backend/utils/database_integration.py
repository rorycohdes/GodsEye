"""
Database integration utilities for scraper data processing.

This module provides functions for validating, transforming, and inserting
scraped company data into the vector database with full schema compliance.
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional

from database.vector_store import VectorStore
from timescale_vector.client import uuid_from_time
from config.settings import (
    get_settings, 
    ScrapedCompanyData, 
    DatabaseCompanyRecord, 
    CompanyMetadata, 
    ScraperMetadata,
    CompanySynthesis
)


def validate_scraped_company(company_data: dict) -> Optional[ScrapedCompanyData]:
    """
    Validate and clean scraped company data using Pydantic schema.
    
    Args:
        company_data: Raw company data dictionary from scraper
        
    Returns:
        Validated ScrapedCompanyData instance or None if validation fails
    """
    try:
        # Convert to Pydantic model for validation
        validated_company = ScrapedCompanyData(**company_data)
        
        # Additional business logic validation
        if not validated_company.name and not validated_company.url:
            print(f"⚠️  Skipping company with no name or URL: {company_data}")
            return None
            
        return validated_company
        
    except Exception as e:
        print(f"❌ Invalid company data: {e}")
        print(f"   Raw data: {company_data}")
        return None


def prepare_scraped_company_for_db(
    scraped_company: ScrapedCompanyData, 
    vec_store: VectorStore, 
    settings,
    batch_number: Optional[int] = None
) -> DatabaseCompanyRecord:
    """
    Prepare validated scraped company data for insertion into the vector store.
    
    Args:
        scraped_company: Validated ScrapedCompanyData instance
        vec_store: VectorStore instance for generating embeddings and AI insights
        settings: Application settings
        batch_number: Optional batch number for tracking
    
    Returns:
        DatabaseCompanyRecord instance ready for database insertion
    """
    # Build content using template from settings
    content_parts = []
    
    if scraped_company.name:
        content_parts.append(f"Company: {scraped_company.name}")
    
    if scraped_company.location:
        content_parts.append(f"Location: {scraped_company.location}")
        
    if scraped_company.description:
        content_parts.append(f"Description: {scraped_company.description}")
        
    if scraped_company.tags:
        content_parts.append(f"Tags: {', '.join(scraped_company.tags)}")
    
    content = '. '.join(content_parts)
    
    # Generate embedding if enabled
    embedding = []
    if settings.scraper.enable_embeddings:
        print(f"🔄 Generating embedding for: {scraped_company.name or 'Unknown'}")
        embedding = vec_store.get_embedding(content)
    
    # Generate AI insights if enabled
    ai_insights = CompanySynthesis()
    if settings.scraper.enable_ai_insights:
        print(f"🤖 Generating AI insights for: {scraped_company.name or 'Unknown'}")
        ai_insights_dict = vec_store.generate_ai_insights(content)
        ai_insights = CompanySynthesis(**ai_insights_dict)
    
    # Create scraper metadata
    scraper_metadata = ScraperMetadata(
        index=scraped_company.index,
        scraped_at=datetime.now().isoformat(),
        scraper_version="2.0",  # Updated version with schema validation
        batch_number=batch_number
    )
    
    # Create company metadata
    company_metadata = CompanyMetadata(
        company_name=scraped_company.name or "Unknown",
        location=scraped_company.location or "",
        tags=scraped_company.tags,
        url=scraped_company.url or "",
        logo_url=scraped_company.logo_url,
        extraction_method=scraped_company.extraction_method or "scraper",
        created_at=datetime.now().isoformat(),
        ai_insights=ai_insights,
        scraper_metadata=scraper_metadata
    )
    
    # Create complete database record
    db_record = DatabaseCompanyRecord(
        id=str(uuid_from_time(datetime.now())),
        metadata=company_metadata,
        contents=content,
        embedding=embedding
    )
    
    return db_record


async def insert_companies_to_database(
    companies: List[dict], 
    table_name: str = None,
    source_name: str = "scraper"
) -> Dict[str, int]:
    """
    Insert scraped companies into the vector database with schema validation.
    
    Args:
        companies: List of raw company dictionaries from scraper
        table_name: Database table name to insert into
        source_name: Name of the source system (for logging and metadata)
    
    Returns:
        Dictionary containing insertion statistics: 
        {"inserted": int, "errors": int, "total": int}
    """
    if not companies:
        print("⚠️  No companies to insert into database")
        return {"inserted": 0, "errors": 0, "total": 0}
    
    settings = get_settings()
    table_name = table_name or settings.scraper.default_table_name
    
    print(f"\n💾 Preparing to insert {len(companies)} companies from {source_name} into database...")
    print(f"🗄️  Target table: {table_name}")
    
    # Initialize VectorStore with specific table name
    vec_store = VectorStore(table_name=table_name)
    
    try:
        # Create tables if they don't exist
        print("🔧 Creating database tables and indexes...")
        vec_store.create_tables()
        vec_store.create_index()  # DiskAnnIndex for vector search
        vec_store.create_keyword_search_index()  # GIN index for keyword search
        
        # Validate and prepare company records for database insertion
        print("🔄 Validating and processing companies for database insertion...")
        db_records = []
        validation_errors = 0
        
        for i, raw_company in enumerate(companies, 1):
            try:
                # Validate scraped data
                validated_company = validate_scraped_company(raw_company)
                if not validated_company:
                    validation_errors += 1
                    continue
                
                print(f"Processing company {i}/{len(companies)}: {validated_company.name or 'Unknown'}")
                
                # Prepare for database insertion
                db_record = prepare_scraped_company_for_db(validated_company, vec_store, settings)
                
                # Convert to dictionary for DataFrame
                db_records.append({
                    "id": db_record.id,
                    "metadata": db_record.metadata.dict(),
                    "contents": db_record.contents,
                    "embedding": db_record.embedding
                })
                
                # Show progress every 10 companies
                if i % 10 == 0:
                    print(f"✅ Processed {i}/{len(companies)} companies...")
                    
            except Exception as e:
                print(f"❌ Error processing company {raw_company.get('name', 'Unknown')}: {e}")
                validation_errors += 1
                continue
        
        if not db_records:
            print("❌ No valid company records prepared for insertion")
            return {"inserted": 0, "errors": validation_errors, "total": len(companies)}
        
        print(f"📊 Validation summary: {len(db_records)} valid, {validation_errors} errors")
        
        # Convert to DataFrame and insert
        print(f"💾 Inserting {len(db_records)} companies into database table '{table_name}'...")
        df = pd.DataFrame(db_records)
        vec_store.upsert(df)
        
        print(f"✅ Successfully inserted {len(db_records)} companies into database!")
        
        # Show sample of inserted companies
        print(f"\n📊 Sample of inserted companies:")
        for i, record in enumerate(db_records[:5], 1):
            metadata = record['metadata']
            name = metadata.get('company_name', 'Unknown')
            location = metadata.get('location', 'N/A')
            tags = ', '.join(metadata.get('tags', []))[:30]
            print(f"   {i}. {name} | {location} | {tags}")
        
        if len(db_records) > 5:
            print(f"   ... and {len(db_records) - 5} more companies")
            
        # Show AI insights sample
        if settings.scraper.enable_ai_insights and db_records:
            sample_insights = db_records[0]['metadata'].get('ai_insights', {})
            if sample_insights:
                print(f"\n🤖 Sample AI insights for '{db_records[0]['metadata']['company_name']}':")
                print(f"   Pitch: {sample_insights.get('pitch', 'N/A')[:100]}...")
                print(f"   Features: {sample_insights.get('feature_summary', [])[:3]}")
        
        return {
            "inserted": len(db_records),
            "errors": validation_errors, 
            "total": len(companies)
        }
        
    except Exception as e:
        print(f"❌ Error inserting companies into database: {e}")
        raise e


def batch_process_companies(
    companies: List[dict],
    batch_size: int = None,
    table_name: str = None,
    source_name: str = "scraper"
) -> Dict[str, int]:
    """
    Process companies in batches for better memory management and progress tracking.
    
    Args:
        companies: List of raw company dictionaries
        batch_size: Size of each batch (uses config default if not specified)
        table_name: Database table name
        source_name: Name of the source system
        
    Returns:
        Dictionary containing total insertion statistics
    """
    if not companies:
        return {"inserted": 0, "errors": 0, "total": 0}
    
    settings = get_settings()
    batch_size = batch_size or settings.scraper.max_companies_per_batch
    
    total_stats = {"inserted": 0, "errors": 0, "total": len(companies)}
    
    print(f"\n📦 Processing {len(companies)} companies in batches of {batch_size}")
    
    for i in range(0, len(companies), batch_size):
        batch_num = (i // batch_size) + 1
        batch_companies = companies[i:i + batch_size]
        
        print(f"\n🔄 Processing batch {batch_num} ({len(batch_companies)} companies)...")
        
        try:
            import asyncio
            batch_stats = asyncio.run(insert_companies_to_database(
                batch_companies, 
                table_name, 
                f"{source_name}_batch_{batch_num}"
            ))
            
            total_stats["inserted"] += batch_stats["inserted"]
            total_stats["errors"] += batch_stats["errors"]
            
            print(f"✅ Batch {batch_num} complete: {batch_stats['inserted']} inserted, {batch_stats['errors']} errors")
            
        except Exception as e:
            print(f"❌ Batch {batch_num} failed: {e}")
            total_stats["errors"] += len(batch_companies)
    
    print(f"\n📊 FINAL STATISTICS:")
    print(f"   Total companies processed: {total_stats['total']}")
    print(f"   Successfully inserted: {total_stats['inserted']}")
    print(f"   Validation/insertion errors: {total_stats['errors']}")
    print(f"   Success rate: {(total_stats['inserted'] / total_stats['total'] * 100):.1f}%")
    
    return total_stats


def get_database_company_count(table_name: str = None) -> int:
    """
    Get the current count of companies in the database table.
    
    Args:
        table_name: Database table name to check
        
    Returns:
        Number of companies in the table
    """
    settings = get_settings()
    table_name = table_name or settings.scraper.default_table_name
    
    try:
        vec_store = VectorStore(table_name=table_name)
        # This is a simple way to get count - you might want to implement
        # a more efficient count method in VectorStore
        latest = vec_store.get_latest_rows(limit=1)
        if not latest.empty:
            print(f"📊 Database table '{table_name}' has records (latest ID: {latest.iloc[0]['id']})")
        else:
            print(f"📊 Database table '{table_name}' appears to be empty")
        return len(latest)
    except Exception as e:
        print(f"❌ Error checking database count: {e}")
        return 0 