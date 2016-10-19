#Look at all these fucking imports. Install all this shit.
import discord
import asyncio
import requests
import random
import tweepy
import datetime
import re, string
import json

#HOW TO USE:
#Messaging "Aradiabot, [command]" or "[command], Aradiabot." will trigger a command.
#Commands are:
#"Aradiabot, search [booru] for [tags]" Boorus supported are derpibooru, e621, and danbooru. Format the tags as if you were using the site search.
#"Aradiabot, show me the mom" returns a picture of Ran Yakumo. Don't ask why.
#"Aradiabot, tell me about Chuck Norris" returns a Chuck Norris joke. Yeah, yeah, dead meme, I get it.
#"Aradiabot, tell me a joke" returns a joke. Sometimes html escape tags get in here. I'm working on it.
#"Aradiabot, pick up some loot" returns a randomly generated magical item. Fill the item names yourself in lootPrefix[], lootItem[], and lootSuffix[].
#"Aradiabot, tweet [tweet]" tweets something on a twitter account. This cuts out punctuaton. I'm working on that, too.
#Thank Aradiabot every so often. She works hard.

#Special thanks to @NO_BOOT_DEVICE on twitter for making this code much neater than it was. It used to be a nightmare.

########VARIABLES AND OTHER SHIT THAT NEEDS TO RUN BEFORE THE MAIN LOOP########

########PLEASE PUT TWEEPY STUFF HERE, THIS NEEDS TO BE SET BEFORE THE BOT CAN RUN########
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

tapi = tweepy.API(auth)

client = discord.Client()

########I CLEARED OUT THE LOOT TABLE BECAUSE MOST OF IT WAS INSIDE JOKES. ADD WHATEVER HERE########
lootPrefix=["Ancient", ]
lootItem=["Sword", ]
lootSuffix=["of Fire", ]


########PUT A DERPIBOORU API KEY HERE. THIS NEEDS TO BE SET BEFORE THE BOT CAN RUN.########
dpapik=""

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

########PUT YOUR DISCORD APP TOKEN HERE. THIS NEEDS TO BE SET BEFORE THE BOT CAN RUN.########
discordtoken = ""

########END VARIABLES########




########FUNCTIONS########

########THIS ONE SPECIFICALLY SEARCHES FOR RAN YAKUMO ON DANBOORU. DON'T ASK WHY IT'S HERE.########
def mom():
	response = requests.get("https://danbooru.donmai.us/posts.json?tags=yakumo_ran+1girl&page=" + str(random.randint(1,200)) + "&limit = 20")
	table = response.json()
	return "https://danbooru.donmai.us/" + str(table[random.randint(0,19)]["file_url"])

def search(site, tags):
	if site in sites:
		if 'func' in sites[site]:
			return sites[site]['func'](tags)
		else:
			if not any(tag.startswith('rating:') for tag in tags.split(' ')): tags = tags + ' rating:s' # safe by default
			response = requests.get((sites[site]['url']).rstrip(), params={**sites[site]['params'], sites[site]['tags']:tags}, headers=headers).json()
			try:
				return sites[site]['prefix'] + str(random.choice(response)["file_url"])
			except:
				return None
	else: 
		return None
	
def derpibooru(tags):
	response = requests.get("https://derpibooru.org/search.json", params={'key':dpapik,'q':tags}, headers=headers).json()
	try:
		return "https:" + str(random.choice(response["search"])["image"])
	except:
		return None
	
def loot():
	return str(random.choice(lootPrefix) + " " + random.choice(lootItem) + " " + random.choice(lootSuffix))

sites = {
          'e621': {'url': 'https://e621.net/post/index.json', 'tags': 'tags', 'prefix': '', 'params': {'limit':320}},
          'danbooru': {'url': 'https://danbooru.donmai.us/posts.json', 'tags': 'tags', 'prefix':"https://danbooru.donmai.us/", 'params': {'limit':200}},
          'derpibooru': {'func': derpibooru}
        }

rc = lambda x: re.compile(x,re.I)
########END FUNCTIONS########

########COMMANDS########
async def cmdmom(cmd, match, message):
	url = mom()
	await client.send_message(message.channel, "Here is your mom. Beep boop. " + url)
		
async def cmdsearch(cmd, match, message):
	site = match.group(1)
	tags = match.group(2)
	result = search(site, tags)
	if result == None:
		await client.send_message(message.channel, "There weren't any results! Beep boop.")
	else:
		await client.send_message(message.channel, "I thought this one looked nice. Beep boop. " + result)
    
async def cmdtweet(cmd, match, message):
	tweet = match.group(1)
	try: 
		if len(tweet) > 140:
			tweet = tweet[:140]
			tapi.update_status(tweet)
		else:
			tapi.update_status(tweet)
			await client.send_message(message.channel, "Your message has been sent. Beep boop.")
	except tweepy.TweepError as e: 
		print(json.loads(e.response.text))
		await client.send_message(message.channel, json.loads(e.response.text)['errors'][0]['message'] + " Beep boop.")

async def cmdloot(cmd, match, message):
	await client.send_message(message.channel, "You obtain the \'" + loot() + "\'! Beep boop.")

async def cmdjoke(cmd, match, message):
	table = requests.get("http://tambal.azurewebsites.net/joke/random").json()
	await client.send_message(message.channel, str(table["joke"]))

async def cmddeadmeme(cmd, match, message):
	table = requests.get("https://api.icndb.com/jokes/random").json()
	await client.send_message(message.channel, str(table["value"]["joke"]))

async def cmdthank(cmd, match, message):
	await client.send_message(message.channel, "You're very welcome. Beep boop.")

########THE COMMAND LIST MAKES THIS PRETTY MODULAR. ADD AND REMOVE STUFF AS YOU PLEASE.########
cmdlist = (
           {'regex': rc('show me the mom'), 'func': cmdmom},
           {'regex': rc('search (\w+) for (.+)'), 'func': cmdsearch},
           {'regex': rc('tweet (.+)'), 'func': cmdtweet},
           {'regex': rc('pick up some loot'), 'func': cmdloot},
           {'regex': rc('tell me a joke'), 'func': cmdjoke},
           {'regex': rc('tell me about chuck norris'), 'func': cmddeadmeme},
           {'regex': rc('thank you'), 'func': cmdthank}
          )

async def findcmd(cmdstr, message):
	scmd = cmdstr.strip(string.punctuation)
#	print(scmd)
	for cmd in cmdlist: 
		match = cmd['regex'].fullmatch(scmd)
		if match:
			await cmd['func'](scmd, match, message)
########END COMMANDS########



########CLIENT EVENTS########
@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	if message.content.startswith('Aradiabot, '):
		cmdstr = message.content[len('Aradiabot, '):]
#		print(cmdstr)
		await findcmd(cmdstr, message)
	elif message.content.endswith(', Aradiabot.'):
		cmdstr = message.content[:-len(', Aradiabot.')]
#		print(cmdstr)
		await findcmd(cmdstr, message)
		
########END CLIENT EVENTS########		
client.run(discordtoken)
