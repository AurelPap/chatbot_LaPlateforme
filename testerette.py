import discord
import openai
from openai import OpenAI
from discord.ext import commands
# from flask import jsonify, request
import asyncio

intents = discord.Intents.all()
intents.messages = True  # Active l'intention pour les événements de message

# Configuration Discord
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration OpenAI
api_key = 'TOKEN HERE'
model_name = 'gpt-3.5-turbo-instruct'

client_GPT = OpenAI(api_key=api_key)

# Variables

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

@bot.event
async def on_member_join(member):
    # Check if the member already has roles
    if len(member.roles) > 1:  # Member has roles other than @everyone
        return  # Exit without assigning roles

    # Assign roles to new members upon joining
    visitor_role = discord.utils.get(member.guild.roles, name="Visitor")

    if visitor_role:
        await member.add_roles(visitor_role)
        await member.send(f"Welcome to the server! You have been assigned the 'Visitor' role.")


# Command: Give role
@bot.command(name="giverole")
async def give_role(ctx, member: discord.Member, role_name: str):
    if ctx.author == bot.user:
        return

    # Ensure the command issuer has the 'Staff' role
    if "Staff" in [role.name for role in ctx.author.roles]:
        # Find the role in the guild
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await member.add_roles(role)
            await ctx.send(f"{member.mention} has been given the '{role_name}' role!")
        else:
            await ctx.send(f"Role '{role_name}' not found.")
    else:
        await ctx.send("You don't have permission to use this command.")


@bot.command(name="getroles")
async def get_roles(ctx):
    roles = [role.name for role in ctx.author.roles if role.name != "@everyone"]
    if roles:
        await ctx.send(f"Your roles are: {', '.join(roles)}")
    else:
        await ctx.send("You don't have any roles.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided."):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban members.")
    except discord.HTTPException:
        await ctx.send("Banning the member failed.")


user_channels = {}
@bot.command(name="getroom")
async def get_room(ctx, *members: discord.Member):
    global user_channels  # Declare user_channels as global
    # Create a private text channel
    guild = ctx.guild

    # Check if user already has a channel
    if ctx.author.id in user_channels:
        await ctx.send(f'You already have a private channel: {user_channels[ctx.author.id]}')
        return

    # overwrites = {
    #     guild.default_role: discord.PermissionOverwrite(read_messages=False),
    #     ctx.author: discord.PermissionOverwrite(read_messages=True)
    # }

    existing_channel = discord.utils.get(guild.channels, name=f"private-room-{ctx.author.name}")
    if not existing_channel:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.author: discord.PermissionOverwrite(read_messages=True)
        }

        channel_name = f"private-room-{ctx.author.name}"
        channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        await ctx.send(f'Private channel {channel_name} created for {ctx.author.mention}.')

        # Store created channel in dictionary
        user_channels[ctx.author.id] = channel_name
        await ctx.send(f"Private room created: {channel.mention}")

        # Invite specified members
        invited_users = []
        for member in members:
            if member != ctx.author:
                await channel.set_permissions(member, read_messages=True)
                invited_users.append(member)

        if invited_users:
            await ctx.send(f"Invited {', '.join([user.mention for user in invited_users])} to the private room.")
        else:
            await ctx.send("No eligible students found to invite.")

        # Clean the var so things don't get out of handas and laggy
        if len(user_channels) > 10000:
            user_channels = {}

        # Code to close channel after 5 minutes (example)
        await asyncio.sleep(7200)
        await channel.delete()

@bot.command()
async def close(ctx):
    guild = ctx.guild

    channel = discord.utils.get(guild.channels, name=f"private-room-{ctx.author.name}")
    if channel:
        await channel.delete()
        await ctx.send(f'Salon {f"private-room-{ctx.author.name}"} supprimé.')
    else:
        await ctx.send('Salon introuvable.')

# Command: Help (to display available commands)
@bot.command()
async def aide(ctx):
    embed = discord.Embed(title="aide - Available Commands", description="List of available commands:")

    if "Staff" in [role.name for role in ctx.author.roles]:
        # List of commands and their descriptions
        commands_list = [
            ("!giverole [username] [role_name]", "Give a role to a user (Staff only)"),
            ("!getroles", "List roles of the user"),
            ("!getroom @[member1] @[member2] ...", "Create a private room for the user and invited members"),
            ("!close", "Close user's private channel"),
            ("!chatbot [message]", "Chat with the GPT-3 AI"),
        ]
        # commands_list.append(("!giverole [username] [role_name]", "Give a role to a user (Staff only)"))

    # Si l'utilisateur n'est que visiteur
    elif len(ctx.author.roles) <= 1:
        commands_list = [
            ("!getroles", "List roles of the user")
            # Maybe Add a new command like !askrole
        ]
    else :
        commands_list = [
            ("!getroles", "List roles of the user"),
            ("!getroom @[member1] @[member2] ...", "Create a private room for the user and invited members"),
            ("!close", "Close user's private channel"),
            ("!chatbot [message]", "Chat with the GPT-3 AI"),
        ]



    for command, description in commands_list:
        embed.add_field(name=command, value=description, inline=False)

    await ctx.send(embed=embed)

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
bot.run('TOKEN HERE')
