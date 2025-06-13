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
import json
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")


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

# Import scraper modules and settings
from scraper.ycombinator.ycombinator import scrape_ycombinator_companies, load_proxies, run_periodic_scraper
from config.settings import get_settings

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
    
    # Get settings and table name
    settings = get_settings()
    table_name = args.table_name or settings.scraper.default_table_name
    
    # Override settings based on args
    if args.no_db:
        settings.scraper.enable_ai_insights = False
        settings.scraper.enable_embeddings = False
        logger.info("🔕 Database, AI insights, and embeddings disabled (--no-db mode)")
    else:
        if args.no_ai:
            settings.scraper.enable_ai_insights = False
            logger.info("🤖 AI insights disabled")
        if args.no_embeddings:
            settings.scraper.enable_embeddings = False
            logger.info("🎯 Embeddings disabled")
    
    # Debug API key (without revealing the full key)
    if api_key:
        masked_key = api_key[:4] + '*' * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else '****'
        logger.info(f"Using API key: {masked_key}")
    else:
        logger.warning("No API key provided. Set WEBSHARE_API_KEY in .env file or use --api-key")
        logger.info("Proceeding without proxy - this may result in rate limiting")
    
    logger.info(f"Using table name: {table_name}")
    
    # Log configuration
    logger.info(f"\n🔧 Scraper Configuration:")
    logger.info(f"   📊 Company cap: {args.cap}")
    logger.info(f"   🔄 Periodic mode: {'Yes' if args.periodic else 'No'}")
    logger.info(f"   👁️  Live display: {'Yes' if args.show_live else 'No'}")
    logger.info(f"   💾 Database insertion: {'No' if args.no_db else 'Yes'}")
    logger.info(f"   📁 JSON backup: {'Disabled' if args.no_backup else 'Enabled'}")
    logger.info(f"   🤖 AI insights: {'No' if args.no_db or args.no_ai else 'Yes'}")
    logger.info(f"   🎯 Embeddings: {'No' if args.no_db or args.no_embeddings else 'Yes'}")
    if not args.no_db:
        logger.info(f"   🗄️  Database table: {table_name}")
    if args.periodic:
        logger.info(f"   ⏰ Interval: {args.interval} hours")
    
    if not args.periodic:  # Run once
        logger.info("\n🚀 Starting single scrape run...")
        try:
            async def run_once():
                try:
                    proxies = await load_proxies(args.proxy_api, api_key) if api_key else []
                    companies = await scrape_ycombinator_companies(
                        proxies=proxies,
                        max_companies=args.cap,
                        show_live=args.show_live,
                        insert_to_db=not args.no_db,
                        table_name=table_name,
                        save_backup=not args.no_backup
                    )
                    
                    # Additional verification for --no-db mode
                    if args.no_db and companies:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = os.path.join(data_dir, f"ycombinator_companies_{timestamp}.json")
                        try:
                            # Ensure the data directory exists
                            os.makedirs(data_dir, exist_ok=True)
                            
                            # Double-check the file was created
                            if not os.path.exists(filename):
                                logger.info(f"📝 Creating JSON file for --no-db mode: {filename}")
                                with open(filename, 'w', encoding='utf-8') as f:
                                    json.dump(companies, f, indent=2, ensure_ascii=False)
                                logger.info(f"✅ Verified JSON file creation: {filename}")
                        except Exception as e:
                            logger.error(f"❌ Error in --no-db file creation: {e}")
                            # Try one last time with a different filename
                            emergency_filename = os.path.join(data_dir, f"ycombinator_companies_final_{timestamp}.json")
                            try:
                                with open(emergency_filename, 'w', encoding='utf-8') as f:
                                    json.dump(companies, f, indent=2, ensure_ascii=False)
                                logger.info(f"✅ Saved to emergency file: {emergency_filename}")
                            except Exception as final_error:
                                logger.error(f"❌ Final attempt failed: {final_error}")
                    
                    return companies
                except ValueError as e:
                    logger.error(f"ERROR: {e}")
                    sys.exit(1)
            
            companies = await run_once()
            
            # Save to file for backup (even if inserted to DB)
            if companies and not args.no_db:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(data_dir, f"ycombinator_companies_backup_{timestamp}.json")
                with open(filename, 'w') as f:
                    json.dump(companies, f, indent=2)
                logger.info(f"💾 Backup saved: {len(companies)} companies to {filename}")
            elif companies:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(data_dir, f"ycombinator_companies_{timestamp}.json")
                with open(filename, 'w') as f:
                    json.dump(companies, f, indent=2)
                logger.info(f"💾 Saved {len(companies)} companies to {filename}")
                
            logger.info(f"Scraping completed. Scraped {len(companies) if companies else 0} companies.")
            
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            sys.exit(1)
    else:  # Run periodically
        logger.info(f"\n🚀 Starting periodic scraper...")
        await run_periodic_scraper(
            interval_hours=args.interval,
            proxy_api_url=args.proxy_api,
            api_key=api_key,
            max_companies_per_run=args.cap,
            show_live=True,
            insert_to_db=not args.no_db,
            table_name=table_name
        )

