import random
import requests

                             

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