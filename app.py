### Folder structure:
# chatbot_webapp/
# ├── app.py
# ├── templates/
# │   └── index.html

# ---------- app.py ----------
from flask import Flask, request, jsonify, render_template
from langchain_core.messages import HumanMessage
from langchain_community.chat_models import ChatOllama

app = Flask(__name__)
chat = ChatOllama(model="phi3")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_route():
    user_message = request.json['message']
    response = chat.invoke([HumanMessage(content=user_message)])
    return jsonify({'response': response.content})

if __name__ == '__main__':
    app.run(debug=True)
