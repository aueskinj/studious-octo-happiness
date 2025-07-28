from flask import Flask, request, jsonify, render_template
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

app = Flask(__name__)

# Fix: Use localhost since Ollama is running locally
chat = ChatOllama(
    model="tinyllama", 
    base_url="http://localhost:11434"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_route():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        # Debug: Print the message being sent
        print(f"Sending message: {user_message}")
        
        result = chat.invoke([HumanMessage(content=user_message)])
        
        # Debug: Print the raw result
        print(f"Raw result: {result}")
        print(f"Result type: {type(result)}")
        
        # Extract content properly
        if hasattr(result, 'content'):
            reply = result.content
        elif hasattr(result, 'text'):
            reply = result.text
        else:
            reply = str(result)
            
        # Debug: Print the extracted reply
        print(f"Extracted reply: {reply}")
        
        return jsonify({'response': reply})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Chat error: {str(e)}'}), 500

@app.route('/test', methods=['GET'])
def test_connection():
    """Test endpoint to check if Ollama connection works"""
    try:
        result = chat.invoke([HumanMessage(content="Hello, can you hear me?")])
        return jsonify({
            'status': 'success',
            'result_type': str(type(result)),
            'has_content': hasattr(result, 'content'),
            'content': getattr(result, 'content', str(result))
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)