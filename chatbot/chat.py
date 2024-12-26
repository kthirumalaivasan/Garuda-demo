import os
import json
from fuzzywuzzy import fuzz
from autocorrect import Speller
import subprocess
import random
from database.db import collection1
from database.db import collection2


# Configuration
MODEL_NAME = "iqtech"  # Your custom model
TRAINING_DATA_FILE = "../datasets/ollama_training.json"  # Full path to the training file
ADMIN_PASSWORD = "admin123"  # Admin password to update data (change to your own)
ADMIN_REVIEW_FILE = "admin_review_queries.json"  # File to store queries for admin review
UNRELEVANT_FILE = "unrelevant.json"  # File to store irrelevant queries

# Initialize the spell checker
spell = Speller()

# Load training data
def load_training_data():
    try:
        with open(TRAINING_DATA_FILE, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return []

# Save training data (admin must manually copy and update)
def save_training_data(training_data):
    try:
        with open(TRAINING_DATA_FILE, 'w') as f:
            json.dump(training_data, f, indent=4)
    except Exception as e:
        print(f"Failed to save training data: {e}")

# Correct spelling mistakes
def correct_spelling(user_input):
    return spell(user_input)

# Find the best match
def find_best_match(user_input, training_data):
    user_input = correct_spelling(user_input.lower())  # Correct spelling first
    best_match = None
    highest_similarity = 0.0

    for entry in training_data:
        prompt_lower = entry["prompt"].lower()
        similarity = fuzz.token_sort_ratio(user_input, prompt_lower)  # Fuzzy matching
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = entry["completion"]

    if highest_similarity > 80:  # Increased threshold for matching
        return best_match

    return None

# Check if the input is a greeting
def is_greeting(user_input):
    greetings = [
        "hi", "hello", "hai", "hey", "halo", "greetings", "good morning", "good evening", "howdy",
        "heyy", "helo", "hii", "hye", "helloo", "good day", "gud morning", "gud evning", "hellow"
    ]
    return any(greet in user_input.lower() for greet in greetings)

# Check if the input is a casual expression
def is_casual_expression(user_input):
    casual_expressions = [
        "thank you", "thanks", "yeah", "yup", "yes", "no", "nope", "lol", "okay", "ok", "great", "good", "awesome",
        "haha", "hee", "hahaha", "lolol", "hehee"
    ]
    return any(exp in user_input.lower() for exp in casual_expressions)

# Check if the query is related to Garuda Aerospace
def is_relevant_query(user_input):
    keywords = [
        "garuda", "aerospace", "drone", "agnishwar", "training", "services", "products", "flagship",
        "cofounder", "founder", "ceo", "company", "about", "contact", "rithika", "projects", 
        "customer", "client", "partner", "team", "leadership", "mission", "vision", "values",
        "history", "profile", "awards", "uav", "ai", "robotics", "automation", "innovation",
        "engineering", "manufacturing", "research", "development", "software", "hardware",
        "aerodynamics", "sensors", "imaging", "analytics", "agriculture", "mapping", 
        "surveillance", "delivery", "inspection", "photography", "videography", "aerial", 
        "maintenance", "environment", "energy", "construction", "mining", "rescue", "disaster", 
        "commercial", "industrial", "defense", "price", "cost", "features", "specifications", 
        "availability", "purchase", "order", "warranty", "support", "repair", "troubleshooting", 
        "demo", "workshop", "webinar", "schedule", "location", "office", "email", "phone", 
        "address", "careers", "jobs", "hiring", "internships", "feedback", "reviews", "complaints",
        "faqs", "help", "assistance", "problem", "issue", "query", "account", "billing", "invoice", 
        "payment", "refund", "subscription", "government", "contract", "tender", "collaboration",
        "proposal", "deployment", "case study", "portfolio", "sustainability", "study", "initiative",
        "website", "more details", "info", "contact us", "email", "phone", "call", "helpdesk",
        "support team", "contact information", "inquiry", "further assistance", "reach us", "customer service","global shipping"
    ]
    return any(keyword in user_input.lower() for keyword in keywords)

# Log queries for admin review
def log_for_admin_review(query):
    try:
        review_data = {
            "prompt": query,
            "completion": ""
        }
        collection1.insert_one(review_data)
        print("Query logged successfully.")
    except Exception as e:
        print(f"Failed to log query for review: {e}")

# Log irrelevant queries
def log_irrelevant_query(query):
    try:
        review_data = {
            "prompt": query,
            "completion": ""
        }
        # Insert the data into the MongoDB collection
        collection2.insert_one(review_data)
        print("Query logged successfully.")
    except Exception as e:
        print(f"Failed to log irrelevant query: {e}")

# Append to the main training data file after admin review
def append_to_main_dataset(prompt, completion):
    try:
        training_data = load_training_data()
        training_data.append({
            "prompt": prompt,
            "completion": completion
        })
        save_training_data(training_data)
    except Exception as e:
        print(f"Failed to append to main dataset: {e}")

# Run custom model using subprocess
def run_custom_model(query):
    try:
        result = subprocess.run(
            ['ollama', 'run', MODEL_NAME, query],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.encode('utf-8').decode('utf-8').strip()
        else:
            return f"Error occurred: {result.stderr.encode('utf-8').decode('utf-8').strip()}"
    except subprocess.TimeoutExpired:
        return "I'm sorry, the response took too long. Please try rephrasing your question."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Chat function
def chat(user_input, is_admin=False):
    training_data = load_training_data()

    # Correct the user input spelling
    user_input_corrected = correct_spelling(user_input)

    # Handling greetings
    if is_greeting(user_input_corrected):
        greetings_responses = [
            "Hi there! 👋 I'm Garuda Bot, developed by IQ TechMax. How can I assist you today? 😊",
            "Hey! How's it going? 😎 I'm Garuda Bot, here to help you! 👍",
            "Hello! Welcome to Garuda Aerospace! How may I help you? 😊"
        ]
        return random.choice(greetings_responses)
    
    # Handle casual expressions like thank you, yes/no, haha, etc.
    elif is_casual_expression(user_input_corrected):
        casual_responses = [
            "You're welcome! 😄", "No worries! 👍", "Lol, I got you! 😆", "Yep, that's correct! ✅", 
            "Sure thing! 😃", "Great! 🙌", "Got it, thanks! 👏", "No problem! 😎", "Yup, no issue! 🤗",
            "Haha! 😂", "Hehe! 😏", "Hahaha, you're funny! 😂", "Heehee! 😆"
        ]
        return random.choice(casual_responses)
    
    # Try to find the best match in the training data for relevant queries
    response = find_best_match(user_input_corrected, training_data)
    
    if response:
        # Return the best match response if found
        return response
    
    # If no match is found, check if the query is still relevant to the training context
    if is_relevant_query(user_input_corrected):
        if is_admin:
            completion = input(f"Admin: Please provide a completion for this query '{user_input_corrected}': ")
            if completion:
                # Append completion to the main dataset
                append_to_main_dataset(user_input_corrected, completion)
                print(f"Response updated successfully! Query: '{user_input_corrected}', Completion: '{completion}'")
                return completion
            else:
                print("Completion not provided. Try again later.")
                return "Completion not provided. Try again later."
        else:
            # Log query to admin review file
            log_for_admin_review(user_input_corrected)
            return "Sorry, I am currently under training. 😅 Let me pass this question to the admin for review. 📝"
    else:
        # Log irrelevant query
        log_irrelevant_query(user_input_corrected)
        # If query is not relevant, respond with a generic message
        return "Sorry, I can only respond to Garuda Aerospace-related queries. 🙇‍♂️"

