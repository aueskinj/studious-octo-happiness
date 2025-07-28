from flask import Flask, request, jsonify, render_template
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

app = Flask(__name__)

# Connect to Ollama (ensure it's running locally)
chat = ChatOllama(model="tinyllama", base_url="http://localhost:11434")

@app.route('/')
def index():
    return render_template('index.html')  # Make sure 'index.html' exists in templates/

@app.route('/chat', methods=['POST'])
def chat_route():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        result = chat.invoke([HumanMessage(content=user_message)])
        reply = getattr(result, "content", str(result))  # fallback to string if no .content
        return jsonify({'response': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
