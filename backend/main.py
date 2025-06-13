#!/usr/bin/env python3
import asyncio
import argparse
import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import sql_routes, vector_routes, realtime_routes
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"backend_log_{datetime.now().strftime('%Y%m%d')}.log")
    ]
)
logger = logging.getLogger("backend")

# Add the current directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import scraper modules
from scraper.ycombinator.ycombinator import scrape_ycombinator_companies, load_proxies, run_periodic_scraper

app = FastAPI(
    title="GodsEye API",
    description="API for company data queries and vector search",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sql_routes.router, prefix="/api/sql", tags=["SQL Queries"])
app.include_router(vector_routes.router, prefix="/api/vector", tags=["Vector Search"])
app.include_router(realtime_routes.router, prefix="/api/realtime", tags=["Real-time Data"])

@app.get("/")
async def root():
    return {"message": "GodsEye API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

def run_api_server(args):
    """Run the FastAPI server"""
    import uvicorn
    
    logger.info(f"Starting GodsEye API server on port {args.port}")
    logger.info("API Documentation available at:")
    logger.info(f"  - Swagger UI: http://localhost:{args.port}/docs")
    logger.info(f"  - ReDoc: http://localhost:{args.port}/redoc")
    logger.info(f"  - Real-time API: http://localhost:{args.port}/api/realtime/latest")
    
    uvicorn.run(
        "main:app",  # Import string for the FastAPI app
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )

async def run_ycombinator_scraper(args):
    """Run the YCombinator scraper with the specified arguments"""
    logger.info("Starting YCombinator scraper")
    
    # Get API key from environment if not provided in args
    api_key = args.api_key or os.getenv("WEBSHARE_API_KEY")
    
    # Debug API key (without revealing the full key)
    if api_key:
        masked_key = api_key[:4] + '*' * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else '****'
        logger.info(f"Using API key: {masked_key}")
    else:
        logger.warning("No API key provided. Set WEBSHARE_API_KEY in .env file or use --api-key")
        logger.info("Proceeding without proxy - this may result in rate limiting")
    
    if args.periodic:
        logger.info(f"Running in periodic mode with {args.interval} hour interval")
        await run_periodic_scraper(
            interval_hours=args.interval,
            proxy_api_url=args.proxy_api,
            api_key=api_key,
            max_companies_per_run=args.cap,
            show_live=args.show_live,
            insert_to_db=not args.no_db,
            table_name=args.table_name
        )
    else:
        logger.info("Running scraper once")
        try:
            proxies = await load_proxies(args.proxy_api, api_key) if api_key else []
            companies = await scrape_ycombinator_companies(
                proxies=proxies,
                max_companies=args.cap,
                show_live=args.show_live,
                insert_to_db=not args.no_db,
                table_name=args.table_name
            )
            logger.info(f"Scraping completed. Scraped {len(companies) if companies else 0} companies.")
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            sys.exit(1)

def run_server_in_thread(args):
    """Run the API server in a separate thread"""
    server_thread = threading.Thread(target=run_api_server, args=(args,))
    server_thread.daemon = True  # Thread will exit when main program exits
    server_thread.start()
    return server_thread

def main():
    """Main entry point for the backend"""
    parser = argparse.ArgumentParser(description='GodsEye Backend Services')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # API Server command (default for frontend connectivity)
    api_parser = subparsers.add_parser('server', help='Run FastAPI server (for frontend connectivity)')
    api_parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
    api_parser.add_argument('--port', type=int, default=8000, help='Port to run the API server on')
    api_parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    
    # YCombinator scraper command
    yc_parser = subparsers.add_parser('yc-scraper', help='Run YCombinator scraper')
    yc_parser.add_argument('--periodic', action='store_true', help='Run the scraper periodically')
    yc_parser.add_argument('--interval', type=float, default=24, help='Interval in hours for periodic scraping')
    yc_parser.add_argument('--proxy-api', type=str, help='API URL to fetch proxy list')
    yc_parser.add_argument('--api-key', type=str, help='API key for proxy service')
    yc_parser.add_argument('--cap', type=int, help='Maximum companies to scrape')
    yc_parser.add_argument('--show-live', action='store_true', help='Show companies as they are scraped')
    yc_parser.add_argument('--no-db', action='store_true', help='Skip database insertion (JSON only)')
    yc_parser.add_argument('--table-name', type=str, help='Database table name to use')
    
    args = parser.parse_args()
    
    # Always start the server in a separate thread
    server_args = argparse.Namespace(host='0.0.0.0', port=8000, reload=False)
    server_thread = run_server_in_thread(server_args)
    logger.info("API server started in background thread")
    
    if not args.command:
        # Default to one-time scraping if no command specified
        logger.info("No command specified, running one-time scraper...")
        scraper_args = argparse.Namespace(
            periodic=False,
            interval=24,
            proxy_api=None,
            api_key=None,
            cap=None,
            show_live=False,
            no_db=False,
            table_name=None
        )
        asyncio.run(run_ycombinator_scraper(scraper_args))
    elif args.command == 'yc-scraper':
        asyncio.run(run_ycombinator_scraper(args))
    else:
        parser.print_help()
    
    # Keep the main thread alive while the server is running
    try:
        server_thread.join()
    except KeyboardInterrupt:
        logger.info("Backend stopped by user")
    except Exception as e:
        logger.exception(f"Unhandled exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Backend stopped by user")
    except Exception as e:
        logger.exception(f"Unhandled exception: {e}")
        sys.exit(1)