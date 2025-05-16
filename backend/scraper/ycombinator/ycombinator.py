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
from utils.proxy_manager import get_random_proxy, parse_proxy, get_proxy_info_string, get_random_user_agent

async def scrape_ycombinator_companies(proxies=None, use_proxy=True, limit_pages=None):
    async with async_playwright() as p:
        browser_options = {}
        
        # Configure proxy if available and enabled
        if proxies and use_proxy:
            try:
                proxy_dict = get_random_proxy(proxies)
                proxy_config = parse_proxy(proxy_dict)
                browser_options["proxy"] = proxy_config
                print(f"Using proxy: {get_proxy_info_string(proxy_dict)}")
            except Exception as e:
                print(f"Error setting up proxy: {e}. Continuing without proxy.")
        
        # Launch browser with proxy if configured
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
async def load_proxies(proxy_api_url=None):
    """
    Load proxies from an API endpoint or return a default list.
    
    Args:
        proxy_api_url: URL to fetch proxies from
        
    Returns:
        List of proxy dictionaries
    """
    if proxy_api_url:
        try:
            response = requests.get(proxy_api_url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Failed to load proxies from API: {e}")
    
    # Return a default list or empty list if API fails
    # You should replace this with your actual proxy list or API
    return [
        {
            "username": "your_username",
            "password": "your_password",
            "proxy_address": "proxy.example.com",
            "port": "8080",
            "country_code": "US"
        }
    ]

# Function to run the scraper periodically
async def run_periodic_scraper(interval_hours=24, proxy_api_url=None, use_proxy=True):
    while True:
        print(f"Starting scrape at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            # Load proxies before each scrape to ensure fresh proxies
            proxies = await load_proxies(proxy_api_url) if use_proxy else None
            await scrape_ycombinator_companies(proxies=proxies, use_proxy=use_proxy)
        except Exception as e:
            print(f"Scrape failed: {e}")
        
        # Wait for the next interval
        next_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Next scrape scheduled at: {next_run}")
        await asyncio.sleep(interval_hours * 3600)  # Convert hours to seconds

# Main execution
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='YCombinator Company Scraper')
    parser.add_argument('--periodic', action='store_true', help='Run the scraper periodically')
    parser.add_argument('--interval', type=float, default=24, help='Interval in hours for periodic scraping')
    parser.add_argument('--proxy-api', type=str, help='API URL to fetch proxy list')
    parser.add_argument('--no-proxy', action='store_true', help='Disable proxy usage')
    
    args = parser.parse_args()
    
    if args.periodic:
        print(f"Starting periodic scraper with {args.interval} hour interval")
        print(f"Proxy usage: {'Disabled' if args.no_proxy else 'Enabled'}")
        asyncio.run(run_periodic_scraper(
            interval_hours=args.interval,
            proxy_api_url=args.proxy_api,
            use_proxy=not args.no_proxy
        ))
    else:
        # Run once
        async def run_once():
            proxies = await load_proxies(args.proxy_api)
            return await scrape_ycombinator_companies(
                proxies=proxies,
                use_proxy=not args.no_proxy
            )
        asyncio.run(run_once())