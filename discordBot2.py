# -*- coding: utf-8 -*-
import bitcoin as f1
import random
import requests
import asyncio
import json
from discord import Game
from discord.ext.commands import Bot
import goslate

BOT_PREFIX = ('//')
TOKEN = 'NTAyMTYxOTQzOTQ4NDI3MjY0.DqkAzA.BO4zAvuN-E0OAAzV8B8vstUyD94'

client = Bot(command_prefix=BOT_PREFIX)

# specifies name that can be called instead of function name


@client.command(name='8ball',
                description='Answers a yes/no question.',
                brief='Answers from a list at random',
                aliases=['eightBall', 'eight', '8'],
                pass_context=True)
async def eightBall(context):
    possibleResponses = [
        'Yes', 'no', 'maybe'
    ]
    await client.say(random.choice(possibleResponses) + ', ' + context.message.author.mention)


@client.command(description='squares the number given to the bot',
                aliases=['^', 'sqr'])
async def square(number):
    squaredVal = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squaredVal))


@client.event
async def onReady():
    await client.change_presence(game=Game(name="with humans"))
    print("logged in as " + client.user.name)


@client.command(description='Retreives teh current Bitcoin value',
                aliases=['Bit', 'BC'])
async def bitcoin():
    await client.say("Bitcoin price is: $" + f1.bitcoinVal())


@client.command(description='Retreives the current weather data via zipcode',
                aliases=['Meteorologist', 'W'])
async def weather(zipcode):
    url = 'https://api.openweathermap.org/data/2.5/weather?zip={},us&appid=9a5a4353163c0c15faf3e6cc7d2ce583'.format(zipcode)
    response = requests.get(url)
    '''value = response.text''' 
    valJSON = response.json()
    print('\n'+ url +'\n')
    valTempK = float(valJSON['main'] ['temp'])
    valTempF = round(float(valTempK * 9/5 - 459.67))
    valDescr = valJSON['weather'][0] ['description']
    valWindSpeed= float(valJSON['wind']['speed'])
    await client.say("Current weather in your area: \n Temperature: " + str(valTempF)+' F \n Forecast: '+ str(valDescr)+ '\n Wind Speed: ' + str(valWindSpeed)+ 'mph')





'''Google translate
language code must be ISO-639-1 language code 
'''

@client.command(description='Tranalte text given into a different language',
                aliases=['Translate', 't', 'T', 'Goslate'])
async def Gtranslate(message):
    temp = message.content
    gs = goslate.Goslate()
    translatedText = gs.translate(temp,'es')

    await client.say("Transalted Text: " + translatedText)



async def listServers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current Servers: ")
        for server in client.servers:
            print(server.name)
        print("\n________________\n\n ")
        await asyncio.sleep(6000)

   



client.loop.create_task(listServers())

client.run(TOKEN)
