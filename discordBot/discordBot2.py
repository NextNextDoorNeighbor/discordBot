# -*- coding: utf-8 -*-
import bitcoin as bitC
import weather as weath
import random
import requests
import asyncio
import json
from discord import Game
from discord.ext.commands import Bot
import goslate
import praw

BOT_PREFIX = ('!')
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
        'Yes', 'no', 'maybe', 'the outcome appears unclear', 'I dunno'
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
    await client.say("Bitcoin price is: $" + bitC.bitcoinVal())


@client.command(description='Retreives the current weather data via zipcode',
                aliases=['Meteorologist', 'W'])
async def weather(zipcode):

    await client.say(weath.curWeath(zipcode))


'''Google translate
language code must be ISO-639-1 language code 
'''


@client.command(description='Tranalte text given into a different language',
                aliases=['Translate', 't', 'T', 'Goslate'])
async def translate(ISO, *text):
    mess = ' '.join(text)
    gs = goslate.Goslate()
    translatedText = gs.translate(mess, ISO)
    await client.say("Translated Text: {} \n ".format(translatedText))


# Hangman

textart = ["`Gallows\n   +----\n   |\n   |\n   |\n   |\n   |\n __|______\n`",
           "`Rope\n   +---+\n   |   |\n   |   +\n   |\n   |\n   |\n __|______`",
           "`Head \n   +---+\n   |   |\n   |   O\n   |\n   |\n   |\n __|______`",
           "`Torso\n   +---+\n   |   |\n   |   O\n   |   |\n   |   |\n   |\n __|______`",
           "`Upper Body\n   +---+\n   |   |\n   |   O\n   |  /|\\\n   |   |\n   |\n __|______`",
           "`DEAD\n   +---+\n   |   |\n   |   O\n   |  /|\\\n   |   |\n   |  / \\\n __|______`"]

current_game = 0  # Used to check if game is running
# List of possible words, input them in caps
possible_words = ['TEST', 'WORD', 'CAR', 'PLANE', 'HELLO', 'WORLD', 'DISCORD', 'FUN', 'COMPUTER']
answer = ''
temparray = []  # used for storring apended underscores
guess = ''  # current guessed letter
letters_guessed = []  # stored list of all guessed letters
correctletterscount = 0  # stores number of guess attempts
lives = 0  # the number of wrong guesses left before game over


@client.command()
async def start_game():
    global current_game, answer, temparray, letters_guessed, correctletterscount, lives, textart

    temparray = []
    letters_guessed = []
    correctletterscount = 0
    lives = 5

    if current_game != 1:
        current_game = 1
        answer = random.choice(possible_words)
        await client.say(answer)
        await client.change_presence(game=Game(name='Hangman'))
        for i in range(0, len(answer)):
            temparray.append('-')

            "".join(temparray)
        await client.say("Lets start! Your word is " + str(len(answer)) + " letters long. You have 5 lives.")
        await client.say(textart[0])
        await client.say(" ".join(temparray))
    else:
        await client.say("Sorry please finish or stop the previous game before starting a new one")


@client.command()
async def stop_game():
    global current_game, answer
    current_game = 0
    answer = ''
    await client.say("You scared? Let me know when you mant to play again!")


@client.command(description='Passes an arg to a game of hangman',
                brief='guess one letter',
                aliases=['guess', 'g', 'G'])
async def guessi(guess):
    global current_game, answer, temparray, letters_guessed, correctletterscount, lives, textart
    if (current_game == 1):
        if str.isalpha(guess) and len(guess) is 1 and str.upper(guess) not in letters_guessed:
            if str.upper(guess) in answer:
                await client.say(guess + " is in the answer. Keep guessing!")
                for i in range(0, len(answer)):
                    if answer[i] == str.upper(guess):
                        temparray[i] = str.upper(guess)
                        correctletterscount += 1
            else:
                await client.say(guess + " isn't in the word, DUH!")
                lives -= 1

            letters_guessed.append(str.upper(guess))
            await client.say(" ".join(temparray))
            await client.say("You have " + str(lives) + " left!")
            await client.say(textart[5 - lives])
            await client.say("Letters that you have guessed already: "+" ".join(letters_guessed))

            if lives == 0:
                await client.say("Sorry, you're bad. You lose")
                current_game = 0
            if correctletterscount == len(answer):
                await client.say("Nevermind...wow...you managed to win. Cool")
                current_game = 0
        elif str.upper(guess) in letters_guessed:
            await client.say("You already tried that one...")
            await client.say("You have " + str(lives) + " left!")
            await client.say(textart[5 - lives])
            await client.say("Letters that you have guessed already: " + " ".join(letters_guessed))
        else:
            await client.say("No cheating, only one letter at a time.")
            await client.say("You have " + str(lives) + " left!")
            await client.say(textart[5 - lives])
            await client.say("Letters that you have guessed already: " + " ".join(letters_guessed))


# end of Hangman


# Reddit Bot
myreddit = praw.Reddit(client_id='BtAeLh20Bs55tw',
                       client_secret='Xbb4D0H2pxrehnR60HMqUDiIlEs',
                       user_agent='redmemes_v1',
                       username='jrmcneil',
                       password='Needtoadd1later')

try:
    myreddit.user.me()
except Exception as exc:
    print(exc)

oldpost = ''
post = ''


@client.command()
async def reddit(sub):
    global oldpost, post
    # Uses 16 because if old post is pulled again go to next, ( no out of index if rand = 15)
    posts = myreddit.subreddit(sub).hot(limit=16)
    random_post_number = random.randint(0, 15)
    for i in range(0, random_post_number - 1):
        post = next(x for x in posts if not x.stickied)
    if oldpost == post.url:
        post = next(x for x in posts if not x.stickied)
    else:
        oldpost = post.url
    await client.say(post.title)
    await client.say(post.url)


async def listServers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current Servers: ")
        for server in client.servers:
            print(server.name)
        print("\n________________\n ")
        await asyncio.sleep(6000)


client.loop.create_task(listServers())

client.run(TOKEN)
