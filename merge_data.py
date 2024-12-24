import os
import json

DATASET_DIR = "./datasets"
OUTPUT_FILE = "combined_data.json"

def merge_datasets():
    combined_data = {"intents": []}
    for file_name in os.listdir(DATASET_DIR):
        if file_name.endswith(".json"):
            file_path = os.path.join(DATASET_DIR, file_name)
            with open(file_path, "r") as f:
                data = json.load(f)
                combined_data["intents"].extend(data.get("intents", []))
    with open(OUTPUT_FILE, "w") as output_file:
        json.dump(combined_data, output_file, indent=4)
    print(f"Datasets merged into {OUTPUT_FILE}.")

if __name__ == "__main__":
    merge_datasets()
