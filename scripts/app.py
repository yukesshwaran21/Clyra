from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Configure OpenAI (you'll need to set your API key)
openai.api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')

# Store conversation history
conversations = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        # Initialize conversation history for new sessions
        if session_id not in conversations:
            conversations[session_id] = []
        
        # Add user message to history
        conversations[session_id].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Prepare messages for OpenAI
        openai_messages = [
            {"role": "system", "content": "You are a helpful and friendly AI assistant. Keep responses concise and engaging."}
        ]
        
        # Add conversation history
        for msg in conversations[session_id][-10:]:  # Last 10 messages
            openai_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=openai_messages,
            max_tokens=150,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        # Add AI response to history
        conversations[session_id].append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({
            "response": ai_response,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
