import json
import requests
import os
from PIL import Image
import io
import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode

# proxy = 'http://<user>:<pass>@<proxy>:<port>'
# proxy_ip = ''
# proxy_port = ''
# proxy = f'https://{proxy_ip}:{proxy_port}'

# os.environ['http_proxy'] = proxy
# os.environ['HTTP_PROXY'] = proxy
# os.environ['https_proxy'] = proxy
# os.environ['HTTPS_PROXY'] = proxy
# proxies = {
#     "http": proxy,
# }

# proxy_test_url = 'https://api.ipify.org'

# try:
#     response = requests.get(proxy_test_url, proxies=proxies, verify=False)
#     print(f'response {response}')
#     print(f'response.text {response.text}')
#     assert response.text == proxy_ip
# except Exception as e:
#     print(f'Error: {e}')
#     print('Proxy does not work')


async def capture_and_save_screenshot_without_api(url: str, output_path: str):
    async with AsyncWebCrawler(verbose=True) as crawler:
        try:
            result = await crawler.arun(
                url=url,
                screenshot=True,
                simulate_user=True,
                scan_full_page=False,
                # adjust_viewport_to_content=True,
                cache_mode=CacheMode.BYPASS
            )

            if result.success and result.screenshot:
                import base64
                screenshot_data = base64.b64decode(result.screenshot)

                # Create an image from the screenshot data
                image = Image.open(io.BytesIO(screenshot_data))

                # Crop the image (adjust these values as needed)
                width, height = 1920, 1080
                cropped_image = image.crop((0, 0, width, height))

                # Create the screenshots directory if it doesn't exist
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Save the cropped image
                cropped_image.save(output_path)

                # with open(output_path, 'wb') as f:
                #     f.write(screenshot_data)
                print(f"Screenshot saved successfully to {output_path}")
                return output_path
            else:
                print("Failed to capture screenshot")
        except Exception as e:
            print(e)


def get_screenshot_url_with_api(page_url):
    """Get screenshot URL from Microlink API."""
    MICROLINK_API = "https://api.microlink.io"
    params = {
        'url': page_url,
        'screenshot': 'true',
        'meta': 'false',
        'ttl': '3days',
    }

    try:
        response = requests.get(MICROLINK_API, params=params, verify=False)
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


async def process_links(input_file, output_file):
    """Process all links and add screenshot URLs."""
    try:
        # Load the JSON data
        data = load_json(input_file)

        # Process each link
        for index, item in enumerate(data.get('links', [])):
            print(f'index: {index}')
            if 'url' in item:
                screenshot_url = get_screenshot_url_with_api(item['url'])
                if screenshot_url:
                    item['screenshot_url'] = screenshot_url
                else:
                    print(
                        f"Failed to get screenshot for {item['url']}. Trying to capture locally...")

                    # trying to capture screenshot locally
                    screenshot_url = await capture_and_save_screenshot_without_api(
                        item['url'], f"screenshots/{item['label']}.png")

                    repo_host = 'https://raw.githubusercontent.com/tokwalabs/tools-explored/refs/heads/main'
                    item['screenshot_url'] = f'{repo_host}/{screenshot_url}'

        # Save the processed data
        save_json(data, output_file)
        print("Processing completed successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    import asyncio
    asyncio.run(process_links('tools_explored_without_screenshot_url.json',
                              'tools_explored_with_screenshot_url.json'))
