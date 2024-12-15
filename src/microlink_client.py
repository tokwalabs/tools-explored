import urllib.request
import urllib.parse
import json

class MicrolinkClient:
    def __init__(self):
        self.API_BASE = "https://api.microlink.io"

    def get_screenshot_url(self, page_url):
        """Get screenshot URL from Microlink API."""
        params = {
            'url': page_url,
            'screenshot': 'true',
            'meta': 'false'
        }
        
        api_url = f"{self.API_BASE}?{urllib.parse.urlencode(params)}"
        
        try:
            with urllib.request.urlopen(api_url) as response:
                data = json.loads(response.read())
                return data.get('data', {}).get('screenshot', {}).get('url')
        except Exception as e:
            print(f"Error processing {page_url}: {str(e)}")
            return None