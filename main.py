import json
import requests


def get_screenshot_url(page_url):
    """Get screenshot URL from Microlink API."""
    MICROLINK_API = "https://api.microlink.io"
    params = {
        'url': page_url,
        'screenshot': 'true',
        'meta': 'false'
    }

    try:
        response = requests.get(MICROLINK_API, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get('data', {}).get('screenshot', {}).get('url')
    except Exception as e:
        print(f"Error processing {page_url}: {str(e)}")
        return None


def load_json(filename):
    """Load JSON data from a file."""
    with open(filename, 'r') as f:
        return json.load(f)


def save_json(data, filename):
    """Save JSON data to a file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def process_links(input_file, output_file):
    """Process all links and add screenshot URLs."""
    try:
        # Load the JSON data
        data = load_json(input_file)

        # Process each link
        for item in data.get('links', []):
            if 'url' in item:
                screenshot_url = get_screenshot_url(item['url'])
                if screenshot_url:
                    item['screenshot_url'] = screenshot_url
                else:
                    print(f"Failed to get screenshot for {item['url']}")

        # Save the processed data
        save_json(data, output_file)
        print("Processing completed successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    process_links('tools_explored_without_screenshot_url.json',
                  'tools_explored_with_screenshot_url.json')
