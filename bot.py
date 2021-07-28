# Discord Server Bot Project
# Author : Matsvei Hauryliuk, VUT FIT Student
# Github : @prontx
# July 2021

# bot.py
# The driver file for the bot



# Section 1: needed imports and initial setup
###################################################################################################



# Imports the package containing math functions definitions
from util import calculator_functions 

# Allows to make requests to third party APIs
import requests, json

# Enables using the Google Translate APIs
from googletrans import Translator

# Needed to work with environment files
import os

import discord
from discord.ext import commands

# Will be used to calculate current time
from datetime import datetime

from dotenv import load_dotenv

# Reads key-value pairs from the .env file
load_dotenv()

# Gets the server token and the server name from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# A required step so that the bot is able to see all users
intents = discord.Intents.all()

# Creating a bot while also specialising the command prefix symbols and the intents
# so we're able to see all the users and not just bots
bot = commands.Bot(command_prefix=('$', '?', '!'), intents=intents)

# Required to use the SQLite databases
import sqlite3

# To handle asynchronous accesses to shared variables
import asyncio



# Section 2: database setup
###################################################################################################



# Creates a DB file in the same folder to store data
database = r'bot.db'

# SQL command to create a table <users> containing 4 fields:
# Discord ID, Discord user name, channels user follows and date of first connection
sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                discord_ID integer PRIMARY KEY,
                                user_name text NOT NULL,
                                channels text,
                                begin_date text NOT NULL
                            );"""

# Creating a connection to a SQLite database
conn = sqlite3.connect(database)

# Creating a cursor to perform actions with the table
c = conn.cursor()

# The code to create the table
c.execute(sql_create_users_table)

# For the changes to take place
conn.commit()



# Section 3: bot events and commands 
###################################################################################################



# Command to perform a certain(given) mathematical operation on the presented numbers
# Uses the functions imported from the util package
# Arguments: first number, second number, operation
@bot.command()
async def calculate(ctx, num1, num2, op):
    try:
        # Casting the arguments to floats so they're not considered strings
        num1 = float(num1)
        num2 = float(num2)

        if op == '+':
            result = calculator_functions.add(num1, num2)
            await ctx.send(f'```The result of the operation is: {result}```')

        if op == '-':
            result = calculator_functions.subtract(num1, num2)
            await ctx.send(f'```The result of the operation is: {result}```')

        if op == '*':
            result = calculator_functions.multiply(num1, num2)
            await ctx.send(f'```The result of the operation is: {result}```')

        if op == '/':
            result = calculator_functions.divide(num1, num2)
            await ctx.send(f'```The result of the operation is: {result}```')

        if op == '//':
            result = calculator_functions.divide_no_remainder(num1, num2)
            await ctx.send(f'```The result of the operation is: {result}```')

        if op == '**':
            result = calculator_functions.power(num1, num2)
            await ctx.send(f'```The result of the operation is: {result}```')

        if op == '%':
            result = calculator_functions.modulo(num1, num2)
            await ctx.send(f'```The result of the operation is: {result}```')

    except ValueError:
        await ctx.send(f'```Enter valid values!```')

    except ZeroDivisionError:
        await ctx.send(f'```Cannot divide by zero!```')

# Command to translate the given word from one language to the other
# Uses Google Translator APIs
# Arguments: first language, second language, word or expression to be translated
@bot.command()
async def translate(ctx, firstlang, secondlang, *args):
    word = ''
    for i in range(len(args)):
        word += args[i]
        if i != (len(args) - 1):
            word += ' '

    import http.client
    conn = http.client.HTTPSConnection("google-translate1.p.rapidapi.com")
    payload = "q=" + word + "&format=text&target=" + secondlang +"&source=" + firstlang
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'accept-encoding': "application/gzip",
        'x-rapidapi-key': "03e84d1cebmsh8393172a48e2fb0p137f01jsn5239041898af",
        'x-rapidapi-host': "google-translate1.p.rapidapi.com"
    }
    conn.request("POST", "/language/translate/v2", payload, headers)
    res = conn.getresponse()
    data = res.read()
    result = data.decode('utf-8')

    # Turns the decoded string into dictionary for to be easier to process later
    result = eval(result)

    # Gets the translation itself
    result = result["data"]["translations"][0]["translatedText"]

    await ctx.send(f'```The translation of your word/phrase is: {result}```')

# Command to determine the temperature in a city given as argument
# Uses third party geopy APIs
# Argument: the city name
@bot.command()
async def weather(ctx, *args):
    try:
        city = ''
        for i in range(len(args)):
            city += args[i]
            if i != (len(args) - 1):
                city += ' '

        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent='aurinko')
        location = geolocator.geocode(city)

        latitude = location.raw['lat']
        longitude = location.raw['lon']

        apiKey = '0676b93a6bd7fdb28d17cb06e21aa60b'
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (latitude, longitude, apiKey)

        response = requests.get(url)
        data = json.loads(response.text)
        currentTemp = data["current"]["temp"]

        await ctx.send(f'```Current temperature in {city} is: {currentTemp}°C```')

    except AttributeError:
        await ctx.send(f'```Sorry, can\'t find any info about that city.```')


# Handles every time the client connects to the server
# Adds all the users' data to the dtabase
@bot.event
async def on_connect():
    for guild in bot.guilds:
        for member in guild.members:
            # Field 4 of the database
            # If the user is already there, date won't be changed
            # Otherwise is added
            firstSessionDate = datetime.now()

            # Field 1 of the database
            # Gets the Discord ID
            global userID
            userID = member.id

            # Field 2 of the database
            # Gets the Discord user name
            userName = member.name

            # Field 3 of the database
            # The channels user follows
            channels = 'General'

            conn = sqlite3.connect(database)
            c = conn.cursor()  

            # The code to apply changes to the table
            c.execute("""INSERT or IGNORE INTO users VALUES (?, ?, ?, ?)""",
                (userID, userName, channels, firstSessionDate))

            conn.commit()

# To be used later ??????????????????????? WTF
channels = 'General '

# Called whenever a member joins the server
@bot.event
async def on_member_join(member):
            # Field 4 of the database
            firstSessionDate = datetime.now()

            # Field 1 of the database
            global userID
            userID = member.id

            # Field 2 of the database
            userName = member.name

            # Field 3 of the database
            channels = 'General'

            conn = sqlite3.connect(database)
            c = conn.cursor()  

            # The code to create the table
            c.execute("""INSERT or IGNORE INTO users VALUES (?, ?, ?, ?, ?)""",
                (userID, userName, channels, firstSessionDate))

            conn.commit()

# Called each time a message is sent
@bot.event
async def on_message(message):
    # Prints the info about the message author
    if message.content == '$me':
        conn = sqlite3.connect(database)
        c = conn.cursor()  

        # Searches through the database using the Discord ID as identifier
        c.execute("SELECT * FROM users WHERE discord_ID=?", (message.author.id, ))

        # Gets the row with the needed user's data
        row = c.fetchall()

        await message.channel.send(f'```{row}```')

        conn.commit()

    # Should be here so the message is later sent to be processed by bot.command()
    await bot.process_commands(message)

# To be later used in the voting
answer = 0

# The code for implementation of reaction roles
@bot.event
async def on_raw_reaction_add(payload):
    channel = 867854256647176252
    message = 867855236861132860
    if payload.channel_id == channel and payload.message_id == message:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        emoji = payload.emoji
        global channels

        if str(emoji.name) == '🎥' :
            role = discord.utils.get(guild.roles, name='Movies')
            channels += 'Movies ' 
            if role:
                await member.add_roles(role)
            else:
                print('Something wrong with the role')
    
        if str(emoji.name) == '📖' :
            role = discord.utils.get(guild.roles, name='Books')
            channels += 'Books ' 
            if role:
                await member.add_roles(role)
            else:
                print('Something wrong with the role')

        if str(emoji.name) == '💻' :
            role = discord.utils.get(guild.roles, name='Programming')
            channels += 'Programming ' 
            if role:
                await member.add_roles(role)
            else:
                print('Something wrong with the role')

        if str(emoji.name) == '🤯' :
            role = discord.utils.get(guild.roles, name='Politics')
            channels += 'Politics ' 
            if role:
                await member.add_roles(role)
            else:
                print('Something wrong with the role')

        if str(emoji.name) == '🙂' :
            role = discord.utils.get(guild.roles, name='Offtopic')
            channels += 'Offtopic ' 
            if role:
                await member.add_roles(role)
            else:
                print('Something wrong with the role')

        conn = sqlite3.connect(database)
        c = conn.cursor()  

        # The code to apply changes to the table
        c.execute("""UPDATE users SET channels=? WHERE discord_ID=?""", (channels, member.id))

        conn.commit()

    else:
        global answer

        if str(payload.emoji.name) == '1️⃣':
            answer = answer + 1

        if str(payload.emoji.name) == '2️⃣':
            answer = answer - 1           

# In case reaction is removed
@bot.event
async def on_raw_reaction_remove(payload):
    channel = 867854256647176252
    message = 867855236861132860
    if payload.channel_id == channel and payload.message_id == message:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        emoji = payload.emoji
        global channels

        channels = str(channels)
        channels = channels.split()

        if str(emoji.name) == '🎥' :
            role = discord.utils.get(guild.roles, name='Movies')
            for index in range(len(channels) - 1, -1, -1):
                if channels[index] == 'Movies':
                    channels.pop(index) 
            await member.remove_roles(role)
    
        if str(emoji.name) == '📖' :
            role = discord.utils.get(guild.roles, name='Books')
            for index in range(len(channels) - 1, -1, -1):
                if channels[index] == 'Books':
                    channels.pop(index) 
            await member.remove_roles(role)

        if str(emoji.name) == '💻' :
            role = discord.utils.get(guild.roles, name='Programming')
            for index in range(len(channels) - 1, -1, -1):
                if channels[index] == 'Programming':
                    channels.pop(index)  
            await member.remove_roles(role)

        if str(emoji.name) == '🤯' :
            role = discord.utils.get(guild.roles, name='Politics')
            for index in range(len(channels) - 1, -1, -1):
                if channels[index] == 'Politics':
                    channels.pop(index) 
            await member.remove_roles(role)

        if str(emoji.name) == '🙂' :
            role = discord.utils.get(guild.roles, name='Offtopic')
            for index in range(len(channels) - 1, -1, -1):
                if channels[index] == 'Offtopic':
                    channels.pop(index)  
            await member.remove_roles(role)

        conn = sqlite3.connect(database)
        c = conn.cursor()  

        channels = str(channels)

        # The code to apply changes to the table
        c.execute("""UPDATE users SET channels=? WHERE discord_ID=?""", (channels, member.id))
        conn.commit()

# Command to initiate a vote with two options given as arguments
# Voting is over after 10 seconds and result is printed
# Arguments: the voting question, the first option, the second option
@bot.command()
async def vote(ctx, question, choice1, choice2):
    await ctx.send(f'```{question} \nSelect between {choice1} or {choice2}```')

    await asyncio.sleep(10)

    if answer > 0:
        await ctx.send(f'```{choice1} wins!```')
    elif answer < 0:
        await ctx.send(f'```{choice2} wins!```')
    else:
        await ctx.send(f'```Tie!```')

# Prints the manual
@bot.command()
async def manual(ctx):
    await ctx.send(f'''```
        $manual - print the manual

        $weather city - prints the weather report of the city, returns an error if the city hasn't been found or if the input is invalid

        $translate firstlang secondlang expression - prints the translation of the expression from language firstlang to language secondlang

        $calculate num1 num2 op - performs the op mathematical operation on numbers num1 and num2, returns errors if input is invalid

        ;compile LANG CODE - compilates the code written in the given language and prints the result of compilation (Uses third party bot)

        $vote question choice1 choice2 - starts a vote with two options given as arguments, over after 10 seconds
    
        $me - prints the database information about the user
    
    ```''')



# Section 4: running the bot 
###################################################################################################



bot.run(TOKEN)