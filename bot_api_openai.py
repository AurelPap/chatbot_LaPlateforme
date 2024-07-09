import discord
import openai
from openai import OpenAI
from discord.ext import commands
from flask import jsonify, request

intents = discord.Intents.all()
intents.messages = True  # Active l'intention pour les événements de message

# Configuration Discord
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration OpenAI
api_key = 'your key'
model_name = 'gpt-3.5-turbo-instruct'

client_GPT = OpenAI(api_key=api_key)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

chat_history = []
MAX_HISTORY = 5  # Limite du nombre d'échanges dans l'historique

@bot.command(name="chatbot")
async def read_message(ctx):
    if ctx.author == bot.user:
        return

    # Extraire le message de l'utilisateur
    prompt = ctx.message.content.replace("!chatbot", "", 1).strip()
    if prompt:
        # Limiter l'historique des échanges
        limited_history = chat_history[-MAX_HISTORY:]

        # Construire le contexte en ajoutant l'historique des échanges
        context = ""
        for entry in limited_history:
            context += f"Vous: {entry['prompt']}\nGPT-3: {entry['response']}\n"
        context += f"Vous: {prompt}\nGPT-3:"

        # Préparer la requête pour OpenAI
        try:
            response = client_GPT.completions.create(
                model=model_name,
                prompt=context,
                max_tokens=100,  # Limite le nombre de tokens pour la réponse
                temperature=0.2
            )
            response_text = response.choices[0].text.strip()
        except Exception as e:
            response_text = f"Erreur lors de la génération de la réponse: {e}"

        # Envoyer la réponse à Discord
        await ctx.channel.send(response_text)

        # Ajouter le prompt et la réponse à l'historique
        chat_history.append({
            'prompt': prompt,
            'response': response_text
        })

        # Limiter la taille de l'historique pour éviter des réponses trop longues
        if len(chat_history) > MAX_HISTORY:
            chat_history.pop(0)


# Lancer le bot
bot.run('your key')
