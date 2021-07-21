# A bot for the Discord server prontx
# Author : Matsvei Hauryliuk, VUT FIT Student
# Github : @prontx

# bot.py
# Main driver file

# Imports the package containing math functions definitions
from util import calculator_functions 
# Can be used like: calculator_functions.add(a, b)

# To make requests to third party APIs
from requests.models import Response
import requests, json

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

intents = discord.Intents.all()

# Creating a bot while also specialising the command prefix symbols
bot = commands.Bot(command_prefix=('$', '?'), intents=intents)

###################################################################################################

# Imports required to use the SQLite databases
import sqlite3
from sqlite3 import Error

database = r'bot.db'

sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                discord_ID integer PRIMARY KEY,
                                user_name text NOT NULL,
                                channels text NOT NULL,
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

# Closing the connection to the database
#conn.close()

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
    await ctx.send(f'''```
$pomoc, $helpplz, $manual, $napoveda - print the manual

$time <X>, $cas <X> - prints the time in city X, returns an error if the city hasn't been found or if the input is invalid

$weather <X>, $pocasi <X> - prints the weather report of the city X, returns an error if the city hasn't been found or if the input is invalid

$covid, $korona <X> - prints the covid report of the country X, returns an error if the country hasn't been found or if the input is invalid

$translate <X> <Y> <z>, $prelozit <X> <Y> <z> - prints the translation the word <z> from language X to language Y

$calculate <X> <Y> <z>, $spocitat <X> <Y> <z> - performs the <z> mathematical operation on numbers X and Y, returns errors if input is invalid

$compilate <LANG> <CODE> - compilates the code written in the given language and prints the result of compilation.
    ```''')

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


# Handles every time a user connects to the server
# Adds their data to the database

# Is updated with each user connection
userPK = 0

@bot.event
async def on_connect():
    # Field 5 of the database
    firstSessionDate = datetime.now()

    # Field 2 of the database
    global userID
    userID = bot.user.id

    # Field 3 of the database
    userName = bot.user.name

    # Field 6 of the database
    permissions = 'User'

    # Field 4 of the database
    channels = ['#general']
    channels = str(channels)

    conn = sqlite3.connect(database)

    # Creating a cursor to operate on the table
    c = conn.cursor()  

    # The code to create the table
    c.execute("""INSERT or IGNORE INTO users VALUES (?, ?, ?, ?, ?)""",
        (userID, userName, channels, firstSessionDate, permissions))

    # For the changes to take place
    conn.commit()

@bot.command()
async def me(ctx):
    conn = sqlite3.connect(database)

    # Creating a cursor to operate on the table
    c = conn.cursor()  

    c.execute("SELECT * FROM users WHERE discord_ID=?", (userID, ))

    # Gets the row with the user's data
    row = c.fetchall()

    await ctx.send(f'```{row}```')

    # For the changes to take place
    conn.commit()

@bot.command()
async def deletethisshit(ctx):
    for guild in bot.guilds:
        for member in guild.members:
            await ctx.send(f'```{member}```')

###################################################################################################

# The other name for the calculate command
@bot.command()
async def spocitat(ctx, num1, num2, op):
    # Casting the arguments to floats so they're not considered strings
    try:
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
            if num2 == 0:
                await ctx.send(f'```Cannot divide by zero!```')
                raise ZeroDivisionError
            result = calculator_functions.divide(num1, num2)
            await ctx.send(f'```The result of the operation is: {result}```')

        if op == '//':
            if num2 == 0:
                await ctx.send(f'```Cannot divide by zero!```')
                raise ZeroDivisionError
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

# The other name for the translate command
@bot.command()
async def prelozit(ctx, firstlang, secondlang, *args):
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

@bot.command()
async def pomoc(ctx):
    await ctx.send(f'''```
$pomoc, $helpplz, $manual, $napoveda - print the manual

$time <X>, $cas <X> - prints the time in city X, returns an error if the city hasn't been found or if the input is invalid

$weather <X>, $pocasi <X> - prints the weather report of the city X, returns an error if the city hasn't been found or if the input is invalid

$covid, $korona <X> - prints the covid report of the country X, returns an error if the country hasn't been found or if the input is invalid

$translate <X> <Y> <z>, $prelozit <X> <Y> <z> - prints the translation the word <z> from language X to language Y

$calculate <X> <Y> <z>, $spocitat <X> <Y> <z> - performs the <z> mathematical operation on numbers X and Y, returns errors if input is invalid

$compilate <LANG> <CODE> - compilates the code written in the given language and prints the result of compilation.
    ```''')

@bot.command()
async def helpplz(ctx):
    await ctx.send(f'''```
$pomoc, $helpplz, $manual, $napoveda - print the manual

$time <X>, $cas <X> - prints the time in city X, returns an error if the city hasn't been found or if the input is invalid

$weather <X>, $pocasi <X> - prints the weather report of the city X, returns an error if the city hasn't been found or if the input is invalid

$covid, $korona <X> - prints the covid report of the country X, returns an error if the country hasn't been found or if the input is invalid

$translate <X> <Y> <z>, $prelozit <X> <Y> <z> - prints the translation the word <z> from language X to language Y

$calculate <X> <Y> <z>, $spocitat <X> <Y> <z> - performs the <z> mathematical operation on numbers X and Y, returns errors if input is invalid

$compilate <LANG> <CODE> - compilates the code written in the given language and prints the result of compilation.
    ```''')

@bot.command()
async def napoveda(ctx):
    await ctx.send(f'''```
$pomoc, $helpplz, $manual, $napoveda - print the manual

$time <X>, $cas <X> - prints the time in city X, returns an error if the city hasn't been found or if the input is invalid

$weather <X>, $pocasi <X> - prints the weather report of the city X, returns an error if the city hasn't been found or if the input is invalid

$covid, $korona <X> - prints the covid report of the country X, returns an error if the country hasn't been found or if the input is invalid

$translate <X> <Y> <z>, $prelozit <X> <Y> <z> - prints the translation the word <z> from language X to language Y

$calculate <X> <Y> <z>, $spocitat <X> <Y> <z> - performs the <z> mathematical operation on numbers X and Y, returns errors if input is invalid

$compilate <LANG> <CODE> - compilates the code written in the given language and prints the result of compilation.
    ```''')

# Command to determine the temperature in a city given as argument
# Uses third party geopy APIs
@bot.command()
async def pocasi(ctx, *args):
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

# Connecting the bot to the server
bot.run(TOKEN)