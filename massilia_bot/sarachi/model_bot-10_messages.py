import json
import numpy as np
from tensorflow.keras.models import load_model
import pickle
import random
import nltk
from collections import deque
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# Initialisation du lemmatizer NLTK
lemmatizer = WordNetLemmatizer()

# Téléchargement des stop words (si ce n'est pas déjà fait)
nltk.download('stopwords')
stop_words = set(stopwords.words('french'))

# Chargement du modèle Keras
model = load_model("chatbot_model.keras")

# Chargement des mots et tags à partir des fichiers pickle
words = pickle.load(open("words.pkl", "rb"))
tags = pickle.load(open("tags.pkl", "rb"))

# Chargement des intents à partir du fichier JSON
with open("consolidated_intents.json", "r", encoding="utf-8") as file:
    intents_data = json.load(file)

# File pour stocker les 10 dernières phrases
last_10_messages = deque(maxlen=10)

def clean_up_sentence(sentence):
    """
    Nettoyage et lemmatisation de la phrase d'entrée.
    """
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words if word.lower() not in stop_words]
    return sentence_words

def bow(sentence, words):
    """
    Crée un sac de mots (Bag of Words) pour la phrase d'entrée.
    """
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence, model):
    """
    Prédit l'intention (tag) pour la phrase d'entrée.
    """
    p = bow(sentence, words)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.20
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": tags[r[0]], "probability": str(r[1])})
    return return_list

def get_response(intents_list, intents_data):
    """
    Sélectionne une réponse correspondant au pattern prédit.
    """
    if intents_list:
        tag = intents_list[0]['intent']
        # Recherche de l'intention correspondante dans intents_data
        for intent in intents_data['intents']:
            if intent['tag'] == tag:
                # Retourne la réponse correspondant au pattern prédit
                return random.choice(intent['responses'])
    return "Je ne comprends pas bien votre question."

def chatbot_main():
    print("Bonjour, je m'appelle Massalia, comment puis-je vous aider?")
    while True:
        message = input("You: ")
        if message.lower() == "quit":
            print("Au revoir !")
            return
        last_10_messages.append(message)  # Ajoute la nouvelle phrase à la file
        intents = predict_class(message, model)
        response = get_response(intents, intents_data)
        print("Bot:", response)

def main():
    while True:
        chatbot_main()
        restart = input("Voulez-vous quitter le chatbot ? (oui/non): ")
        if restart.lower() != "non":
            break
    print("Merci d'avoir utilisé notre chatbot !")

if __name__ == "__main__":
    main()
