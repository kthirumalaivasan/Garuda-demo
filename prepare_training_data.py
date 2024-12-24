import json

INPUT_FILE = "combined_data.json"
OUTPUT_FILE = "ollama_training.json"

def prepare_training_data():
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    formatted_data = []
    for intent in data.get("intents", []):
        # Skip intents missing required keys
        user_inputs = intent.get("user_input_variations", [])
        responses = intent.get("responses", [])
        
        if not user_inputs or not responses:
            print(f"Skipping intent due to missing data: {intent.get('intent', 'Unknown Intent')}")
            continue

        for user_input in user_inputs:
            for response in responses:
                formatted_data.append({
                    "prompt": user_input,
                    "completion": response
                })

    with open(OUTPUT_FILE, "w") as output_file:
        json.dump(formatted_data, output_file, indent=4)
    print(f"Training data saved to {OUTPUT_FILE}.")

if __name__ == "__main__":
    prepare_training_data()
