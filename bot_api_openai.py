import discord
import openai
from openai import OpenAI
from discord.ext import commands

intents = discord.Intents.all()
intents.messages = True  # Active l'intention pour les événements de message

# Configuration Discord
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration OpenAI
api_key = 'key openai here'
model_name = 'gpt-3.5-turbo-instruct'

client_GPT = OpenAI(api_key=api_key)

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

@bot.command(name="chatbot")
async def read_message(ctx):
    if ctx.author == bot.user:
        return

    # Préparer la requête pour OpenAI
    response = client_GPT.completions.create(
        model=model_name,
        prompt=ctx.message.content,
        max_tokens=100,  # Limite le nombre de tokens pour la réponse
        temperature=0.2
    )

    # Envoyer la réponse à Discord
    await ctx.channel.send(response.choices[0].text)


# Lancer le bot
bot.run('TOKEN discord bot here')
