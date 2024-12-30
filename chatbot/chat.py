import os
import json
from fuzzywuzzy import fuzz
import random
from sentence_transformers import SentenceTransformer, util
from database.db import collection1
from database.db import collection2
import subprocess
from utils.logger import logger

# Configuration
MODEL_NAME = "iqtech"  # Your custom model
TRAINING_DATA_FILE = "../datasets/ollama_training.json"  # Full path to the training file
ADMIN_PASSWORD = "admin123"  # Admin password to update data (change to your own)
ADMIN_REVIEW_FILE = "admin_review_queries.json"  # File to store queries for admin review
UNRELEVANT_FILE = "unrelevant.json"  # File to store irrelevant queries

# Initialize SentenceTransformer model for semantic similarity
semantic_model = SentenceTransformer('all-MiniLM-L6-v2')

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
        logger.error("Failed to save training data: {e}")

# Find the best match
def find_best_match_fuzzy(user_input, training_data):
    # user_input = correct_spelling(user_input.lower())  # Correct spelling first
    best_match = None
    highest_similarity = 0.0

    for entry in training_data:
        prompt_lower = entry["prompt"].lower()
        similarity = fuzz.token_sort_ratio(user_input.lower(), prompt_lower)  # Fuzzy matching
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = entry["completion"]

    if highest_similarity > 80:  # Increased threshold for matching
        return best_match

    return None

# Find the best match using semantic similarity
def find_best_match_semantic(user_input, training_data):
    user_embedding = semantic_model.encode(user_input)
    highest_similarity = 0.0
    best_match = None

    for entry in training_data:
        prompt_embedding = semantic_model.encode(entry["prompt"])
        similarity = util.cos_sim(user_embedding, prompt_embedding).item()

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = entry["completion"]

    if highest_similarity > 0.7:  # Threshold for semantic similarity
        return best_match

    return None

# Check if the input is a greeting
def is_greeting(user_input):
    greetings = [
        "hi", "hello", "hai", "hey", "halo", "greetings", "good morning", "good evening", "howdy",
        "heyy", "helo", "hii", "hye", "helloo", "good day", "gud morning", "gud evning", "hellow"
    ]
    return any(greet in user_input.lower() for greet in greetings) and len(user_input.split()) <= 2

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
        logger.info("Query logged successfully.")
    except Exception as e:
        logger.error("Failed to log query for review: {e}")

# Log irrelevant queries
def log_irrelevant_query(query):
    try:
        review_data = {
            "prompt": query,
            "completion": ""
        }
        collection2.insert_one(review_data)
        logger.info("Query logged successfully.")
    except Exception as e:
        logger.error("Failed to log irrelevant query: {e}")

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
        logger.error("Failed to append to main dataset: {e}")

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
        return logger.error("An error occurred: {e}")

# Chat function
def chat(user_input, is_admin=False):
    training_data = load_training_data()

    # Correct the user input spelling
    # user_input_corrected = correct_spelling(user_input)

    # Handling greetings
    if is_greeting(user_input):
        greetings_responses = [
            "Hi there! I'm Garuda Bot, developed by IQ TechMax. How can I assist you today?",
            "Hey! How's it going? I'm Garuda Bot, here to help you!",
            "Hello! Welcome to Garuda Aerospace! How may I help you?"
        ]
        return random.choice(greetings_responses)
    
    # Try to find the best match using fuzzy matching
    response = find_best_match_fuzzy(user_input, training_data)
    
    if response:
        return response
    
    # If no match found, try semantic similarity
    response = find_best_match_semantic(user_input, training_data)
    
    if response:
        return response
    
    # If no match found, check if the query is relevant and handle it for admin review
    if is_relevant_query(user_input):
        if is_admin:
            completion = input(f"Admin: Please provide a completion for this query '{user_input}': ")
            if completion:
                append_to_main_dataset(user_input, completion)
                return completion
            else:
                return "Completion not provided. Try again later."
        else:
            log_for_admin_review(user_input)
            return "Sorry, I am currently under training. Let me pass this question to the admin for review."
    else:
        log_irrelevant_query(user_input)
        return "Sorry, I can only respond to Garuda Aerospace-related queries."
