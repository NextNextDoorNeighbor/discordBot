import unittest
import sys
# Work with Python 3.6
import discord

if len(sys.argv) is 1:
	# default credentials filename
	credentials_filename = 'bot_tester_credentials.txt'
else:
	# use command line argument if specified
	credentials_filename = sys.argv[1]

credentials_filename = 'bot_tester_credentials.txt'

try:
	credentials_file = open(credentials_filename, 'r')
except IOError:
	print('no credentials file: {}'.format(credentials_filename))
else:
	with credentials_file:
		credentials = credentials_file.read().splitlines()
		token = credentials[0]
		bot_username = credentials[1]
		test_filename = credentials[2]

test_lines = open(test_filename).read().splitlines()
# index of what line in test file we're currently at:
global line_index
line_index = 0
test_running = False
def increment_ind(index):
	global line_index
	line_index = index + 1


class TestStringMethods(unittest.TestCase):
	def test_responses(self):
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

			if message.content == "begin test":
				global test_running
				test_running = True
				print(test_running)
				await client.send_message(message.channel, test_lines[line_index])
				return

			print(test_running)
			#if test_running:
			print(message.author.name)
			print(message.content)
			print(message.channel.name)
			increment_ind(line_index)
			self.assertEqual(message.content, test_lines[line_index])
			"""
			try:
				self.assertEqual(message.content, test_lines[line_index])
			except:
				print("expected: {}".format(test_lines[line_index]))
				print("result: {}".format(message.content))
			"""
			#line_index += 1
			increment_ind(line_index) 
			if line_index is len(test_lines):
				print("test complete")
				await client.close()
				return
				
			else:
				await client.send_message(message.channel, test_lines[line_index + 1])    

				#if message.content.startswith('!hello'):
				#    msg = 'Hello {0.author.mention}'.format(message)
				#    await client.send_message(message.channel, msg)



		client.run(token)


if __name__ == '__main__':
	unittest.main()




