# GodsEye

## Docker

### Activate virtual environment

Caveats:

- Ensure your in the directory containing the venv folder
- Ensure you have created the virtual environment to begin with using `python -m venv venv`

Then run the following:

```
source <venv folder>/bin/activate
```

or

```
source venv/bin/activate
```

## YCombinator Scraper

### Prerequisites

1. Set up environment variables in `.env` file:

   ```
   WEBSHARE_API_KEY=your_proxy_api_key
   TIMESCALE_SERVICE_URL=your_database_url
   ```

2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

### Running the Scraper

#### Basic Commands

**Single Run (Recommended for Testing):**

```bash
# Basic single run with 20 companies
python scraper/ycombinator/ycombinator.py --once --cap 20

# Quick test with minimal features (faster)
python scraper/ycombinator/ycombinator.py --once --cap 5 --no-ai --no-embeddings
```

**Single Run with Database Integration:**

```bash
# Standard run with database insertion
python scraper/ycombinator/ycombinator.py --once --cap 50

# Use custom table name
python scraper/ycombinator/ycombinator.py --once --cap 30 --table-name "yc_companies_2024"
```

**JSON-Only Mode (No Database):**

```bash
# Save to JSON file only
python scraper/ycombinator/ycombinator.py --once --cap 25 --no-db
```

#### Advanced Options

**Performance Tuning:**

```bash
# Disable AI insights for faster scraping
python scraper/ycombinator/ycombinator.py --once --cap 100 --no-ai

# Disable both AI and embeddings (fastest)
python scraper/ycombinator/ycombinator.py --once --cap 100 --no-ai --no-embeddings
```

**Periodic Scraping:**

```bash
# Run every 12 hours
python scraper/ycombinator/ycombinator.py --interval 12 --cap 50

# Daily runs with custom table
python scraper/ycombinator/ycombinator.py --interval 24 --cap 100 --table-name "daily_scrapes"
```

#### Command Reference

```bash
python scraper/ycombinator/ycombinator.py [OPTIONS]

Options:
  --once              Run once instead of periodically
  --interval HOURS    Hours between runs (default: 24)
  --cap NUMBER        Max companies per run (default: 50)
  --table-name NAME   Custom database table name
  --no-db             Save to JSON only (no database)
  --no-ai             Disable AI insights generation
  --no-embeddings     Disable embedding generation
  --proxy-api URL     Custom proxy API URL
  --api-key KEY       Proxy service API key
  --show-live         Show companies as scraped (default: enabled)
```

#### Example Workflows

**Testing/Development:**

```bash
# Quick test - 5 companies, no AI, no embeddings
python scraper/ycombinator/ycombinator.py --once --cap 5 --no-ai --no-embeddings

# Medium test - 20 companies with full features
python scraper/ycombinator/ycombinator.py --once --cap 20
```

**Production Data Collection:**

```bash
# Full run with database integration
python scraper/ycombinator/ycombinator.py --once --cap 200

# Periodic production scraping
python scraper/ycombinator/ycombinator.py --interval 24 --cap 100 --table-name "production_yc_data"
```

**Specific Use Cases:**

```bash
# Fast data collection (no AI processing)
python scraper/ycombinator/ycombinator.py --once --cap 500 --no-ai --no-embeddings

# AI insights focus (smaller batch with full processing)
python scraper/ycombinator/ycombinator.py --once --cap 50

# Backup to JSON (database issues)
python scraper/ycombinator/ycombinator.py --once --cap 100 --no-db
```

**Quick Start Recommendation:**

```bash
# Start with this command for your first run:
python scraper/ycombinator/ycombinator.py --once --cap 10
```

### Features

- ✅ **Schema Validation** - Full Pydantic validation for data integrity
- ✅ **Database Integration** - Automatic insertion into vector database
- ✅ **AI Insights** - Generated company pitches and feature summaries
- ✅ **Vector Embeddings** - For semantic search capabilities
- ✅ **Batch Processing** - Efficient handling of large datasets
- ✅ **Proxy Support** - Built-in proxy rotation for scraping
- ✅ **Error Handling** - Comprehensive error tracking and recovery
- ✅ **Progress Tracking** - Real-time scraping progress and statistics

## API Development

document.querySelector to get element of specific class very str8 forward

vector operations and tradional data queries, one database

fast api for two way communciations AND real time database update

The main differences between @router and @app decorators in FastAPI are:

@app decorators
Direct binding: Routes are directly attached to the main FastAPI application instance
Global scope: All routes defined with @app are immediately available at the application level
Simple structure: Good for small applications with few routes

@router decorators
Modular organization: Routes are defined on APIRouter instances for better code organization
Prefix support: Can add URL prefixes when including the router in the app
Separation of concerns: Allows grouping related endpoints in separate files
Reusability: Routers can be included in multiple apps or with different prefixes

In your current setup:
SQL routes use @router.get() and are included with prefix /api/sql
Vector routes use @router.get() and are included with prefix /api/vector
This means your endpoints will be:
/api/sql/companies
/api/vector/search
etc.

Makes sql queries in realtime to keep the frontend updated with the latest changes using SSE in our api
SSE route just for sending data to the webscraping page

Intermediate ways to test files or quick ways [tools] to poke and prod your api/ server such as:
curl and json.tool
curl and query params such as limit
ex. curl -s "http://127.0.0.1:8000/api/realtime/latest?limit=3" | python3 -m json.tool

no need to cluster file with logs and print statements

when you get "These conflicts are too complex to resolve in the web editor." just merge from the command line
