import json

class JsonHandler:
    @staticmethod
    def load_json(filename):
        """Load JSON data from a file."""
        with open(filename, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_json(data, filename):
        """Save JSON data to a file."""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)