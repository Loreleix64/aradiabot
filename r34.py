# Aradiabot function for searching rule34.xxx
# As they don't have an API, this was easier to put in it's own file so I could organize everything.

import requests
from html.parser import HTMLParser
import random
import sys
counter = [10,9,8,7,6,5,4,3,2,1]
images = []

class booruparser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if tag == 'a':
			if any('id' in pairs for pairs in attrs):
				try:
					images.append(str(attrs[1][1]))
				except:
					pass
				
class imageparser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		if ('id', 'image') in attrs:
			print("http:" + attrs[2][1])
			
			
parser = booruparser()
imgparser = imageparser()

tags = ""

for arg in sys.argv:
	if arg == sys.argv[0]:
		pass
	else:
		tags = tags + arg + "+"		

count = 0
while len(images) < 1:
	if count < 10:
		parser.feed(requests.get('http://rule34.xxx/index.php?page=post&s=list&tags=' + tags + '&pid=' + str(counter[count])).text)
		count = count + 1
	else:
		break
	
if count != 10:
	image = requests.get('http://rule34.xxx/' + random.choice(images)).text
	imgparser.feed(image)
else:
	print("0")
