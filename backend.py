from flask import Flask, request, jsonify
import requests

# Initialize Flask app
app = Flask(__name__)

# Hugging Face API key and model
api_key = "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"
model = "mistralai/Mistral-Nemo-Instruct-2407"
api_url = f"https://api-inference.huggingface.co/models/{model}"

# Set up headers with your API key
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Function to interact with the Hugging Face model
def chat_with_ai(user_input):
    formatted_input = f"You are an AI named 'chat helper.' Your mission is to help people with things They will provide input, and you should respond thoughtfully and supportively. Always answer what they ask and avoid saying mean things.\nUser: {user_input}\nAI:"
    
    payload = {
        "inputs": formatted_input
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            ai_response = result[0].get("generated_text", "").strip() if isinstance(result[0], dict) else ""
            # Remove the instruction part from the response
            response_start = formatted_input.rfind("AI:") + len("AI:")
            return ai_response[response_start:].strip()
        else:
            return "Error: Unexpected response format."
    else:
        return f"Error: {response.status_code} - {response.text}"

# Define the POST endpoint to interact with the chatbot
@app.route('/chat', methods=['POST'])
def chat():
    # Get user input from the JSON request body
    user_input = request.json.get('user_input')
    
    if user_input:
        # Get the AI response by calling the chat_with_ai function
        ai_response = chat_with_ai(user_input)
        return jsonify({"response": ai_response})
    else:
        return jsonify({"error": "No input provided"}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
