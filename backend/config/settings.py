import logging
import os
from datetime import timedelta, datetime
from functools import lru_cache
from typing import Optional, List, Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(dotenv_path="./.env")


def setup_logging():
    """Configure basic logging for the application."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


class LLMSettings(BaseModel):
    """Base settings for Language Model configurations."""

    temperature: float = 0.0
    max_tokens: Optional[int] = None
    max_retries: int = 3


class OpenAISettings(LLMSettings):
    """OpenAI-specific settings extending LLMSettings."""

    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    default_model: str = Field(default="gpt-4o")
    embedding_model: str = Field(default="text-embedding-3-small")


class DatabaseSettings(BaseModel):
    """Database connection settings."""

    service_url: str = Field(default_factory=lambda: os.getenv("TIMESCALE_SERVICE_URL"))


class VectorStoreSettings(BaseModel):
    """Settings for the VectorStore."""

    table_name: str = "documents"
    embedding_dimensions: int = 1536
    time_partition_interval: timedelta = timedelta(days=7)


class CohereSettings(BaseModel):
    """Cohere-specific settings."""

    api_key: str = Field(default_factory=lambda: os.getenv("COHERE_API_KEY"))


class CompanySynthesis(BaseModel):
    """Schema for DeepSeek AI insights output."""
    
    pitch: str = Field(default="", description="Company pitch as a string")
    feature_summary: list[str] = Field(default_factory=list, description="Feature summary as an array of strings")


class DeepSeekSettings(LLMSettings):
    """DeepSeek-specific settings extending LLMSettings."""

    api_key: str = Field(default_factory=lambda: os.getenv("GROQ_CLOUD_API_KEY"))
    base_url: str = Field(default="https://api.groq.com/openai/v1")
    default_model: str = Field(default="deepseek-r1-distill-llama-70b")
    temperature: float = 0.3
    max_tokens: int = 500


# === SCRAPER SCHEMAS ===

class ScrapedCompanyData(BaseModel):
    """Schema for raw company data extracted by the scraper."""
    
    index: Optional[int] = Field(None, description="Company index in scraper results")
    name: Optional[str] = Field(None, description="Company name")
    location: Optional[str] = Field(None, description="Company location")
    description: Optional[str] = Field(None, description="Company description")
    tags: List[str] = Field(default_factory=list, description="Company tags/categories")
    url: Optional[str] = Field(None, description="Company profile URL")
    logo_url: Optional[str] = Field(None, description="Company logo URL")
    extraction_method: Optional[str] = Field(None, description="Method used for extraction (playwright/javascript)")


class ScraperMetadata(BaseModel):
    """Schema for scraper-specific metadata."""
    
    index: Optional[int] = Field(None, description="Original scraper index")
    scraped_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Timestamp when scraped")
    scraper_version: str = Field(default="1.0", description="Version of the scraper used")
    batch_number: Optional[int] = Field(None, description="Batch number if using batch extraction")


class CompanyMetadata(BaseModel):
    """Schema for company metadata stored in vector database."""
    
    company_name: str = Field(..., description="Company name")
    location: str = Field(default="", description="Company location")
    tags: List[str] = Field(default_factory=list, description="Company tags/categories")
    url: str = Field(default="", description="Company profile URL")
    logo_url: Optional[str] = Field(None, description="Company logo URL")
    extraction_method: str = Field(default="ycombinator_scraper", description="Method used for data extraction")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Record creation timestamp")
    ai_insights: CompanySynthesis = Field(default_factory=CompanySynthesis, description="AI-generated insights")
    scraper_metadata: ScraperMetadata = Field(default_factory=ScraperMetadata, description="Scraper-specific metadata")


class DatabaseCompanyRecord(BaseModel):
    """Schema for complete company record as stored in vector database (matches pd.Series structure)."""
    
    id: str = Field(..., description="Unique identifier for the company record")
    metadata: CompanyMetadata = Field(..., description="Company metadata including AI insights")
    contents: str = Field(..., description="Full text content for embedding and search")
    embedding: List[float] = Field(..., description="Vector embedding of the contents")
    
    class Config:
        # Allow arbitrary types for the embedding field
        arbitrary_types_allowed = True


class ScraperConfig(BaseModel):
    """Configuration settings for the scraper."""
    
    default_table_name: str = Field(default="ycombinator_companies", description="Default database table name")
    max_companies_per_batch: int = Field(default=20, description="Maximum companies to process per batch")
    batch_delay_seconds: float = Field(default=1.0, description="Delay between batches in seconds")
    enable_ai_insights: bool = Field(default=True, description="Whether to generate AI insights")
    enable_embeddings: bool = Field(default=True, description="Whether to generate embeddings")
    content_template: str = Field(
        default="Company: {name}. Location: {location}. Description: {description}. Tags: {tags}",
        description="Template for generating content string"
    )


class Settings(BaseModel):
    """Main settings class combining all sub-settings."""

    openai: OpenAISettings = Field(default_factory=OpenAISettings)
    cohere: CohereSettings = Field(default_factory=CohereSettings)
    deepseek: DeepSeekSettings = Field(default_factory=DeepSeekSettings)
    company_synthesis: CompanySynthesis = Field(default_factory=CompanySynthesis)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    vector_store: VectorStoreSettings = Field(default_factory=VectorStoreSettings)
    scraper: ScraperConfig = Field(default_factory=ScraperConfig)


@lru_cache()
def get_settings() -> Settings:
    """Create and return a cached instance of the Settings."""
    settings = Settings()
    setup_logging()
    return settings