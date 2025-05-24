import asyncio
import json
from typing import List, Dict, Optional
from playwright.async_api import Page

class CompanyExtractor:
    """Handles extraction of company data from YCombinator with fallback mechanisms"""
    
    def __init__(self, page: Page):
        self.page = page
        
    async def extract_companies_playwright(self) -> List[Dict]:
        """Extract companies using Playwright locators with error handling"""
        companies = []
        
        try:
            # Wait for results container
            results_container = self.page.locator('div._section_i9oky_163._results_i9oky_343')
            await results_container.wait_for(timeout=5000)
            
            # Get all company links
            company_links = results_container.locator('a._company_i9oky_355')
            count = await company_links.count()
            
            print(f"Found {count} company elements")
            
            for i in range(count):
                try:
                    company_link = company_links.nth(i)
                    
                    # Extract basic company data with fallbacks
                    company_data = await self._extract_single_company_playwright(company_link, i)
                    if company_data:
                        companies.append(company_data)
                        
                except Exception as e:
                    print(f"Error extracting company {i}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in playwright extraction: {e}")
            
        return companies
    
    async def _extract_single_company_playwright(self, company_link, index: int) -> Optional[Dict]:
        """Extract data from a single company element using Playwright"""
        try:
            company_data = {
                'index': index,
                'extraction_method': 'playwright'
            }
            
            # Extract URL
            try:
                company_data['url'] = await company_link.get_attribute('href')
                if company_data['url'] and not company_data['url'].startswith('http'):
                    company_data['url'] = f"https://www.ycombinator.com{company_data['url']}"
            except Exception as e:
                print(f"Error extracting URL for company {index}: {e}")
                company_data['url'] = None
            
            # Extract company name with multiple fallback selectors
            name_selectors = [
                'span._coName_i9oky_470',
                '.company-name',
                '[class*="coName"]',
                'span[class*="Name"]'
            ]
            
            company_data['name'] = await self._extract_text_with_fallbacks(
                company_link, name_selectors, f"company {index} name"
            )
            
            # Extract location
            location_selectors = [
                'span._coLocation_i9oky_486',
                '.company-location',
                '[class*="coLocation"]',
                'span[class*="Location"]'
            ]
            
            company_data['location'] = await self._extract_text_with_fallbacks(
                company_link, location_selectors, f"company {index} location"
            )
            
            # Extract description
            description_selectors = [
                'span._coDescription_i9oky_495',
                '.company-description',
                '[class*="coDescription"]',
                'span[class*="Description"]'
            ]
            
            company_data['description'] = await self._extract_text_with_fallbacks(
                company_link, description_selectors, f"company {index} description"
            )
            
            # Extract tags/pills
            try:
                pills_container = company_link.locator('div._pillWrapper_i9oky_33, .pill-wrapper, [class*="pillWrapper"]')
                
                if await pills_container.count() > 0:
                    pill_links = pills_container.locator('a._tagLink_i9oky_1040, .tag-link, [class*="tagLink"]')
                    pills_count = await pill_links.count()
                    
                    tags = []
                    for j in range(pills_count):
                        try:
                            pill_text = await pill_links.nth(j).inner_text()
                            if pill_text.strip():
                                tags.append(pill_text.strip())
                        except:
                            continue
                    
                    company_data['tags'] = tags
                else:
                    company_data['tags'] = []
                    
            except Exception as e:
                print(f"Error extracting tags for company {index}: {e}")
                company_data['tags'] = []
            
            # Extract logo image
            try:
                img_element = company_link.locator('img')
                if await img_element.count() > 0:
                    company_data['logo_url'] = await img_element.first.get_attribute('src')
                else:
                    company_data['logo_url'] = None
            except:
                company_data['logo_url'] = None
            
            # Only return if we have at least a name or URL
            if company_data.get('name') or company_data.get('url'):
                return company_data
            else:
                print(f"Insufficient data for company {index}")
                return None
                
        except Exception as e:
            print(f"Error extracting company {index}: {e}")
            return None
    
    async def _extract_text_with_fallbacks(self, parent_element, selectors: List[str], context: str) -> Optional[str]:
        """Try multiple selectors to extract text with fallbacks"""
        for selector in selectors:
            try:
                element = parent_element.locator(selector)
                if await element.count() > 0:
                    text = await element.first.inner_text()
                    if text and text.strip():
                        return text.strip()
            except Exception as e:
                continue
        
        print(f"Could not extract {context} with any fallback selector")
        return None
    
    async def extract_companies_javascript(self) -> List[Dict]:
        """Extract companies using JavaScript evaluation as fallback"""
        try:
            js_code = """
            () => {
                const companies = [];
                const resultsContainer = document.querySelector('div._section_i9oky_163._results_i9oky_343, [class*="results"], [class*="Results"]');
                
                if (!resultsContainer) {
                    console.log('Results container not found');
                    return companies;
                }
                
                const companyLinks = resultsContainer.querySelectorAll('a._company_i9oky_355, a[class*="company"], a[href*="/companies/"]');
                
                companyLinks.forEach((link, index) => {
                    try {
                        const company = {
                            index: index,
                            extraction_method: 'javascript'
                        };
                        
                        // Extract URL
                        company.url = link.href || link.getAttribute('href');
                        if (company.url && !company.url.startsWith('http')) {
                            company.url = 'https://www.ycombinator.com' + company.url;
                        }
                        
                        // Extract name with fallbacks
                        const nameSelectors = [
                            'span._coName_i9oky_470',
                            '.company-name',
                            '[class*="coName"]',
                            'span[class*="Name"]'
                        ];
                        
                        for (const selector of nameSelectors) {
                            const nameEl = link.querySelector(selector);
                            if (nameEl && nameEl.textContent.trim()) {
                                company.name = nameEl.textContent.trim();
                                break;
                            }
                        }
                        
                        // Extract location with fallbacks
                        const locationSelectors = [
                            'span._coLocation_i9oky_486',
                            '.company-location',
                            '[class*="coLocation"]',
                            'span[class*="Location"]'
                        ];
                        
                        for (const selector of locationSelectors) {
                            const locationEl = link.querySelector(selector);
                            if (locationEl && locationEl.textContent.trim()) {
                                company.location = locationEl.textContent.trim();
                                break;
                            }
                        }
                        
                        // Extract description with fallbacks
                        const descriptionSelectors = [
                            'span._coDescription_i9oky_495',
                            '.company-description',
                            '[class*="coDescription"]',
                            'span[class*="Description"]'
                        ];
                        
                        for (const selector of descriptionSelectors) {
                            const descEl = link.querySelector(selector);
                            if (descEl && descEl.textContent.trim()) {
                                company.description = descEl.textContent.trim();
                                break;
                            }
                        }
                        
                        // Extract tags
                        const tagsContainer = link.querySelector('div._pillWrapper_i9oky_33, .pill-wrapper, [class*="pillWrapper"]');
                        company.tags = [];
                        
                        if (tagsContainer) {
                            const tagLinks = tagsContainer.querySelectorAll('a._tagLink_i9oky_1040, .tag-link, [class*="tagLink"]');
                            tagLinks.forEach(tagLink => {
                                const tagText = tagLink.textContent.trim();
                                if (tagText) {
                                    company.tags.push(tagText);
                                }
                            });
                        }
                        
                        // Extract logo
                        const imgEl = link.querySelector('img');
                        company.logo_url = imgEl ? imgEl.src : null;
                        
                        // Only add if we have minimum required data
                        if (company.name || company.url) {
                            companies.push(company);
                        }
                        
                    } catch (error) {
                        console.log('Error extracting company', index, error);
                    }
                });
                
                return companies;
            }
            """
            
            companies = await self.page.evaluate(js_code)
            print(f"JavaScript extraction found {len(companies)} companies")
            return companies
            
        except Exception as e:
            print(f"Error in JavaScript extraction: {e}")
            return []

