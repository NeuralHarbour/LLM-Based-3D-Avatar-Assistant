import json

def count_greetings(json_file_path):
    # Load the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Check if 'intent_data' and 'common_examples' keys are present in the JSON
    if 'intent_data' in data and 'common_examples' in data['intent_data']:
        common_examples = data['intent_data']['common_examples']
        greeting_count = sum(1 for example in common_examples if 'intent' in example and example['intent'] == 'fallback')
        return greeting_count
    else:
        print("The 'intent_data' or 'common_examples' key is not present in the JSON file.")
        return 0

# Example usage:
json_file_path = 'intents.json'
greeting_count = count_greetings(json_file_path)

print(f"Number of intents with intent 'fallback': {greeting_count}")
