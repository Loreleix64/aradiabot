# Aradiabot image functions.
# Still under construction!
# I hope to add more soon.
from wand.image import Image
import random

def liquid(imagename):
	x = random.uniform(0.8,5.0)
	y = random.uniform(0.4,0.9)
	with Image(filename=imagename) as img:
		img.resize(round(img.width / 2), round(img.height / 2))
		oldx = img.width
		oldy = img.height
		img.liquid_rescale(round(img.width * x), round(img.height * y))
		img.liquid_rescale(oldx, oldy)
		img.save(filename='liqnew' + imagename)
				
