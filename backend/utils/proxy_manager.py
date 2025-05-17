import random
import requests

def fetch_proxies(api_url, api_key=None):
    """
    Fetch proxies from an API endpoint.
    
    Args:
        api_url: URL to fetch proxies from
        api_key: Optional API key for authorization
        
    Returns:
        A list of proxy dictionaries
    """
    headers = {}
    if api_key:
        # Webshare specifically uses this header format
        headers['Authorization'] = f'Token {api_key}'
    
    try:
        print(f"Fetching proxies from: {api_url}")
        print(f"Using authorization header: {'Yes' if api_key else 'No'}")
        
        response = requests.get(api_url, headers=headers)
        
        # Print status code for debugging
        print(f"API response status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"API error response: {response.text}")
            
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        data = response.json()
        
        # Extract the proxy results from the JSON response
        if 'results' in data and isinstance(data['results'], list):
            return data['results']
        else:
            # Print the actual response structure for debugging
            print(f"Unexpected API response format: {data.keys()}")
            raise ValueError("Unexpected API response format. Expected 'results' list.")
    
    except requests.RequestException as e:
        print(f"Error fetching proxies: {e}")
        return []


def get_random_proxy(proxies):
    """
    Select a random proxy from the list.
    
    Args:
        proxies: List of proxy dictionaries
        
    Returns:
        A randomly selected proxy dictionary
    """
    if not proxies:
        raise ValueError("No proxies available. Please check your API endpoint.")
    
    return random.choice(proxies)

def parse_proxy(proxy_dict):
    """
    Parse proxy dictionary into Playwright proxy configuration.
    
    Args:
        proxy_dict: Dictionary with proxy details including username, password, 
                   proxy_address, and port
        
    Returns:
        Dictionary with proxy configuration for Playwright
    """
    return {
        "server": f"http://{proxy_dict['proxy_address']}:{proxy_dict['port']}",
        "username": proxy_dict['username'],
        "password": proxy_dict['password'],
    }

def get_proxy_info_string(proxy_dict):
    """
    Get a string representation of proxy for logging (without credentials).
    
    Args:
        proxy_dict: Dictionary with proxy details
        
    Returns:
        String representation of proxy
    """
    return f"{proxy_dict['proxy_address']}:{proxy_dict['port']} ({proxy_dict['country_code']})"

def get_random_user_agent():
    """
    Get a random user agent string.
    
    Returns:
        A randomly selected user agent string
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    ]
    
    return random.choice(user_agents)