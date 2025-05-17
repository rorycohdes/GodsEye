#!/usr/bin/env python3
import asyncio
import argparse
import logging
import sys
import os
from datetime import datetime
from pathlib import Path

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

async def run_ycombinator_scraper(args):
    """Run the YCombinator scraper with the specified arguments"""
    logger.info("Starting YCombinator scraper")
    
    if args.periodic:
        logger.info(f"Running in periodic mode with {args.interval} hour interval")
        logger.info(f"Proxy usage: {'Disabled' if args.no_proxy else 'Enabled'}")
        await run_periodic_scraper(
            interval_hours=args.interval,
            proxy_api_url=args.proxy_api,
            use_proxy=not args.no_proxy
        )
    else:
        logger.info("Running scraper once")
        proxies = None
        if not args.no_proxy:
            logger.info("Loading proxies...")
            proxies = await load_proxies(args.proxy_api)
            logger.info(f"Loaded {len(proxies)} proxies")
        
        companies = await scrape_ycombinator_companies(
            proxies=proxies,
            use_proxy=not args.no_proxy,
            limit_pages=args.limit
        )
        
        logger.info(f"Scraping completed. Scraped {len(companies)} companies.")

def main():
    """Main entry point for the backend"""
    parser = argparse.ArgumentParser(description='Backend Services')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # YCombinator scraper command
    yc_parser = subparsers.add_parser('yc-scraper', help='Run YCombinator scraper')
    yc_parser.add_argument('--periodic', action='store_true', help='Run the scraper periodically')
    yc_parser.add_argument('--interval', type=float, default=24, help='Interval in hours for periodic scraping')
    yc_parser.add_argument('--proxy-api', type=str, help='API URL to fetch proxy list')
    yc_parser.add_argument('--no-proxy', action='store_true', help='Disable proxy usage')
    yc_parser.add_argument('--limit', type=int, help='Limit scraping to N pages (for testing)')
    
    # Add more commands for other backend services here
    # Example:
    # api_parser = subparsers.add_parser('api', help='Run API server')
    # api_parser.add_argument('--port', type=int, default=8000, help='Port to run the API server on')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'yc-scraper':
        asyncio.run(run_ycombinator_scraper(args))
    # Add more command handlers here
    # elif args.command == 'api':
    #     run_api_server(args)
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