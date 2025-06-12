import asyncio
import json
import time
import random
import requests
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright
import sys
import os
import pandas as pd
from typing import List, Dict, Optional

# Add the parent directory to sys.path to import from backend.utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.proxy_manager import get_random_proxy, parse_proxy, get_proxy_info_string, get_random_user_agent, fetch_proxies

# Import database integration utilities
from utils.database_integration import insert_companies_to_database
from config.settings import get_settings

from dotenv import load_dotenv
from scraper.ycombinator.company_extractor import extract_all_companies
import os

# Fix the path to the .env file - use absolute path
# The current approach with '../.env' is relative and may not work correctly
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
env_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path=env_path)

webshare_api_key = os.getenv("WEBSHARE_API_KEY")
print(f"webshare_api_key: {webshare_api_key}")

# If the key is still None, try to load from a different location
if webshare_api_key is None:
    # Try loading from the current directory
    load_dotenv()
    webshare_api_key = os.getenv("WEBSHARE_API_KEY")
    print(f"Retrying with default .env path, webshare_api_key: {webshare_api_key}")



async def scrape_ycombinator_companies(proxies, max_companies=None, show_live=False, insert_to_db=True, table_name=None):
    """
    Scrape YCombinator companies using proxies with batch extraction.
    
    Args:
        proxies: List of proxy dictionaries (required)
        max_companies: Optional maximum number of companies to extract
        show_live: Whether to display companies as they are scraped
        insert_to_db: Whether to insert scraped data into database (default: True)
        table_name: Database table name for insertion
        
    Returns:
        List of company dictionaries
    """
    if not proxies:
        raise ValueError("Proxies are required for scraping")
    
    # Try multiple proxies if one fails
    max_proxy_attempts = min(3, len(proxies))
    
    for attempt in range(max_proxy_attempts):
        print(f"\n🔄 Proxy attempt {attempt + 1}/{max_proxy_attempts}")
        
        async with async_playwright() as p:
            browser_options = {}
            
            # Configure proxy
            try:
                proxy_dict = get_random_proxy(proxies)
                proxy_config = parse_proxy(proxy_dict)
                browser_options["proxy"] = proxy_config
                print(f"Using proxy: {get_proxy_info_string(proxy_dict)}")
            except Exception as e:
                print(f"Error setting up proxy: {e}")
                if attempt == max_proxy_attempts - 1:
                    raise ValueError(f"Failed to setup proxy after {max_proxy_attempts} attempts")
                continue
            
            # Launch browser with proxy
            browser = await p.chromium.launch(
                headless=False, 
                **browser_options,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu',
                    '--window-size=1920x1080'
                ]
            )
            
            # Create a new context with a random user agent
            context = await browser.new_context(
                user_agent=get_random_user_agent(),
                viewport={'width': 1920, 'height': 1080}
            )
            
            # Create a new page from the context
            page = await context.new_page()
            
            try:
                # Test proxy connection first
                print("🔍 Testing proxy connection...")
                try:
                    # Try a simple request first to validate proxy
                    await page.goto('https://httpbin.org/ip', timeout=15000)
                    await page.wait_for_load_state('networkidle', timeout=10000)
                    print("✅ Proxy connection test successful")
                except Exception as proxy_test_error:
                    print(f"❌ Proxy connection test failed: {proxy_test_error}")
                    await browser.close()
                    if attempt == max_proxy_attempts - 1:
                        raise ValueError(f"All proxy attempts failed. Last error: {proxy_test_error}")
                    continue
                
                # Navigate to the companies page
                print("🌐 Navigating to YCombinator companies page...")
                await page.goto('https://www.ycombinator.com/companies', timeout=30000)
                print('✅ Successfully navigated to YCombinator companies page')
                
                # Wait for the page to load completely
                await page.wait_for_load_state('networkidle', timeout=20000)
                await page.wait_for_timeout(3000)  # Additional wait for dynamic content
                
                # Ensure "All batches" checkbox is checked
                print('Ensuring "All batches" checkbox is checked...')
                
                try:
                    # Find the "All batches" checkbox within _facet_i9oky_85
                    all_batches_selectors = [
                        'div._facet_i9oky_85 label:has-text("All batches") input[type="checkbox"]',
                        'label:has-text("All batches") input[type="checkbox"]',
                        'div._facet_i9oky_85 input[type="checkbox"][checked]'
                    ]
                    
                    all_batches_checkbox = None
                    for selector in all_batches_selectors:
                        try:
                            checkbox_locator = page.locator(selector).first
                            if await checkbox_locator.count() > 0:
                                all_batches_checkbox = checkbox_locator
                                print(f'Found "All batches" checkbox with selector: {selector}')
                                break
                        except Exception as e:
                            continue
                    
                    if all_batches_checkbox:
                        is_checked = await all_batches_checkbox.is_checked()
                        print(f'"All batches" checkbox is checked: {is_checked}')
                        
                        if not is_checked:
                            # Click the label instead of the input for better reliability
                            label_selector = 'div._facet_i9oky_85 label:has-text("All batches")'
                            label_element = page.locator(label_selector).first
                            if await label_element.count() > 0:
                                await label_element.click()
                                print('Clicked "All batches" label')
                                await page.wait_for_timeout(2000)
                            else:
                                await all_batches_checkbox.click()
                                print('Clicked "All batches" checkbox')
                                await page.wait_for_timeout(2000)
                        else:
                            print('"All batches" is already checked')
                    else:
                        print('Could not find "All batches" checkbox, proceeding anyway...')
                        
                except Exception as e:
                    print(f'Error handling checkbox: {e}, proceeding anyway...')
                
                # Wait for and access the results section directly
                print('Looking for results section...')
                
                try:
                    # Wait for the results container to be present
                    results_container = page.locator('div._section_i9oky_163._results_i9oky_343')
                    await results_container.wait_for(timeout=15000)
                    print('Results container found')
                    
                    # Wait for company elements to be present
                    company_elements = page.locator('a._company_i9oky_355')
                    await company_elements.first.wait_for(timeout=10000)
                    
                    # Count initial companies
                    initial_count = await company_elements.count()
                    print(f'Found {initial_count} companies in results section')
                    
                    if initial_count == 0:
                        print('No companies found in results section')
                        
                except Exception as e:
                    print(f'Error accessing results section: {e}')
                    # Try to find results with alternative selectors
                    try:
                        alt_results = page.locator('[class*="_results_"]')
                        if await alt_results.count() > 0:
                            print('Found results with alternative selector')
                        else:
                            print('No results section found with any selector')
                            raise Exception('Could not find results section')
                    except Exception as alt_error:
                        raise Exception(f'Could not access results section: {alt_error}')
                
                print('Successfully accessed results section')
                
                # Show cap information if set
                if max_companies:
                    print(f'🔢 Company cap set to: {max_companies} companies')
                    print(f'📦 Extraction will proceed in batches with scrolling')
                
                # Extract all companies using batch method with infinite scroll and cap
                companies = await extract_all_companies(page, max_companies, show_live)
                
                # Display detailed summary of scraped companies
                if companies:
                    print(f"\n📊 SCRAPED COMPANIES SUMMARY ({len(companies)} total):")
                    print("=" * 80)
                    
                    # Show company breakdown by batch (assuming 20 companies per batch for display)
                    batch_size = 20
                    for batch_start in range(0, min(len(companies), 100), batch_size):  # Show first 100
                        batch_end = min(batch_start + batch_size, len(companies))
                        batch_num = (batch_start // batch_size) + 1
                        
                        print(f"\n📦 Batch {batch_num} Companies ({batch_start + 1}-{batch_end}):")
                        for i in range(batch_start, batch_end):
                            company = companies[i]
                            name = company.get('name', 'Unknown')[:30].ljust(30)
                            location = company.get('location', 'N/A')[:20].ljust(20)
                            tags = ', '.join(company.get('tags', [])[:2])[:25].ljust(25)
                            print(f"   {i+1:3d}. {name} | {location} | {tags}")
                    
                    if len(companies) > 100:
                        print(f"\n   ... and {len(companies) - 100} more companies")
                    
                    print("=" * 80)
                    
                    # Show industry breakdown
                    industries = {}
                    for company in companies:
                        for tag in company.get('tags', []):
                            if tag in ['B2B', 'Consumer', 'Fintech', 'Healthcare', 'Education', 'Industrials']:
                                industries[tag] = industries.get(tag, 0) + 1
                    
                    if industries:
                        print("🏭 Industry Breakdown:")
                        for industry, count in sorted(industries.items(), key=lambda x: x[1], reverse=True):
                            print(f"   {industry}: {count} companies")
                        print()
                
                if max_companies and len(companies) >= max_companies:
                    print(f'🛑 Reached company cap: {len(companies)}/{max_companies} companies extracted')
                else:
                    print(f'✅ Successfully extracted {len(companies)} companies via batch method')
                
                # Insert into database if requested
                if companies and insert_to_db:
                    try:
                        await insert_companies_to_database(companies, table_name, "ycombinator_scraper")
                    except Exception as e:
                        print(f"❌ Database insertion failed: {e}")
                        print("📁 Saving to JSON file as fallback...")
                        # Save to JSON as fallback
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"ycombinator_companies_fallback_{timestamp}.json"
                        with open(filename, 'w') as f:
                            json.dump(companies, f, indent=2)
                        print(f"💾 Saved {len(companies)} companies to {filename}")
                
                return companies
                
            except Exception as e:
                print(f"❌ Error during scraping with proxy attempt {attempt + 1}: {e}")
                
                await browser.close()
                
                if attempt == max_proxy_attempts - 1:
                    print("🚫 All proxy attempts exhausted")
                    raise e
                else:
                    print(f"🔄 Trying next proxy (attempt {attempt + 2})...")
                    await asyncio.sleep(2)  # Brief delay before retry
                    continue
            
            finally:
                try:
                    await browser.close()
                except:
                    pass

# Function to load proxies from an API or file
async def load_proxies(proxy_api_url=None, api_key=None):
    """
    Load proxies from an API endpoint.
    
    Args:
        proxy_api_url: URL to fetch proxies from
        api_key: Optional API key for authorization
        
    Returns:
        List of proxy dictionaries
    
    Raises:
        ValueError: If no proxies are available
    """
    # Default to Webshare API if no URL is provided
    if not proxy_api_url:
        proxy_api_url = "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=25"
    
    # Debug the API key
    print(f"API key in load_proxies: {'Present' if api_key else 'Missing'}")
    
    # Use the fetch_proxies function from proxy_manager
    proxies = fetch_proxies(proxy_api_url, api_key)
    
    if proxies:
        print(f"Successfully loaded {len(proxies)} proxies from API")
        
        # Validate proxy format
        valid_proxies = []
        for proxy in proxies:
            if all(key in proxy for key in ['proxy_address', 'port']):
                valid_proxies.append(proxy)
            else:
                print(f"⚠️  Skipping invalid proxy format: {proxy}")
        
        if valid_proxies:
            print(f"✅ {len(valid_proxies)} valid proxies ready for use")
            return valid_proxies
        else:
            raise ValueError("No valid proxies found in the response")
    else:
        raise ValueError("No proxies available. Cannot proceed without proxies.")

# Function to run the scraper periodically
async def run_periodic_scraper(interval_hours=24, proxy_api_url=None, api_key=None, max_companies_per_run=None, show_live=False, insert_to_db=True, table_name=None):
    """
    Run the scraper periodically with batch extraction, detailed logging, and database insertion.
    
    Args:
        interval_hours: Hours between scrape runs
        proxy_api_url: URL to fetch proxies from
        api_key: API key for proxy service
        max_companies_per_run: Maximum companies to scrape per run (optional)
        show_live: Whether to display companies as they are scraped
        insert_to_db: Whether to insert scraped data into database
        table_name: Database table name for insertion
    """
    run_count = 0
    total_companies_scraped = 0
    all_time_companies = []  # Track all companies across runs
    
    while True:
        run_count += 1
        print(f"\n{'='*60}")
        print(f"🚀 Starting periodic scrape run #{run_count} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📦 Using batch extraction with scrolling method")
        print(f"💾 Database insertion: {'Enabled' if insert_to_db else 'Disabled'}")
        if insert_to_db:
            print(f"🗄️  Target table: {table_name or 'default'}")
        
        if max_companies_per_run:
            print(f"📊 Company cap for this run: {max_companies_per_run}")
        
        print(f"📈 Total companies scraped so far: {total_companies_scraped}")
        print(f"{'='*60}")
        
        try:
            # Load proxies before each scrape to ensure fresh proxies
            proxies = await load_proxies(proxy_api_url, api_key)
            
            # Run scraper with company cap, batch method, and database insertion
            companies = await scrape_ycombinator_companies(
                proxies=proxies, 
                max_companies=max_companies_per_run,
                show_live=show_live,
                insert_to_db=insert_to_db,
                table_name=table_name
            )
            
            companies_this_run = len(companies) if companies else 0
            total_companies_scraped += companies_this_run
            
            # Add to all-time collection (avoid duplicates by URL)
            if companies:
                existing_urls = {c.get('url') for c in all_time_companies}
                new_companies = [c for c in companies if c.get('url') not in existing_urls]
                all_time_companies.extend(new_companies)
                
                print(f"📊 NEW companies this run: {len(new_companies)}")
                
                # Log names of new companies found in this run
                if new_companies:
                    print(f"\n🆕 New companies discovered in run #{run_count}:")
                    for i, company in enumerate(new_companies[:10], 1):  # Show first 10 new
                        name = company.get('name', 'Unknown')
                        location = company.get('location', 'N/A')
                        print(f"   {i:2d}. {name} ({location})")
                    if len(new_companies) > 10:
                        print(f"   ... and {len(new_companies) - 10} more new companies")
            
            print(f"✅ Scrape run #{run_count} completed successfully")
            print(f"📊 Companies in this run: {companies_this_run}")
            print(f"📈 Total unique companies: {len(all_time_companies)}")
            
            # Show periodic summary of top companies
            if all_time_companies and run_count % 3 == 0:  # Every 3 runs
                print(f"\n🏆 TOP COMPANIES ACROSS ALL RUNS:")
                print("-" * 60)
                top_companies = sorted(all_time_companies, 
                                     key=lambda x: len(x.get('tags', [])), reverse=True)[:5]
                for i, company in enumerate(top_companies, 1):
                    name = company.get('name', 'Unknown')[:30]
                    tag_count = len(company.get('tags', []))
                    location = company.get('location', 'N/A')[:15]
                    print(f"  {i}. {name} ({tag_count} tags, {location})")
                print("-" * 60)
            
            if max_companies_per_run and companies_this_run >= max_companies_per_run:
                print(f"🔢 Hit company cap of {max_companies_per_run} for this run")
            
        except Exception as e:
            print(f"❌ Scrape run #{run_count} failed: {e}")
            print("🔄 Will retry at next interval")
        
        # Calculate next run time
        next_run_time = datetime.now()
        next_run_time = next_run_time.replace(second=0, microsecond=0)
        next_run_time = next_run_time.replace(hour=(next_run_time.hour + int(interval_hours)) % 24)
        
        print(f"\n⏰ Next scrape run #{run_count + 1} scheduled for: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏳ Waiting {interval_hours} hours...")
        
        await asyncio.sleep(interval_hours * 3600)  # Convert hours to seconds

# Main execution
#* The main function if you ever want to run this file directly
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='YCombinator Company Scraper with Database Integration and Schema Validation')
    parser.add_argument('--once', action='store_true', help='Run the scraper once instead of periodically')
    parser.add_argument('--interval', type=float, default=24, help='Interval in hours for periodic scraping')
    parser.add_argument('--proxy-api', type=str, help='API URL to fetch proxy list')
    parser.add_argument('--api-key', type=str, help='API key for proxy service')
    parser.add_argument('--cap', type=int, default=50, help='Maximum number of companies to scrape per run (default: 50)')
    parser.add_argument('--show-live', action='store_true', default=True, help='Show companies as they are scraped (live mode) - enabled by default')
    parser.add_argument('--no-db', action='store_true', help='Disable database insertion (save to JSON only)')
    parser.add_argument('--table-name', type=str, help='Database table name (uses config default if not specified)')
    parser.add_argument('--no-ai', action='store_true', help='Disable AI insights generation')
    parser.add_argument('--no-embeddings', action='store_true', help='Disable embedding generation')
    
    args = parser.parse_args()
    
    # Load settings
    settings = get_settings()
    
    # Override settings based on args
    if args.no_ai:
        settings.scraper.enable_ai_insights = False
    if args.no_embeddings:
        settings.scraper.enable_embeddings = False
    
    table_name = args.table_name or settings.scraper.default_table_name
    
    # Debug the API key values
    print(f"API key from args: '{args.api_key}'")
    print(f"API key from env: '{webshare_api_key}'")
    
    # Use API key from environment if not provided in args
    api_key = args.api_key or webshare_api_key
    print(f"Final API key (type: {type(api_key)}): '{api_key}'")
    
    if not api_key:
        print("ERROR: No API key provided. Set WEBSHARE_API_KEY in .env file or use --api-key")
        sys.exit(1)
    
    # Show configuration
    print(f"\n🔧 Scraper Configuration (with Schema Validation):")
    print(f"   📊 Company cap per run: {args.cap}")
    print(f"   🔄 Periodic mode: {'No' if args.once else 'Yes'}")
    print(f"   👁️  Live display: {'Yes' if args.show_live else 'No'}")
    print(f"   💾 Database insertion: {'No' if args.no_db else 'Yes'}")
    print(f"   🤖 AI insights: {'Yes' if settings.scraper.enable_ai_insights else 'No'}")
    print(f"   🎯 Embeddings: {'Yes' if settings.scraper.enable_embeddings else 'No'}")
    if not args.no_db:
        print(f"   🗄️  Database table: {table_name}")
    print(f"   🔗 Proxy retry attempts: 3")
    print(f"   📋 Schema validation: Enabled")
    if not args.once:
        print(f"   ⏰ Interval: {args.interval} hours")
    
    if args.once:
        # Run once
        async def run_once():
            try:
                proxies = await load_proxies(args.proxy_api, api_key)
                return await scrape_ycombinator_companies(
                    proxies=proxies,
                    max_companies=args.cap,
                    show_live=args.show_live,
                    insert_to_db=not args.no_db,
                    table_name=table_name
                )
            except ValueError as e:
                print(f"ERROR: {e}")
                sys.exit(1)
                
        print(f"\n🚀 Starting single scrape run...")
        companies = asyncio.run(run_once())
        
        # Save to file for backup (even if inserted to DB)
        if companies and not args.no_db:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ycombinator_companies_backup_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(companies, f, indent=2)
            print(f"💾 Backup saved: {len(companies)} companies to {filename}")
        elif companies:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ycombinator_companies_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(companies, f, indent=2)
            print(f"💾 Saved {len(companies)} companies to {filename}")
    else:
        print(f"\n🚀 Starting periodic scraper...")
        asyncio.run(run_periodic_scraper(
            interval_hours=args.interval,
            proxy_api_url=args.proxy_api,
            api_key=api_key,
            max_companies_per_run=args.cap,
            show_live=True,
            insert_to_db=not args.no_db,
            table_name=table_name
        ))