async def scroll_and_load_more(page: Page, limit_pages: Optional[int] = None) -> bool:
    """Scroll to load more companies with pagination support"""
    try:
        previous_count = 0
        pages_loaded = 0
        max_attempts = 3
        
        while True:
            # Check if we've hit the page limit
            if limit_pages and pages_loaded >= limit_pages:
                print(f"Reached page limit: {limit_pages}")
                break
                
            # Get current company count
            try:
                current_count = await page.locator('a._company_i9oky_355').count()
            except:
                current_count = await page.evaluate("""
                    () => document.querySelectorAll('a[href*="/companies/"]').length
                """)
            
            print(f"Current company count: {current_count}")
            
            # If no new companies loaded, try to load more
            if current_count == previous_count:
                # Check for loading indicator
                loading_indicator = page.locator('text=Loading more, .loading, [class*="loading"]')
                is_loading = await loading_indicator.count() > 0
                
                if is_loading:
                    print("Waiting for loading to complete...")
                    await page.wait_for_timeout(2000)
                    continue
                
                # Try scrolling to bottom
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(1000)
                
                # Check for load more button or infinite scroll trigger
                load_more_selectors = [
                    'button:has-text("Load more")',
                    'button:has-text("Show more")',
                    '[class*="loadMore"]',
                    '[class*="showMore"]'
                ]
                
                for selector in load_more_selectors:
                    try:
                        load_more_btn = page.locator(selector)
                        if await load_more_btn.count() > 0:
                            await load_more_btn.click()
                            await page.wait_for_timeout(2000)
                            break
                    except:
                        continue
                
                # Wait and check again
                await page.wait_for_timeout(2000)
                new_count = await page.locator('a._company_i9oky_355').count()
                
                if new_count == current_count:
                    max_attempts -= 1
                    if max_attempts <= 0:
                        print("No more companies to load")
                        break
                else:
                    max_attempts = 3  # Reset attempts if new content loaded
                    pages_loaded += 1
            else:
                previous_count = current_count
                pages_loaded += 1
                max_attempts = 3  # Reset attempts
                
            await page.wait_for_timeout(1000)
        
        return True
        
    except Exception as e:
        print(f"Error during scrolling: {e}")
        return False

async def extract_all_companies(page: Page, limit_pages: Optional[int] = None) -> List[Dict]:
    """Main function to extract all companies with both approaches"""
    extractor = CompanyExtractor(page)
    
    # First, scroll to load all companies
    print("Starting infinite scroll to load all companies...")
    await scroll_and_load_more(page, limit_pages)
    
    # Try Playwright approach first
    print("Attempting extraction with Playwright locators...")
    companies = await extractor.extract_companies_playwright()
    
    # If Playwright approach fails or returns insufficient data, try JavaScript
    if len(companies) < 10:  # Arbitrary threshold
        print("Playwright extraction insufficient, trying JavaScript fallback...")
        js_companies = await extractor.extract_companies_javascript()
        
        if len(js_companies) > len(companies):
            print("JavaScript extraction returned more companies, using those")
            companies = js_companies
    
    # Clean and validate data
    cleaned_companies = []
    for company in companies:
        if company.get('name') or company.get('url'):
            # Ensure required fields exist
            company.setdefault('name', 'Unknown')
            company.setdefault('location', '')
            company.setdefault('description', '')
            company.setdefault('tags', [])
            company.setdefault('logo_url', None)
            company.setdefault('url', None)
            
            cleaned_companies.append(company)
    
    return cleaned_companies
