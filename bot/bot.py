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

from dotenv import load_dotenv
# Reads key-value pairs from the .env file
load_dotenv()

# Gets the server token and the server name from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Creating a bot while also specialising the command prefix symbols
bot = commands.Bot(command_prefix=('$', '?'))

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
async def translate(ctx, firstlang, secondlang, word):
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
async def prelozit(ctx, firstlang, secondlang, word):
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

# Connecting the bot to the server
bot.run(TOKEN)