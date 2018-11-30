# Work with Python 3.6
import discord

TOKEN = 'NTAxNDMwODAzOTgxNjY0MjY3.DqZWcw.T7C9fs-a7xtNdiXDNFwO9hEfMt0'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    #client.send_message(message.channel, message)
    client.send_message(message.channel, message.content)
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.name}'.format(message)
        await client.send_message(message.channel, msg)



client.run(TOKEN)