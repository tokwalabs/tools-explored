from src.link_processor import LinkProcessor

def main():
    try:
        processor = LinkProcessor()
        processor.process_links(
            'tools_explored_without_url.json',
            'tools_explored_with_url.json'
        )
        print("Processing completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()