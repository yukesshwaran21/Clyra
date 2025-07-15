from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from datetime import datetime
import json
import uuid

app = Flask(__name__)
CORS(app)

# Configure OpenAI with your API key
openai.api_key = "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"

# Store conversation history and user preferences
conversations = {}
user_preferences = {}

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
        user_message = {
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "id": str(uuid.uuid4())
        }
        conversations[session_id].append(user_message)
        
        # Prepare messages for OpenAI
        openai_messages = [
            {"role": "system", "content": "You are a helpful, professional, and friendly AI assistant. Provide clear, concise, and engaging responses. Use emojis occasionally to make conversations more pleasant."}
        ]
        
        # Add conversation history (last 10 messages for context)
        for msg in conversations[session_id][-10:]:
            openai_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=openai_messages,
            max_tokens=200,
            temperature=0.7,
            presence_penalty=0.1,
            frequency_penalty=0.1
        )
        
        ai_response = response.choices[0].message.content
        
        # Add AI response to history
        bot_message = {
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().isoformat(),
            "id": str(uuid.uuid4())
        }
        conversations[session_id].append(bot_message)
        
        return jsonify({
            "response": ai_response,
            "message_id": bot_message["id"],
            "status": "success",
            "timestamp": bot_message["timestamp"]
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            "error": "I'm experiencing some technical difficulties. Please try again in a moment.",
            "status": "error"
        }), 500

@app.route('/api/conversation/<session_id>', methods=['GET'])
def get_conversation(session_id):
    """Get conversation history for a session"""
    if session_id in conversations:
        return jsonify({
            "messages": conversations[session_id],
            "status": "success"
        })
    return jsonify({
        "messages": [],
        "status": "success"
    })

@app.route('/api/clear/<session_id>', methods=['DELETE'])
def clear_conversation(session_id):
    """Clear conversation history for a session"""
    if session_id in conversations:
        conversations[session_id] = []
    return jsonify({
        "status": "success",
        "message": "Conversation cleared"
    })

@app.route('/api/export/<session_id>', methods=['GET'])
def export_conversation(session_id):
    """Export conversation as JSON"""
    if session_id in conversations:
        return jsonify({
            "conversation": conversations[session_id],
            "exported_at": datetime.now().isoformat(),
            "status": "success"
        })
    return jsonify({
        "conversation": [],
        "status": "success"
    })

@app.route('/api/stats/<session_id>', methods=['GET'])
def get_stats(session_id):
    """Get conversation statistics"""
    if session_id in conversations:
        messages = conversations[session_id]
        user_messages = [m for m in messages if m["role"] == "user"]
        bot_messages = [m for m in messages if m["role"] == "assistant"]
        
        return jsonify({
            "total_messages": len(messages),
            "user_messages": len(user_messages),
            "bot_messages": len(bot_messages),
            "conversation_started": messages[0]["timestamp"] if messages else None,
            "last_activity": messages[-1]["timestamp"] if messages else None,
            "status": "success"
        })
    
    return jsonify({
        "total_messages": 0,
        "user_messages": 0,
        "bot_messages": 0,
        "status": "success"
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
