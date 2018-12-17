import unittest
import sys
import time
# Work with Python 3.6
import discord
import asyncio

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
	print(line_index)


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

			if message.content == 'begin test':
				global test_running
				test_running = True
				await client.send_message(message.channel, test_lines[line_index])
				return
			msg = message.content

			increment_ind(line_index)
			current_test_line = test_lines[line_index]
			number_chars = {'0','1','2','3','4','5','6','7','8','9','.',','}
			eightball = ['Yes, ', 'no, ', 'maybe, ', 'the outcome appears unclear, ', 'I dunno, ']
			# expand current_test_line into multiple lines if newline delimiter '&' present
			j = 0
			while j < len(current_test_line):
				# replace & with '\n'
				if current_test_line[j] is '&':
					current_test_line = current_test_line[:j] + '\n' + current_test_line[(j + 1):]
				
				if current_test_line[j] is '%':
					# remove '%' from test line
					current_test_line = current_test_line[:j] + current_test_line[(j + 1):]
					# remove a sequence of numeral chars from msg before running test comparison
					k = 0
					while k < len(msg):
						if msg[k] in number_chars:
							msg = msg[:k] + msg[(k+1):]
						else:
							k += 1
				j += 1

			
			# for 8ball, remove from msg any string values indicated by ~8ball~
			if '~8ball~' in current_test_line:
				# remove 8ball value
				for answer in eightball:
					if answer in msg:
						msg = msg.replace(answer, '')
				# remove '~8ball~' from test line
				current_test_line = current_test_line.replace('~8ball~', '')

			# for weather, remove from msg an arbitrary string indicated by {str}
			# currently handles a single instance of {str} per test line
			temp_test_line = ''
			msg_lines = msg.splitlines()
			temp_test_lines = current_test_line.splitlines()
			j = 0
			while j < len(temp_test_lines):
				if '{str}' in temp_test_lines[j]:
					str_ind = temp_test_lines[j].find('{str}')
					temp_test_lines[j] = temp_test_lines[j].replace('{str}', '')
					reduced_len = len(temp_test_lines[j])
					msg_lines[j] = msg_lines[j][:str_ind] + msg_lines[j][(len(msg) - reduced_len + str_ind):]
				j += 1
			# reassemble current_test_line and msg after removing any {str}
			msg = ''
			current_test_line = ''
			for line in msg_lines:
				msg += line
			for line in temp_test_lines:
				current_test_line += line
			
			# TEST #1: LINE NUMBER COMPARISON
			try:
				self.assertEqual(len(msg.splitlines()), len(current_test_line.splitlines()))
			except:
				print('different number of lines')
				print(msg.splitlines())
				print('vs')
				print(current_test_line.splitlines())
			# TEST #2: LINE-BY-LINE COMPARISON OF PROCESSED MESSAGE VS TEST LINE
			# (equality should hold after processing)
			try:
				j = 0
				# line by line comparison
				while j < len(current_test_line.splitlines()):
					self.assertEqual(msg.splitlines()[j], current_test_line.splitlines()[j])
					j += 1
			except:
				print('lines not equal')
				print('{}'.format(msg.splitlines()[j]))
				print('vs')
				print('{}'.format(current_test_line.splitlines()[j]))

			increment_ind(line_index)
			await asyncio.sleep(1)
			# close bot if all lines have been tested:
			if line_index is len(test_lines):
				print("test complete")
				await client.close()
				return
			# otherwise reply with next test message
			else:
				await asyncio.sleep(2)
				await client.send_message(message.channel, test_lines[line_index])    
			


		client.run(token)


if __name__ == '__main__':
	unittest.main()




