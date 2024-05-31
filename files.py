import json

def save_string_as_json(string_data, file_name):
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(string_data, file)
        print(f"String data saved successfully to {file_name}")
        print("You have connected to the salesman: \n")
    except Exception as e:
        print(f"Error saving string data to {file_name}: {e}")


def load_json_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading data from {file_name}: {e}")
        return None