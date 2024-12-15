from .microlink_client import MicrolinkClient
from .json_handler import JsonHandler

class LinkProcessor:
    def __init__(self):
        self.microlink = MicrolinkClient()
        self.json_handler = JsonHandler()

    def process_links(self, input_file, output_file):
        """Process all links and add screenshot URLs."""
        # Load the JSON data
        data = self.json_handler.load_json(input_file)
        
        # Process each link
        for item in data.get('links', []):
            if 'url' in item:
                screenshot_url = self.microlink.get_screenshot_url(item['url'])
                if screenshot_url:
                    item['screenshot_url'] = screenshot_url
                else:
                    print(f"Failed to get screenshot for {item['url']}")
        
        # Save the processed data
        self.json_handler.save_json(data, output_file)