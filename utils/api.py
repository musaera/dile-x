import json

def fetch_drone_data():
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
            return data
    except Exception as e:
        print(f"Error fetching drone data: {e}")
        return []
