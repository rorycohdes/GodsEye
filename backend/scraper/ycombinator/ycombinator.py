import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

async def scrape_ycombinator_companies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set to True for production
        page = await browser.new_page()
        
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

# Function to run the scraper periodically
async def run_periodic_scraper(interval_hours=24):
    while True:
        print(f"Starting scrape at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            await scrape_ycombinator_companies()
        except Exception as e:
            print(f"Scrape failed: {e}")
        
        # Wait for the next interval
        next_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Next scrape scheduled at: {next_run}")
        await asyncio.sleep(interval_hours * 3600)  # Convert hours to seconds

# Run the scraper once
# asyncio.run(scrape_ycombinator_companies())

# Or run periodically (e.g., every 24 hours)
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--periodic":
        interval = 24  # Default to 24 hours
        if len(sys.argv) > 2:
            try:
                interval = float(sys.argv[2])
            except ValueError:
                print(f"Invalid interval: {sys.argv[2]}. Using default 24 hours.")
        
        print(f"Starting periodic scraper with {interval} hour interval")
        asyncio.run(run_periodic_scraper(interval))
    else:
        # Run once
        asyncio.run(scrape_ycombinator_companies())