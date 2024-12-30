from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chat import chat  # Import the chat function from chat.py
from utils.logger import logger

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Route for main page
@app.route('/')
def index():
    return render_template('index.html')  # Ensure to place your HTML in a templates folder

# Route for handling user messages
@app.route('/chat', methods=['POST'])
def chat_route():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Call the chat function to handle user input and return response
    bot_response = chat(user_message)
    
    return jsonify({"response": bot_response})

logger.info("Garuda Demo bot started successfully")
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
