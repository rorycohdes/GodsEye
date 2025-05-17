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

# Add the parent directory to sys.path to import from backend.utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.proxy_manager import get_random_proxy, parse_proxy, get_proxy_info_string, get_random_user_agent, fetch_proxies

from dotenv import load_dotenv
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


async def scrape_ycombinator_companies(proxies, limit_pages=None):
    """
    Scrape YCombinator companies using proxies.
    
    Args:
        proxies: List of proxy dictionaries (required)
        limit_pages: Optional limit on number of pages to scrape
        
    Returns:
        List of company dictionaries
    """
    if not proxies:
        raise ValueError("Proxies are required for scraping")
        
    async with async_playwright() as p:
        browser_options = {}
        
        # Configure proxy
        try:
            proxy_dict = get_random_proxy(proxies)
            proxy_config = parse_proxy(proxy_dict)
            browser_options["proxy"] = proxy_config
            print(f"Using proxy: {get_proxy_info_string(proxy_dict)}")
        except Exception as e:
            raise ValueError(f"Error setting up proxy: {e}")
        
        # Launch browser with proxy
        browser = await p.chromium.launch(headless=False, **browser_options)  # Set to True for production
        
        # Create a new context with a random user agent
        context = await browser.new_context(
            user_agent=get_random_user_agent()
        )
        
        # Create a new page from the context
        page = await context.new_page()
        
        try:
            # Navigate to the companies page
            await page.goto('https://www.ycombinator.com/companies')
            print('Navigated to YCombinator companies page')
            
            # Click on "All batches" checkbox if it's not already checked
            all_batches_checkbox = page.locator('div._facet_i9oky_85 h4:has-text("Batch") ~ label:has-text("All batches") input[type="checkbox"]')
            
            is_checked = await all_batches_checkbox.is_checked()
            if not is_checked:
                await all_batches_checkbox.click()
                print('Clicked "All batches" checkbox')
            else:
                print('"All batches" checkbox is already checked')
            
            # Click the "Show X companies" button to load the results
            show_results_button = page.locator('div._showResults_i9oky_169 button')
            await show_results_button.click()
            print('Clicked "Show companies" button')
            
            # Wait for the results to load
            await page.wait_for_selector('div._section_i9oky_163._results_i9oky_343 a._company_i9oky_355', timeout=30000)
            print('Results loaded successfully')
            
            # Function to scrape the current page of companies
            async def scrape_current_page():
                return await page.evaluate('''() => {
                    const companyElements = document.querySelectorAll('div._section_i9oky_163._results_i9oky_343 a._company_i9oky_355');
                    const companies = [];
                    
                    companyElements.forEach(company => {
                        // Extract company URL
                        const url = company.getAttribute('href');
                        
                        // Extract company name
                        const nameElement = company.querySelector('span._coName_i9oky_470');
                        const name = nameElement ? nameElement.textContent.trim() : '';
                        
                        // Extract company location
                        const locationElement = company.querySelector('span._coLocation_i9oky_486');
                        const location = locationElement ? locationElement.textContent.trim() : '';
                        
                        // Extract company description
                        const descriptionElement = company.querySelector('span._coDescription_i9oky_495');
                        const description = descriptionElement ? descriptionElement.textContent.trim() : '';
                        
                        // Extract batch information
                        const batchElement = company.querySelector('._pillWrapper_i9oky_33 a[href^="/companies?batch="] span');
                        const batch = batchElement ? batchElement.textContent.replace(/^\\S+\\s+/, '') : ''; // Remove YC logo
                        
                        // Extract industry tags
                        const industryElements = company.querySelectorAll('._pillWrapper_i9oky_33 a[href^="/companies?industry="] span');
                        const industries = Array.from(industryElements).map(el => el.textContent.trim());
                        
                        // Extract logo URL
                        const logoElement = company.querySelector('img');
                        const logoUrl = logoElement ? logoElement.getAttribute('src') : '';
                        
                        // Add the company data to the array
                        companies.push({
                            name,
                            url,
                            location,
                            description,
                            batch,
                            industries,
                            logoUrl
                        });
                    });
                    
                    return companies;
                }''')
            
            # Initial scrape
            all_companies = []
            initial_companies = await scrape_current_page()
            all_companies.extend(initial_companies)
            print(f"Initially scraped {len(initial_companies)} companies")
            
            # Check if there's pagination and handle it
            has_pagination = await page.locator('nav.pagination').count() > 0
            
            if has_pagination:
                # Get the total number of pages
                pagination_text = await page.locator('nav.pagination').text_content()
                import re
                match = re.search(r'of (\d+)', pagination_text)
                if match:
                    total_pages = int(match.group(1))
                    
                    # Apply page limit if specified
                    if limit_pages and limit_pages > 0:
                        total_pages = min(total_pages, limit_pages)
                        
                    print(f"Found pagination with {total_pages} total pages")
                    
                    # Loop through all pages
                    for current_page in range(2, total_pages + 1):
                        # Click the next page button
                        await page.locator('button.pagination-next').click()
                        print(f"Navigated to page {current_page}")
                        
                        # Wait for the page to load
                        await page.wait_for_timeout(2000)  # Adjust timeout as needed
                        
                        # Scrape the current page
                        page_companies = await scrape_current_page()
                        all_companies.extend(page_companies)
                        print(f"Scraped {len(page_companies)} companies from page {current_page}")
                        
                        # Optional: add a delay between page navigations
                        await page.wait_for_timeout(1000)
            
            # Save the data to a file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = Path("ycombinator_data")
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / f"ycombinator_companies_{timestamp}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_companies, f, indent=2)
            
            print(f"Successfully scraped {len(all_companies)} companies in total")
            print(f"Data saved to {output_file}")
            
            return all_companies
            
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
        finally:
            await browser.close()

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
        return proxies
    else:
        raise ValueError("No proxies available. Cannot proceed without proxies.")

