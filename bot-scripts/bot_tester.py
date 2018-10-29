# Work with Python 3.6
import discord

token = input('Token?: ')
bot_username = input('Username of bot to test?: ')
test_filename = input('Name of test file?: ')
channel_name = input('Name of channel?: ')
# load test_file
test_lines = open(test_filename).read().splitlines()
global line_index
line_index = 0
test_running = False

def increment_ind(index):
    global line_index
    line_index = index + 1

client = discord.Client()

client.get_all_channels()

# TODO: need to retrieve channel based on name, rather than first in enumeration


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    """
    for server in client.servers:
        for channel in server.channels:
            if channel.name == "Text Channels":
                test_channel = channel
                print(test_channel.name)
                await client.send_message(test_channel, test_lines[0])
    """

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content == "begin test":
        global test_running
        test_running = True
        await client.send_message(message.channel, test_lines[line_index])

    if test_running:
        print(message.author.name)
        print(message.content)
        print(message.channel.name)
        increment_ind(line_index)
        assert message.content == test_lines[line_index]
        #line_index += 1
        increment_ind(line_index)
        if line_index is len(test_lines):
            print("test complete")
            client.close()
            sys.exit
        await client.send_message(message.channel, test_lines[line_index + 1])
        

        #if message.content.startswith('!hello'):
        #    msg = 'Hello {0.author.mention}'.format(message)
        #    await client.send_message(message.channel, msg)



client.run(token)
