from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from datetime import datetime
import json
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI with your API key from environment
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    print("WARNING: OPENAI_API_KEY not found in environment variables!")
    print("Please make sure your .env file contains: OPENAI_API_KEY=your-key-here")

# Store conversation history and user preferences
conversations = {}
user_preferences = {}

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Check if OpenAI API key is configured
        if not openai.api_key:
            return jsonify({
                "error": "OpenAI API key is not configured. Please check your environment variables.",
                "status": "error"
            }), 500

        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        print(f"Received message: {message}")  # Debug logging
        
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
        
        print(f"Sending to OpenAI: {len(openai_messages)} messages")  # Debug logging
        
        # Get response from OpenAI using the newer client format
        try:
            # Try the newer OpenAI client format first
            from openai import OpenAI
            client = OpenAI(api_key=openai.api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=openai_messages,
                max_tokens=200,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content
            
        except ImportError:
            # Fallback to older OpenAI format
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=openai_messages,
                max_tokens=200,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content
        
        print(f"OpenAI response: {ai_response}")  # Debug logging
        
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
        
    except openai.error.AuthenticationError as e:
        print(f"OpenAI Authentication Error: {str(e)}")
        return jsonify({
            "error": "Invalid OpenAI API key. Please check your configuration.",
            "status": "error"
        }), 500
        
    except openai.error.RateLimitError as e:
        print(f"OpenAI Rate Limit Error: {str(e)}")
        return jsonify({
            "error": "Rate limit exceeded. Please try again in a moment.",
            "status": "error"
        }), 500
        
    except openai.error.APIError as e:
        print(f"OpenAI API Error: {str(e)}")
        return jsonify({
            "error": "OpenAI service is temporarily unavailable. Please try again.",
            "status": "error"
        }), 500
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": "I'm experiencing some technical difficulties. Please try again in a moment.",
            "status": "error"
        }), 500

@app.route('/api/conversation/<session_id>', methods=['GET'])
def get_conversation(session_id):
    """Get conversation history for a session"""
    try:
        if session_id in conversations:
            return jsonify({
                "messages": conversations[session_id],
                "status": "success"
            })
        return jsonify({
            "messages": [],
            "status": "success"
        })
    except Exception as e:
        print(f"Error getting conversation: {str(e)}")
        return jsonify({
            "error": "Failed to retrieve conversation",
            "status": "error"
        }), 500

@app.route('/api/clear/<session_id>', methods=['DELETE'])
def clear_conversation(session_id):
    """Clear conversation history for a session"""
    try:
        if session_id in conversations:
            conversations[session_id] = []
        return jsonify({
            "status": "success",
            "message": "Conversation cleared"
        })
    except Exception as e:
        print(f"Error clearing conversation: {str(e)}")
        return jsonify({
            "error": "Failed to clear conversation",
            "status": "error"
        }), 500

@app.route('/api/export/<session_id>', methods=['GET'])
def export_conversation(session_id):
    """Export conversation as JSON"""
    try:
        if session_id in conversations:
            return jsonify({
                "conversation": conversations[session_id],
                "exported_at": datetime.now().isoformat(),
                "status": "success"
            })
        return jsonify({
            "conversation": [],
            "exported_at": datetime.now().isoformat(),
            "status": "success"
        })
    except Exception as e:
        print(f"Error exporting conversation: {str(e)}")
        return jsonify({
            "error": "Failed to export conversation",
            "status": "error"
        }), 500

@app.route('/api/stats/<session_id>', methods=['GET'])
def get_stats(session_id):
    """Get conversation statistics"""
    try:
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
    except Exception as e:
        print(f"Error getting stats: {str(e)}")
        return jsonify({
            "error": "Failed to get statistics",
            "status": "error"
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "openai_configured": bool(openai.api_key)
    })

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"OpenAI API Key configured: {bool(openai.api_key)}")
    app.run(debug=True, port=5000, host='0.0.0.0')