# Function to run the scraper periodically
async def run_periodic_scraper(interval_hours=24, proxy_api_url=None, api_key=None):
    while True:
        print(f"Starting scrape at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            # Load proxies before each scrape to ensure fresh proxies
            proxies = await load_proxies(proxy_api_url, api_key)
            await scrape_ycombinator_companies(proxies=proxies)
        except Exception as e:
            print(f"Scrape failed: {e}")
            print("Will retry at next interval")
        
        # Wait for the next interval
        next_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Next scrape scheduled at: {next_run}")
        await asyncio.sleep(interval_hours * 3600)  # Convert hours to seconds

# Main execution
#* The main function if you ever want to run this file directly
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='YCombinator Company Scraper')
    parser.add_argument('--periodic', action='store_true', help='Run the scraper periodically')
    parser.add_argument('--interval', type=float, default=24, help='Interval in hours for periodic scraping')
    parser.add_argument('--proxy-api', type=str, help='API URL to fetch proxy list')
    parser.add_argument('--api-key', type=str, help='API key for proxy service')
    parser.add_argument('--limit', type=int, help='Limit scraping to N pages (for testing)')
    
    args = parser.parse_args()
    
    # Debug the API key values
    print(f"API key from args: '{args.api_key}'")
    print(f"API key from env: '{webshare_api_key}'")
    
    # Use API key from environment if not provided in args
    api_key = args.api_key or webshare_api_key
    print(f"Final API key (type: {type(api_key)}): '{api_key}'")
    
    if not api_key:
        print("ERROR: No API key provided. Set WEBSHARE_API_KEY in .env file or use --api-key")
        sys.exit(1)
    
    if args.periodic:
        print(f"Starting periodic scraper with {args.interval} hour interval")
        asyncio.run(run_periodic_scraper(
            interval_hours=args.interval,
            proxy_api_url=args.proxy_api,
            api_key=api_key
        ))
    else:
        # Run once
        async def run_once():
            try:
                proxies = await load_proxies(args.proxy_api, api_key)
                return await scrape_ycombinator_companies(
                    proxies=proxies,
                    limit_pages=args.limit
                )
            except ValueError as e:
                print(f"ERROR: {e}")
                sys.exit(1)
                
        asyncio.run(run_once())