def run_server_in_thread(args):
    """Run the API server in a separate thread"""
    server_thread = threading.Thread(target=run_api_server, args=(args,))
    server_thread.daemon = True  # Thread will exit when main program exits
    server_thread.start()
    return server_thread

def main():
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
    yc_parser.add_argument('--cap', type=int, default=50, help='Maximum companies to scrape (default: 50)')
    yc_parser.add_argument('--show-live', action='store_true', default=True, help='Show companies as they are scraped (live mode) - enabled by default')
    yc_parser.add_argument('--no-db', action='store_true', help='Disable database insertion, embeddings, and AI insights (JSON only)')
    yc_parser.add_argument('--no-backup', action='store_true', help='Disable JSON file backup storage (data will only be stored in database if --no-db is not used)')
    yc_parser.add_argument('--table-name', type=str, help='Database table name to use')
    yc_parser.add_argument('--no-ai', action='store_true', help='Disable AI insights generation')
    yc_parser.add_argument('--no-embeddings', action='store_true', help='Disable embedding generation')
    
    args = parser.parse_args()
    
    if args.command == 'yc-scraper':
        # Run scraper in isolation, similar to ycombinator.py
        async def run_scraper():
            try:
                # Get API key from environment if not provided in args
                api_key = args.api_key or os.getenv("WEBSHARE_API_KEY")
                
                if not api_key:
                    logger.error("No API key provided. Set WEBSHARE_API_KEY in .env file or use --api-key")
                    raise ValueError("No API key provided. Set WEBSHARE_API_KEY in .env file or use --api-key")
                
                # Debug API key (without revealing the full key)
                masked_key = api_key[:4] + '*' * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else '****'
                logger.info(f"Using API key: {masked_key}")
                
                # Log configuration
                logger.info(f"\n🔧 Scraper Configuration:")
                logger.info(f"   📊 Company cap: {args.cap}")
                logger.info(f"   🔄 Periodic mode: {'Yes' if args.periodic else 'No'}")
                logger.info(f"   👁️  Live display: {'Yes' if args.show_live else 'No'}")
                logger.info(f"   💾 Database insertion: {'No' if args.no_db else 'Yes'}")
                logger.info(f"   📁 JSON backup: {'Disabled' if args.no_backup else 'Enabled'}")
                logger.info(f"   🤖 AI insights: {'No' if args.no_db or args.no_ai else 'Yes'}")
                logger.info(f"   🎯 Embeddings: {'No' if args.no_db or args.no_embeddings else 'Yes'}")
                if not args.no_db:
                    logger.info(f"   🗄️  Database table: {args.table_name}")
                
                proxies = await load_proxies(args.proxy_api, api_key)
                companies = await scrape_ycombinator_companies(
                    proxies=proxies,
                    max_companies=args.cap,
                    show_live=args.show_live,
                    insert_to_db=not args.no_db,
                    table_name=args.table_name,
                    save_backup=not args.no_backup
                )
                return companies
            except Exception as e:
                logger.error(f"Scraping failed: {e}")
                raise
        
        # Run scraper directly without server
        asyncio.run(run_scraper())
    elif args.command == 'server':
        # Run server only
        run_api_server(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Backend stopped by user")
    except Exception as e:
        logger.exception(f"Unhandled exception: {e}")
        sys.exit(1)