import discord
import openai
from openai import OpenAI
from discord.ext import commands
import random as r

intents = discord.Intents.all()
intents.messages = True  # Active l'intention pour les événements de message

# Configuration Discord
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration OpenAI
api_key = 'API KEY'
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
async def give_role(ctx, username: str, role_name: str):
    if ctx.author == bot.user:
        return

    # Ensure the command issuer has the 'Staff' role
    if "Staff" in [role.name for role in ctx.author.roles]:
        # Find the member in the guild
        member = discord.utils.get(ctx.guild.members, name=username)
        if not member:
            await ctx.send(f"User '{username}' not found.")
            return

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

# Command: Revoke role
@bot.command(name="revokerole")
async def give_role(ctx, username: str, role_name: str):
    if ctx.author == bot.user:
        return

    # Ensure the command issuer has the 'Staff' role
    if "Staff" in [role.name for role in ctx.author.roles]:
        # Find the member in the guild
        member = discord.utils.get(ctx.guild.members, name=username)
        if not member:
            await ctx.send(f"User '{username}' not found.")
            return

        # Find the role in the guild
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await member.add_roles(role)
            await ctx.send(f"{member.mention} has been given the '{role_name}' role!")
        else:
            await ctx.send(f"Role '{role_name}' not found.")
    else:
        await ctx.send("You don't have permission to use this command.")


@bot.command(name="getroom")
async def get_room(ctx, max_users: int = 1):
    # Create a private text channel
    if max_users > 5:
        await ctx.send("Error: Maximum group size is 5.")
        return


    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True)
    }

    channel = await guild.create_text_channel(f"private-room-{ctx.author.name}", overwrites=overwrites)
    await ctx.send(f"Private room created: {channel.mention}")

    # Invite other users with the "STUDENT" role
    student_role = discord.utils.get(guild.roles, name="STUDENT")
    if not student_role:
        await ctx.send("No 'STUDENT' role found in the server.")
        return

    students = [member for member in guild.members if student_role in member.roles and member != ctx.author]

    # Shuffle the list to randomize the invitations
    r.shuffle(students)

    invited_users = []
    for student in students[:max_users-1]:
        await channel.set_permissions(student, read_messages=True)
        invited_users.append(student)

    if invited_users:
        await ctx.send(f"Invited {', '.join([user.mention for user in invited_users])} to the private room.")
    else:
        await ctx.send("No eligible students found to invite.")


# Lancer le bot
bot.run('DISCORD Token')
