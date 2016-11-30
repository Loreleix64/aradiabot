# Aradiabot functions for searching through various image sharing websites.
import requests
import random
import subprocess
import json
import asyncio
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
async def mom():
	response = requests.get("https://danbooru.donmai.us/posts.json?tags=yakumo_ran+1girl&page=" + str(random.randint(1,200)) + "&limit = 20")
	table = response.json()
	return "https://danbooru.donmai.us/" + str(table[random.randint(0,19)]["file_url"])
	
async def e621(tags):
	tagsa = tags.split(" ")
	tags = ""
	for tag in tagsa:
		tags = tags + tag + "+"
	response = requests.get("https://e621.net/post/index.json?tags=" + tags + "&limit=320", headers=headers).json()
	try:
		return random.choice(response)["file_url"]
	except:
		return "No results!"

async def danbooru(tags):
	tagsa = tags.split(" ")
	tags = ""
	for tag in tagsa:
		tags = tags + tag + "+"
	response = requests.get("https://danbooru.donmai.us/posts.json?tags=" + tags + "&limit=200", headers=headers).json()
	try:
		return "https://danbooru.donmai.us/" + random.choice(response)["file_url"]
	except:
		return "No results!"
	
async def derpibooru(tags):
	response = requests.get("https://derpibooru.org/search.json?q=" + tags, params={'key':#Please supply your own derpibooru API key!}, headers=headers).json()
	try:
		return "https:" + random.choice(response["search"])["image"]
	except:
		return "No results!"

async def rule34(tags):
	tagsa = tags.split(" ")
	args = ['python3.5', 'r34.py'] # This worked a lot better in it's own file.
	for tag in tagsa:
		args.append(tag)
	p = subprocess.Popen(args, stdout=subprocess.PIPE)
	text = p.stdout.read().decode()
	print (text)
	if text.strip() == "0":
		return "No results!"
	else:
		return text
