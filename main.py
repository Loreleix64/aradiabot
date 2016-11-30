# Aradiabot main file + misc functions.
import discord
import asyncio
import random
import tweepy
import json
import booru
import os
import re
import glitch
import requests
import image

#Please provide your own twitter api keys if you want to make use of the tweeting function.
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

tapi = tweepy.API(auth)

client = discord.Client()

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

# Most of the things in the loot tables were inside jokes.
# Feel free to feel these in yourself.
lootPrefix=["Ancient"]
lootItem=["Sword"]
lootSuffix=["of Fire"]
def lootgen():
	return str(random.choice(lootPrefix) + " " + random.choice(lootItem) + " " + random.choice(lootSuffix))

async def tweet(msg, message):
	r = re.search(r'<@(.*)>', msg)
	r2 = re.search(r'<@!(.*)>', msg)
	if r or r2:
		for group in r.groups():
			for u in message.channel.server.members:
				if str(group) == str(u.id):
					msg = re.sub(r'<@(.*)>', "@" + str(u.name), msg)

		for group in r2.groups():
                        for u in message.channel.server.members:
                                if str(group) == str(u.id):
                                        msg = re.sub(r'<@(.*)>', "@" + str(u.name), msg)
	imsg = False
	print (message.attachments)
	if len(message.attachments) == 1:
		j = message.attachments[0]
		if j["filename"].lower().endswith('.jpg') or j["filename"].lower().endswith('.jpeg') or j["filename"].lower().endswith('.png') or j["filename"].lower().endswith('.gif'):
			import urllib.request
			fname = j["filename"]
			req = urllib.request.Request(j["url"], None, headers)
			html = urllib.request.urlopen(req).read()
			with open(fname, 'wb') as f:
				f.write(html)


			imsg = True

	try: 
		if len(msg) > 140:
			msg = msg[:140]
			if imsg:
				tapi.update_with_media(fname, status=msg)
				os.remove(fname)
			else:
				tapi.update_status(msg)
		else:
			if imsg:
				tapi.update_with_media(fname, status=msg)
				os.remove(fname)
			else:
				tapi.update_status(msg)
		return "Your message has been sent."
	except tweepy.TweepError as e: 
		print(json.loads(e.response.text))
		return json.loads(e.response.text)['errors'][0]['message']

async def loot():
	return "You obtain the \'" + lootgen() + "\'! Beep boop."

async def joke():
	table = requests.get("http://tambal.azurewebsites.net/joke/random").json()
	return str(table["joke"])
	
async def imgglitch(message):
	if len(message.attachments) == 1:
		j = message.attachments[0]
		print("Validating!")
		if j["filename"].lower().endswith('.jpg') or j["filename"].lower().endswith('.jpeg') or j["filename"].lower().endswith('.png') or j["filename"].lower().endswith('.gif'):
			print("Downloading!")
			import urllib.request
			fname = j["filename"]
			req = urllib.request.Request(j["url"], None, headers)
			html = urllib.request.urlopen(req).read()
			with open(fname, 'wb') as f:
				f.write(html)
			print("Glitching!" + fname)	
			glitch.genImg(fname)
			print("Sending!")
			await client.send_file(message.channel,'new' + fname + '.png')
			print("Removing!")
			os.remove('new' + fname + '.png')
			os.remove(fname)
	else:
		client.send_message(message.channel, "You did not upload an image, or it is corrupt!")

async def liquid(message):
	if len(message.attachments) == 1:
		j = message.attachments[0]
		print("Validating!")
		if j["filename"].lower().endswith('.jpg') or j["filename"].lower().endswith('.jpeg') or j["filename"].lower().endswith('.png') or j["filename"].lower().endswith('.gif'):
			print("Downloading!")
			import urllib.request
			fname = j["filename"]
			req = urllib.request.Request(j["url"], None, headers)
			html = urllib.request.urlopen(req).read()
			with open(fname, 'wb') as f:
				f.write(html)
			print("Glitching!" + fname)	
			image.liquid(fname)
			print("Sending!")
			await client.send_file(message.channel,'liqnew' + fname)
			print("Removing!")
			os.remove('liqnew' + fname)
			os.remove(fname)
	else:
		client.send_message(message.channel, "You did not upload an image, or it is corrupt!")

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	#Booru commands, listed in booru.py
	if message.content.startswith('$mom'):
		result = await booru.mom()
		await client.send_message(message.channel, result)
	elif message.content.startswith('$e621'):
		result = await booru.e621(message.content[5:])
		await client.send_message(message.channel, result)
	elif message.content.startswith('$danbooru'):
		result = await booru.danbooru(message.content[9:])
		await client.send_message(message.channel, result)
	elif message.content.startswith('$derpibooru'):
		result = await booru.derpibooru(message.content[11:])
		await client.send_message(message.channel, result)
	elif message.content.startswith('$r34'):
		result = await booru.rule34(message.content[4:])
		await client.send_message(message.channel, result)
		
	#Image handling functions, listed in glitch.py and image.py
	elif message.content.startswith('$glitch'):
		await imgglitch(message)
	elif message.content.startswith('$liquid'):
		await liquid(message)

	#Miscellanious commands.
	elif message.content.startswith('$joke'):
		joked = await joke()
		await client.send_message(message.channel, joked)
	elif message.content.startswith('$loot'):
		pickedup = await loot()
		await client.send_message(message.channel, pickedup)
	elif message.content.startswith('$tweet'):
		returnstatus = await tweet(message.content[6:], message)
		await client.send_message(message.channel, returnstatus)
	elif message.content.startswith('$help'):
		await client.send_message(message.channel, help)
client.run("Here's where your discord client id goes")

