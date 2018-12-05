# Work with Python 3.6, not 3.7
from discord.ext.commands import Bot
from discord import Game
import random


BOT_PREFIX = ("!")
TOKEN = 'NTAxNjAzMzQyMTUwMjcwOTc5.DrGNDQ.sP4_kl0CJM-6nTq3KL8Qf2cMmvI'
client = Bot(command_prefix = BOT_PREFIX)

textart = ["`Gallows\n   +----\n   |\n   |\n   |\n   |\n   |\n __|______\n`",
"`Rope\n   +---+\n   |   |\n   |   +\n   |\n   |\n   |\n __|______`",
"`Head \n   +---+\n   |   |\n   |   O\n   |\n   |\n   |\n __|______`",
"`Torso\n   +---+\n   |   |\n   |   O\n   |   |\n   |   |\n   |\n __|______`",
"`Upper Body\n   +---+\n   |   |\n   |   O\n   |  /|\\\n   |   |\n   |\n __|______`",
"`DEAD\n   +---+\n   |   |\n   |   O\n   |  /|\\\n   |   |\n   |  / \\\n __|______`"]

current_game = 0 #Used to check if game is running
possible_words = ['WORD', 'TEST', 'CAR', 'PLANE'] #List of possible words, input them in caps
answer = ''
temparray = [] #used for storring apended underscores
guess = '' #current guessed letter
letters_guessed = [] #stored list of all guessed letters
correctletterscount = 0  #stores number of guess attempts
lives = 0    #the number of wrong guesses left before game over
testcount = 0
test = -1

@client.command()
async def start_game():
    global current_game, answer, temparray, letters_guessed, correctletterscount, lives, textart, test, testcount

    if current_game != 1:

        current_game = 1
        temparray = []
        letters_guessed = []
        correctletterscount = 0
        lives = 5

        if (test >= 0):
            answer = possible_words[test]
            test += 1
        else:
            answer = random.choice(possible_words)
        await client.change_presence(game=Game(name='Hangman'))
        for i in range(0,len(answer)):
            temparray.append('-')

            "".join(temparray)
        await client.say("Lets start! Your word is "+ str(len(answer)) +" letters long. You have 5 lives.")
        await client.say(textart[0])
        await client.say(" ".join(temparray))
    else:
        await client.say("Sorry please finish or stop the previous game before starting a new one")


@client.command()
async def stop_game():
    global current_game, answer
    if (current_game == 1):
        current_game = 0
        answer = ''
        await client.change_presence(game=None, status=None)
        await client.say("You scared? Let me know when you want to play again!")
    else:
        await client.say("You have to be in a game to be able to stop one.")


@client.command()
async def guess(guess):
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
                await client.change_presence(game=None,status=None)
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
    else:
        await client.say("You have to start a game before you guess.")

@client.command()
async def testing():
    global possible_words, test
    test = 0
    possible_words = ['TESTING','BUG','WORKING','UPPER','LOWER','STOP','DOUBLE']
    await client.say("Testing mode on.")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)