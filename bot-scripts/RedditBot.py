from discord.ext import commands
import praw
import random


BOT_PREFIX = ("!")
TOKEN = 'NTAxNjAzMzQyMTUwMjcwOTc5.DrGNDQ.sP4_kl0CJM-6nTq3KL8Qf2cMmvI'
client = commands.Bot(command_prefix = BOT_PREFIX)
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
    posts = myreddit.subreddit(sub).hot(limit = 16) # Uses 16 because if old post is pulled again go to next, ( no out of index if rand = 15)
    random_post_number = random.randint(0, 15)
    for i in range(0, random_post_number - 1):
        post = next(x for x in posts if not x.stickied)
    if oldpost == post.url:
        post = next(x for x in posts if not x.stickied)
    else:
        oldpost = post.url
    await client.say(post.title)
    await client.say(post.url)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)