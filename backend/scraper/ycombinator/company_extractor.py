import asyncio
import json
from typing import List, Dict, Optional, Set
from playwright.async_api import Page

class CompanyExtractor:
    """Handles extraction of company data from YCombinator with fallback mechanisms"""
    
    def __init__(self, page: Page, show_live: bool = False):
        self.page = page
        self.show_live = show_live
        self.extracted_urls: Set[str] = set()  # Track extracted companies to avoid duplicates
        
    async def extract_companies_in_batches(self, max_companies: Optional[int] = None) -> List[Dict]:
        """Extract companies in batches with scrolling and logging"""
        all_companies = []
        batch_number = 1
        
        print("🚀 Starting batch extraction with scrolling...")
        
        while True:
            # Extract current batch of visible companies
            print(f"\n📦 Extracting batch #{batch_number}...")
            batch_companies = await self._extract_current_batch()
            
            if not batch_companies:
                print(f"No companies found in batch #{batch_number}")
                break
            
            # Filter out duplicates and add to all companies
            new_companies = []
            for company in batch_companies:
                company_url = company.get('url', '')
                if company_url and company_url not in self.extracted_urls:
                    self.extracted_urls.add(company_url)
                    new_companies.append(company)
                    all_companies.append(company)
            
            print(f"✅ Batch #{batch_number}: Found {len(batch_companies)} companies, {len(new_companies)} new")
            
            # Log company names from this batch
            if new_companies:
                print(f"📋 Companies in batch #{batch_number}:")
                for i, company in enumerate(new_companies, 1):
                    name = str(company.get('name', 'Unknown') or 'Unknown')
                    location = str(company.get('location', 'N/A') or 'N/A')
                    tags = ', '.join(str(tag) for tag in (company.get('tags', []) or [])[:2])
                    print(f"   {i:2d}. {name:<30} | {location:<20} | {tags}")
            
            # Check if we've reached the company cap
            if max_companies and len(all_companies) >= max_companies:
                print(f"🔢 Reached company cap: {len(all_companies)}/{max_companies}")
                break
            
            # Try to scroll and load more companies
            print(f"🔄 Scrolling to load more companies...")
            more_loaded = await self._scroll_and_load_more()
            
            if not more_loaded:
                print("🏁 No more companies to load")
                break
            
            batch_number += 1
            
            # Add delay between batches
            await asyncio.sleep(1)
        
        print(f"\n📊 Total extraction complete: {len(all_companies)} companies across {batch_number} batches")
        return all_companies[:max_companies] if max_companies else all_companies
    
    async def _extract_current_batch(self) -> List[Dict]:
        """Extract companies currently visible on the page"""
        try:
            # Wait for results container
            results_container = self.page.locator('div._section_i9oky_163._results_i9oky_343')
            await results_container.wait_for(timeout=5000)
            
            # Get all company links currently visible
            company_links = results_container.locator('a._company_i9oky_355')
            count = await company_links.count()
            
            companies = []
            for i in range(count):
                try:
                    company_link = company_links.nth(i)
                    company_data = await self._extract_single_company_playwright(company_link, i)
                    if company_data:
                        companies.append(company_data)
                except Exception as e:
                    print(f"Error extracting company {i}: {e}")
                    continue
            
            return companies
            
        except Exception as e:
            print(f"Error in batch extraction: {e}")
            return []
    
    async def _scroll_and_load_more(self) -> bool:
        """Scroll to load more companies and return True if new content was loaded"""
        try:
            # Get current company count before scrolling
            initial_count = await self.page.locator('a._company_i9oky_355').count()
            
            # Scroll to bottom
            await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await self.page.wait_for_timeout(2000)
            
            # Check for and click load more button if exists
            load_more_selectors = [
                'button:has-text("Load more")',
                'button:has-text("Show more")',
                '[class*="loadMore"]',
                '[class*="showMore"]'
            ]
            
            for selector in load_more_selectors:
                try:
                    load_more_btn = self.page.locator(selector)
                    if await load_more_btn.count() > 0:
                        await load_more_btn.click()
                        print("Clicked load more button")
                        await self.page.wait_for_timeout(3000)
                        break
                except:
                    continue
            
            # Wait for potential loading
            await self.page.wait_for_timeout(2000)
            
            # Check if new companies were loaded
            final_count = await self.page.locator('a._company_i9oky_355').count()
            new_companies_loaded = final_count > initial_count
            
            if new_companies_loaded:
                print(f"📈 Loaded {final_count - initial_count} more companies ({initial_count} → {final_count})")
            
            return new_companies_loaded
            
        except Exception as e:
            print(f"Error during scrolling: {e}")
            return False

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
                        
                        # Show live display if enabled
                        if self.show_live:
                            name = str(company_data.get('name', 'Unknown') or 'Unknown')[:30]
                            location = str(company_data.get('location', 'N/A') or 'N/A')[:20]
                            tags = ', '.join(str(tag) for tag in (company_data.get('tags', []) or [])[:2])[:30]
                            print(f"📍 Live: {len(companies):3d}. {name} | {location} | {tags}")
                        
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
            js_code = f"""
            () => {{
                const companies = [];
                const showLive = {str(self.show_live).lower()};
                const resultsContainer = document.querySelector('div._section_i9oky_163._results_i9oky_343, [class*="results"], [class*="Results"]');
                
                if (!resultsContainer) {{
                    console.log('Results container not found');
                    return companies;
                }}
                
                const companyLinks = resultsContainer.querySelectorAll('a._company_i9oky_355, a[class*="company"], a[href*="/companies/"]');
                
                companyLinks.forEach((link, index) => {{
                    try {{
                        const company = {{
                            index: index,
                            extraction_method: 'javascript'
                        }};
                        
                        // Extract URL
                        company.url = link.href || link.getAttribute('href');
                        if (company.url && !company.url.startsWith('http')) {{
                            company.url = 'https://www.ycombinator.com' + company.url;
                        }}
                        
                        // Extract name with fallbacks
                        const nameSelectors = [
                            'span._coName_i9oky_470',
                            '.company-name',
                            '[class*="coName"]',
                            'span[class*="Name"]'
                        ];
                        
                        for (const selector of nameSelectors) {{
                            const nameEl = link.querySelector(selector);
                            if (nameEl && nameEl.textContent.trim()) {{
                                company.name = nameEl.textContent.trim();
                                break;
                            }}
                        }}
                        
                        // Extract location with fallbacks
                        const locationSelectors = [
                            'span._coLocation_i9oky_486',
                            '.company-location',
                            '[class*="coLocation"]',
                            'span[class*="Location"]'
                        ];
                        
                        for (const selector of locationSelectors) {{
                            const locationEl = link.querySelector(selector);
                            if (locationEl && locationEl.textContent.trim()) {{
                                company.location = locationEl.textContent.trim();
                                break;
                            }}
                        }}
                        
                        // Extract description with fallbacks
                        const descriptionSelectors = [
                            'span._coDescription_i9oky_495',
                            '.company-description',
                            '[class*="coDescription"]',
                            'span[class*="Description"]'
                        ];
                        
                        for (const selector of descriptionSelectors) {{
                            const descEl = link.querySelector(selector);
                            if (descEl && descEl.textContent.trim()) {{
                                company.description = descEl.textContent.trim();
                                break;
                            }}
                        }}
                        
                        // Extract tags
                        const tagsContainer = link.querySelector('div._pillWrapper_i9oky_33, .pill-wrapper, [class*="pillWrapper"]');
                        company.tags = [];
                        
                        if (tagsContainer) {{
                            const tagLinks = tagsContainer.querySelectorAll('a._tagLink_i9oky_1040, .tag-link, [class*="tagLink"]');
                            tagLinks.forEach(tagLink => {{
                                const tagText = tagLink.textContent.trim();
                                if (tagText) {{
                                    company.tags.push(tagText);
                                }}
                            }});
                        }}
                        
                        // Extract logo
                        const imgEl = link.querySelector('img');
                        company.logo_url = imgEl ? imgEl.src : null;
                        
                        // Only add if we have minimum required data
                        if (company.name || company.url) {{
                            companies.push(company);
                            
                            // Show live display if enabled (every 5th company to avoid spam)
                            if (showLive && companies.length % 5 === 0) {{
                                const name = (company.name || 'Unknown').substring(0, 30);
                                const location = (company.location || 'N/A').substring(0, 20);
                                const tagText = company.tags.slice(0, 2).join(', ').substring(0, 30);
                                console.log(`📍 Live JS: ${{companies.length.toString().padStart(3, ' ')}}. ${{name}} | ${{location}} | ${{tagText}}`);
                            }}
                        }}
                        
                    }} catch (error) {{
                        console.log('Error extracting company', index, error);
                    }}
                }});
                
                return companies;
            }}
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

async def extract_all_companies(page: Page, max_companies: Optional[int] = None, show_live: bool = False) -> List[Dict]:
    """Main function to extract all companies using batch method"""
    extractor = CompanyExtractor(page, show_live)
    
    # Use the new batch extraction method
    companies = await extractor.extract_companies_in_batches(max_companies)
    
    # Clean and validate data
    cleaned_companies = []
    for i, company in enumerate(companies):
        if company.get('name') or company.get('url'):
            # Ensure required fields exist
            company.setdefault('name', 'Unknown')
            company.setdefault('location', '')
            company.setdefault('description', '')
            company.setdefault('tags', [])
            company.setdefault('logo_url', None)
            company.setdefault('url', None)
            
            cleaned_companies.append(company)
            
            # Apply company cap if specified
            if max_companies and len(cleaned_companies) >= max_companies:
                break
    
    print(f"\n🎯 Final result: {len(cleaned_companies)} companies ready for processing")
    return cleaned_companies
