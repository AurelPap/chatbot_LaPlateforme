import discord
import openai
from openai import OpenAI
from discord.ext import commands

intents = discord.Intents.all()
intents.messages = True  # Active l'intention pour les événements de message

# Configuration Discord
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration OpenAI
api_key = 'TOKEN HERE'
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

    await member.add_roles(visitor_role)


async def on_message(message):
    if message.author.bot:
        return  # Ignore messages from bots

    # Command to give roles based on a specific message
    if message.content.startswith('!giverole'):
        if "Staff" in [role.name for role in message.author.roles]:
            if "Staff" not in message.content.lower():
                student_role = discord.utils.get(message.guild.roles, name="Student")


            if "Staff" in message.content.lower():
                staff_role = discord.utils.get(message.guild.roles, name="STAFF")
                await message.author.add_roles(staff_role)
                await message.channel.send(f"{message.author.mention} join the Staff !")

            elif "b1ia" in message.content.lower():
                b1_role = discord.utils.get(message.guild.roles, name="B1")
                ia_role = discord.utils.get(message.guild.roles, name="IA")
                await message.author.add_roles(student_role, b1_role, ia_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en B1 IA !")

            elif "b2ia" in message.content.lower():

                b2_role = discord.utils.get(message.guild.roles, name="B2")
                ia_role = discord.utils.get(message.guild.roles, name="IA")
                await message.author.add_roles(student_role, b2_role, ia_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en B2 IA !")

            elif "b3ia" in message.content.lower():

                b3_role = discord.utils.get(message.guild.roles, name="B3")
                ia_role = discord.utils.get(message.guild.roles, name="IA")
                await message.author.add_roles(student_role, b3_role, ia_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en B3 IA !")

            elif "msc1ia" in message.content.lower():

                msc1_role = discord.utils.get(message.guild.roles, name="MSC1")
                ia_role = discord.utils.get(message.guild.roles, name="IA")
                await message.author.add_roles(student_role, msc1_role, ia_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en Master IA !")

            elif "msc2ia" in message.content.lower():

                msc2_role = discord.utils.get(message.guild.roles, name="MSC2")
                ia_role = discord.utils.get(message.guild.roles, name="IA")
                await message.author.add_roles(student_role, msc2_role, ia_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en Deuxième année de Master IA !")

            elif "b1dev" in message.content.lower():

                b1_role = discord.utils.get(message.guild.roles, name="B1")
                dev_role = discord.utils.get(message.guild.roles, name="Dev")
                await message.author.add_roles(student_role, b1_role, dev_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en B1 Développement !")

            elif "b2dev" in message.content.lower():

                b2_role = discord.utils.get(message.guild.roles, name="B2")
                dev_role = discord.utils.get(message.guild.roles, name="Dev")
                await message.author.add_roles(student_role, b2_role, dev_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en B2 Développement !")

            elif "b3dev" in message.content.lower():

                b3_role = discord.utils.get(message.guild.roles, name="B3")
                dev_role = discord.utils.get(message.guild.roles, name="Dev")
                await message.author.add_roles(student_role, b3_role, dev_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en B3 Développement !")

            elif "msc1dev" in message.content.lower():

                msc1_role = discord.utils.get(message.guild.roles, name="MSC1")
                dev_role = discord.utils.get(message.guild.roles, name="Dev")
                await message.author.add_roles(student_role, msc1_role, dev_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en Master Développement !")

            elif "msc2dev" in message.content.lower():

                msc2_role = discord.utils.get(message.guild.roles, name="MSC2")
                dev_role = discord.utils.get(message.guild.roles, name="Dev")
                await message.author.add_roles(student_role, msc2_role, dev_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en Deuxième année de Master Développement !")

            elif "b1logiciel" in message.content.lower():

                b1_role = discord.utils.get(message.guild.roles, name="B1")
                logiciel_role = discord.utils.get(message.guild.roles, name="Logiciel")
                await message.author.add_roles(student_role, b1_role, logiciel_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en B1 Logiciel !")

            elif "b2logiciel" in message.content.lower():

                b2_role = discord.utils.get(message.guild.roles, name="B2")
                logiciel_role = discord.utils.get(message.guild.roles, name="Logiciel")
                await message.author.add_roles(student_role, b2_role, logiciel_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en B2 Logiciel !")

            elif "b3logiciel" in message.content.lower():

                b3_role = discord.utils.get(message.guild.roles, name="B3")
                logiciel_role = discord.utils.get(message.guild.roles, name="Logiciel")
                await message.author.add_roles(student_role, b3_role, logiciel_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en B3 Logiciel !")

            elif "msc1logiciel" in message.content.lower():

                msc1_role = discord.utils.get(message.guild.roles, name="MSC1")
                logiciel_role = discord.utils.get(message.guild.roles, name="Logiciel")
                await message.author.add_roles(student_role, msc1_role, logiciel_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en Master Logiciel !")

            elif "msc2logiciel" in message.content.lower():

                msc2_role = discord.utils.get(message.guild.roles, name="MSC2")
                logiciel_role = discord.utils.get(message.guild.roles, name="Logiciel")
                await message.author.add_roles(student_role, msc2_role, logiciel_role)
                await message.channel.send(f"{message.author.mention} est désormais étudiant en Deuxième année de Master Logiciel !")

            else:
                await message.channel.send("Command format incorrect. Use !giverole {formation Level(b2)}{formation Tag(ia)} or b1 or Staff.")
        else:
            await message.channel.send("You don't have permission to use this command.")

    if message.content.startswith('!GetRole'):
        roles = [role.name for role in message.author.roles if role.name != "@everyone"]
        if roles:
            await message.channel.send(f"Your roles are: {', '.join(roles)}")
        else:
            await message.channel.send("You don't have any roles.")


# Lancer le bot
bot.run('TOKEN HERE')
