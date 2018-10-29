#Chris Ward Tutorial Bot with added features
# Team Software Project
import discord

TOKEN = 'NTAyMTYxOTQzOTQ4NDI3MjY0.DqkAzA.BO4zAvuN-E0OAAzV8B8vstUyD94'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)
    elif message.content.startswith('!bot'):
            await client.send_message(message.channel, "You rang?")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)