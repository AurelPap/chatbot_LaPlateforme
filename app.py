from flask import Flask, request, jsonify, render_template
import openai
from openai import OpenAI
import threading
import time

app = Flask(__name__)

# Remplacez 'YOUR_API_KEY' par votre clé API OpenAI
api_key = "YOUR_API_KEY"

client = OpenAI(api_key=api_key)

# Historique des discussions
chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_prompt', methods=['POST'])
def send_prompt():
    data = request.json
    prompt = data.get('prompt')
    if prompt:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=100,
            temperature=0.2
        )
        
        reply = response.choices[0].text.strip()
        
        # Ajouter le prompt et la réponse à l'historique
        chat_history.append({"prompt": prompt, "response": reply})
        
    
        return jsonify(reply)
    return jsonify({"error": "No prompt provided"}), 400

@app.route('/get_history', methods=['GET'])
def get_history():
    return jsonify(chat_history)

if __name__ == '__main__':
    app.run(debug=True)