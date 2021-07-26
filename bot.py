# A bot for the Discord server prontx
# Author : Matsvei Hauryliuk, VUT FIT Student
# Github : @prontx

# bot.py
# Main driver file

# Imports the package containing math functions definitions
from copy import deepcopy
from util import calculator_functions 
# Can be used like: calculator_functions.add(a, b)

# To make requests to third party APIs
from requests.models import Response
import requests, json

# To use the Google Translate APIs
from googletrans import Translator

# To work with environment files
import os

import discord
from discord.ext import commands

# Will be used to calculate current time
from datetime import date, datetime

from dotenv import load_dotenv
# Reads key-value pairs from the .env file
load_dotenv()

# Gets the server token and the server name from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# A required step to see all users
intents = discord.Intents.all()

# Creating a bot while also specialising the command prefix symbols and the intents
# so we're able to see all the users and not just bots
bot = commands.Bot(command_prefix=('$', '?'), intents=intents)

###################################################################################################

# Imports required to use the SQLite databases
import sqlite3
from sqlite3 import Error

database = r'bot.db'

sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                discord_ID integer PRIMARY KEY,
                                user_name text NOT NULL,
                                channels text,
                                begin_date text NOT NULL,
                                permissions text NOT NULL  
                            );"""

# Creating a database connection to a SQLite database
conn = None
    
conn = sqlite3.connect(database)

# Creating a cursor to operate on the table
c = conn.cursor()

# The code to create the table
c.execute(sql_create_users_table)

conn.commit()

###################################################################################################

# Command to calculate the given operation on the given numbers
# Uses the functions imported from the util package
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

    # Turns string into dictionary
    result = eval(result)

    result = result["data"]["translations"][0]["translatedText"]

    await ctx.send(f'```The translation of your word/phrase is: {result}```')

# Prints the manual
@bot.command()
async def manual(ctx):
    await ctx.send(f'''```TBD```''')

# Command to determine the temperature in a city given as argument
# Uses third party geopy APIs
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
# Adds all the users' data to the database
@bot.event
async def on_connect():
    for guild in bot.guilds:
        for member in guild.members:
            # Field 4 of the database
            firstSessionDate = datetime.now()

            # Field 1 of the database
            global userID
            userID = member.id

            # Field 2 of the database
            userName = member.name

            # Field 5 of the database
            permissions = 'User'

            # Field 3 of the database
            channels = 'General'

            conn = sqlite3.connect(database)

            # Creating a cursor to operate on the table
            c = conn.cursor()  

            # The code to create the table
            c.execute("""INSERT or IGNORE INTO users VALUES (?, ?, ?, ?, ?)""",
                (userID, userName, channels, firstSessionDate, permissions))

            # For the changes to take place
            conn.commit()

# To be used later
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

            # Field 5 of the database
            permissions = 'User'

            # Field 3 of the database
            channels = 'General'

            conn = sqlite3.connect(database)

            # Creating a cursor to operate on the table
            c = conn.cursor()  

            # The code to create the table
            c.execute("""INSERT or IGNORE INTO users VALUES (?, ?, ?, ?, ?)""",
                (userID, userName, channels, firstSessionDate, permissions))

            # For the changes to take place
            conn.commit()

@bot.event
async def on_message(message):
    # Prints the info about the message author
    if message.content == '$me':
        conn = sqlite3.connect(database)

        # Creating a cursor to operate on the table
        c = conn.cursor()  

        c.execute("SELECT * FROM users WHERE discord_ID=?", (message.author.id, ))

        # Gets the row with the user's data
        row = c.fetchall()

        await message.channel.send(f'```{row}```')

        # For the changes to take place
        conn.commit()

# The code for implementation of reaction roles
@bot.event
async def on_raw_reaction_add(payload):
    channel = 867854256647176252
    message = 867855236861132860
    if payload.channel_id == channel and payload.message_id == message:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # This is the problem
        emoji = payload.emoji

        import copy
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

        # Creating a cursor to operate on the table
        c = conn.cursor()  

        # The code to create the table
        c.execute("""UPDATE users SET channels=? WHERE discord_ID=?""", (channels, member.id))

        # For the changes to take place
        conn.commit()

# Case reaction is removed


@bot.event
async def on_raw_reaction_remove(payload):
    channel = 867854256647176252
    message = 867855236861132860
    if payload.channel_id == channel and payload.message_id == message:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # This is the problem
        emoji = payload.emoji

        import copy
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

        # Creating a cursor to operate on the table
        c = conn.cursor()  

        channels = str(channels)

        # The code to create the table
        c.execute("""UPDATE users SET channels=? WHERE discord_ID=?""", (channels, member.id))

        # For the changes to take place
        conn.commit()


bot.run(TOKEN)