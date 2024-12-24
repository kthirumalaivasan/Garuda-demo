# import os
# import json

# # File paths
# MODEL_CONFIG_FILE = "iqtechmodel.txt"
# TRAINING_DATA_FILE = "../ollama_training.json"

# # Function to read the model configuration from iqtechmodel.txt
# def load_model_config():
#     config = {}
#     try:
#         with open(MODEL_CONFIG_FILE, 'r') as file:
#             for line in file:
#                 if line.strip() and not line.startswith('#'):  # Ignore comments and empty lines
#                     key, value = line.split(":", 1)
#                     config[key.strip()] = value.strip()
#     except FileNotFoundError:
#         raise FileNotFoundError(f"Configuration file not found: {MODEL_CONFIG_FILE}")
#     return config

# # Function to load training data
# def load_training_data():
#     if not os.path.exists(TRAINING_DATA_FILE):
#         raise FileNotFoundError(f"Training data file not found: {TRAINING_DATA_FILE}")
#     try:
#         with open(TRAINING_DATA_FILE, 'r') as file:
#             data = json.load(file)
#             return data
#     except json.JSONDecodeError as e:
#         raise ValueError(f"Error decoding JSON from training data file: {e}")

# # Function to simulate training
# def train_model(config, training_data):
#     model_name = config.get('Model Name', 'default_model')
#     epochs = int(config.get('Training Epochs', 10))
#     batch_size = int(config.get('Batch Size', 32))
#     learning_rate = float(config.get('Learning Rate', 0.001))
#     optimizer = config.get('Optimizer', 'Adam')

#     print(f"Training model: {model_name}")
#     print(f"Using configuration:")
#     print(f"  - Epochs: {epochs}")
#     print(f"  - Batch Size: {batch_size}")
#     print(f"  - Learning Rate: {learning_rate}")
#     print(f"  - Optimizer: {optimizer}")
#     print(f"Training data loaded: {len(training_data)} entries")

#     # Placeholder for actual model training logic
#     for epoch in range(1, epochs + 1):
#         print(f"Epoch {epoch}/{epochs}: Training...")
#         # Simulate training process
#     print(f"Training complete for model: {model_name}")

# # Main function
# def main():
#     try:
#         config = load_model_config()
#         training_data = load_training_data()
#         train_model(config, training_data)
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     main()

# import streamlit as st
# from chat import load_training_data, save_training_data, find_best_match, correct_spelling, is_greeting, is_relevant_query, run_custom_model
# from fuzzywuzzy import fuzz
# import subprocess
# import json

# # Initialize session state
# if 'training_data' not in st.session_state:
#     st.session_state.training_data = load_training_data()

# # Function to handle the chat process
# def handle_chat(user_input):
#     # Correct spelling
#     user_input_corrected = correct_spelling(user_input)

#     # Handle greetings
#     if is_greeting(user_input_corrected):
#         return "Hi, I am Garuda Bot developed by IQ TechMax. How can I assist you today?"

#     # Handle relevant queries related to Garuda Aerospace
#     elif is_relevant_query(user_input_corrected):
#         response = find_best_match(user_input_corrected, st.session_state.training_data)
#         if response:
#             return response
#         else:
#             # Relevant query but no answer found in training data
#             return "Sorry, I am currently under training. Let me pass this question to the admin for review."
    
#     # If no relevant queries found
#     else:
#         return "Sorry, I can only respond to Garuda Aerospace-related queries."

# # Function to save the new training data
# def save_new_data(user_input, admin_response):
#     new_entry = {
#         "prompt": user_input,
#         "completion": admin_response
#     }
#     st.session_state.training_data.append(new_entry)
#     save_training_data(st.session_state.training_data)
#     return "Thanks! I've saved the new question and answer to my knowledge base."

# # Streamlit App UI
# def chat_interface():
#     st.title("Garuda Aerospace Chatbot")
    
#     # User input form
#     user_input = st.text_input("You: ", "")
    
#     if user_input:
#         # Process the user input
#         bot_response = handle_chat(user_input)
        
#         # Display bot response
#         st.write(f"Bot: {bot_response}")
        
#         if bot_response == "Sorry, I am currently under training. Let me pass this question to the admin for review.":
#             # Admin review form
#             admin_response = st.text_area(f"Admin: Provide an answer for '{user_input}' or type 'skip' to ignore", "")
#             if admin_response and admin_response.lower() != "skip":
#                 # Save new training data if admin provides a response
#                 st.write(save_new_data(user_input, admin_response))
#             elif admin_response.lower() == "skip":
#                 st.write("Bot: Skipping this query. It won't be saved.")

# if __name__ == "__main__":
#     chat_interface()


##############S
from chat import load_training_data, save_training_data, find_best_match, correct_spelling, is_greeting, is_relevant_query, run_custom_model
from fuzzywuzzy import fuzz
import json

# Load training data
def load_training_data_from_file():
    return load_training_data()

# Function to handle the chat process
def handle_chat(user_input, training_data):
    # Correct spelling
    user_input_corrected = correct_spelling(user_input)

    # Handle greetings
    if is_greeting(user_input_corrected):
        return "Hi, I am Garuda Bot developed by IQ TechMax. How can I assist you today?"

    # Handle relevant queries related to Garuda Aerospace
    elif is_relevant_query(user_input_corrected):
        response = find_best_match(user_input_corrected, training_data)
        if response:
            return response
        else:
            # Relevant query but no answer found in training data
            return "Sorry, I am currently under training. Let me pass this question to the admin for review."
    
    # If no relevant queries found
    else:
        return "Sorry, I can only respond to Garuda Aerospace-related queries."

# Function to save the new training data
def save_new_data(user_input, admin_response, training_data):
    new_entry = {
        "prompt": user_input,
        "completion": admin_response
    }
    training_data.append(new_entry)
    save_training_data(training_data)
    return "Thanks! I've saved the new question and answer to my knowledge base."

# Main function to run the chatbot training process
def train_chatbot():
    # Load training data
    training_data = load_training_data_from_file()
    
    print("Garuda Aerospace Chatbot - Training Mode")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        # Process the user input
        bot_response = handle_chat(user_input, training_data)
        
        # Display bot response
        print(f"Bot: {bot_response}")
        
        if bot_response == "Sorry, I am currently under training. Let me pass this question to the admin for review.":
            # Admin review form (console-based)
            admin_response = input(f"Admin: Provide an answer for '{user_input}' or type 'skip' to ignore: ")
            if admin_response and admin_response.lower() != "skip":
                # Save new training data if admin provides a response
                print(save_new_data(user_input, admin_response, training_data))
            elif admin_response.lower() == "skip":
                print("Bot: Skipping this query. It won't be saved.")
                
if __name__ == "__main__":
    train_chatbot()
