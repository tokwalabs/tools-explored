import json
import urllib.request
import urllib.parse

def fetch_json(url):
    """Fetch JSON data from a URL."""
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())

def get_screenshot_url(page_url):
    """Get screenshot URL from Microlink API."""
    MICROLINK_API = "https://api.microlink.io"
    params = {
        'url': page_url,
        'screenshot': 'true',
        'meta': 'false'
    }
    
    api_url = f"{MICROLINK_API}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read())
            return data.get('data', {}).get('screenshot', {}).get('url')
    except Exception as e:
        print(f"Error processing {page_url}: {str(e)}")
        return None

def process_links(input_url):
    """Process all links and add screenshot URLs."""
    # Fetch the original JSON
    data = fetch_json(input_url)
    
    # Process each link
    for item in data.get('links', []):
        if 'url' in item:
            screenshot_url = get_screenshot_url(item['url'])
            if screenshot_url:
                item['screenshot_url'] = screenshot_url
            else:
                print(f"Failed to get screenshot for {item['url']}")
    
    return data

def save_json(data, filename):
    """Save JSON data to a file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    # Replace with your actual GitHub raw URL
    input_url = "YOUR_GITHUB_RAW_URL/tools_explored_without_url.json"
    
    try:
        # Process the links
        processed_data = process_links(input_url)
        
        # Save the results locally
        save_json(processed_data, 'tools_explored_with_url.json')
        print("Processing completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()