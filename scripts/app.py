from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

try:
    import typing_extensions
    from packaging import version
    if version.parse(getattr(typing_extensions, "__version__", "0.0.0")) < version.parse("4.0.0"):
        print("ERROR: Your typing_extensions package is too old for the current OpenAI library.")
        print("Please run: pip install --upgrade typing_extensions")
        sys.exit(1)
except ImportError:
    print("ERROR: typing_extensions or packaging is not installed.")
    print("Please run: pip install typing_extensions packaging")
    sys.exit(1)

import openai
import os
from datetime import datetime
import json
import uuid
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    print("WARNING: OPENAI_API_KEY not found in environment variables!")
    print("Please make sure your .env file contains: OPENAI_API_KEY=your-key-here")

conversations = {}
user_preferences = {}

try:
    from openai import AuthenticationError, RateLimitError, APIError
except ImportError:
    AuthenticationError = RateLimitError = APIError = Exception

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if not openai.api_key:
            return jsonify({
                "error": "OpenAI API key is not configured. Please check your environment variables.",
                "status": "error"
            }), 500

        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        print(f"Received message: {message}")  # Debug logging
        
        if session_id not in conversations:
            conversations[session_id] = []
        
        user_message = {
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat(),
            "id": str(uuid.uuid4())
        }
        conversations[session_id].append(user_message)
        
        openai_messages = [
            {"role": "system", "content": "You are a helpful, professional, and friendly AI assistant. Provide clear, concise, and engaging responses. Use emojis occasionally to make conversations more pleasant."}
        ]
        
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
        
    except AuthenticationError as e:
        print(f"OpenAI Authentication Error: {str(e)}")
        return jsonify({
            "error": "Invalid OpenAI API key. Please check your configuration.",
            "details": str(e),
            "status": "error"
        }), 500
        
    except RateLimitError as e:
        print(f"OpenAI Rate Limit Error: {str(e)}")
        return jsonify({
            "error": "Rate limit exceeded. Please try again in a moment.",
            "details": str(e),
            "status": "error"
        }), 500
        
    except APIError as e:
        print(f"OpenAI API Error: {str(e)}")
        return jsonify({
            "error": "OpenAI service is temporarily unavailable. Please try again.",
            "details": str(e),
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
