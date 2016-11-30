# Aradiabot image glitching functions.
# Transcribed over from my 'fastglitch' repository.
from io import BytesIO, StringIO
import random, sys, PIL.Image, PIL.ImageChops, PIL.ImageDraw, os
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
import asyncio

def genImg(fname):
	img = PIL.Image.open(fname)
	img = img.convert('RGBA')
	proto1 = RandomByteAddition(img, random.randint(1,16))
	proto2 = RGBOffset(proto1, random.randint(1,64))
	proto3 = PixelOffset(proto2, random.randint(1,512))
	proto4 = Artifact(proto3, random.randint(1,64))
	proto5 = RowSlice(proto4, random.randint(1,32))
	proto6 = Noise(proto5, random.randint(25000,50000))
	p = proto6.convert('RGB')
	p.save('new' + fname + '.png')
	proto1.close()
	proto2.close()
	proto3.close()
	proto4.close()
	proto5.close()
	proto6.close()

def RandomByteAddition(image, seed):
	bytesBroken = False
	bytesobj = BytesIO()
	image.save(bytesobj, 'jpeg')
	iter = seed
	bytesobj.seek(1024)
	if seed > 0:
		for x in range(0, iter):
			bytes2 = bytesobj
			bytesobj.seek(random.randint(0, 32), 1)
			byte = random.choice(chars)
			bytesobj.write(bytes(byte, 'utf-8'))
			try:
				PIL.Image.open(bytesobj)
			except:
				bytesBroken = True
				break

	if bytesBroken == True:
		bytes2.seek(0)
		new_img = PIL.Image.open(bytes2)
	else:
		bytesobj.seek(0)
		new_img = PIL.Image.open(bytesobj)
	return new_img

def RGBOffset(image, distance):
	distance = distance * 30
	r, g, b = image.split()
	r = PIL.ImageChops.offset(r, distance * -1, 0)
	b = PIL.ImageChops.offset(b, distance, 0)
	new_img = PIL.Image.merge('RGB', (r, g, b))
	return new_img

def PixelOffset(image, distance):
	new_img = PIL.ImageChops.offset(image, distance)
	return new_img

def RowSlice(image, sliceamount):
	cps = 0
	new_img = image
	for x in range(sliceamount):
		upbound = cps
		downbound = upbound + random.randint(16, 128)
		if downbound > image.height:
			break
		box = (0,
		 upbound,
		 new_img.width,
		 downbound)
		reigon = new_img.crop(box)
		distance = random.randint(-128, 128)
		reigon = PIL.ImageChops.offset(reigon, distance, 0)
		new_img.paste(reigon, box)
		reigon.close()
		cps = downbound

		return new_img

def Artifact(image, screwamount):
	tnspimg = image.convert('RGBA')
	base = PIL.Image.new('RGBA', tnspimg.size, (255, 255, 255, 0))
	rows = PIL.ImageDraw.Draw(base)
	cps = 0
	for x in range(screwamount):
		leftbound = cps
		rightbound = leftbound + random.randint(32, 128)
		if rightbound > image.width:
			break
		y1 = random.randint(0, image.height - int(round(image.height / 2.0, 0)))
		x1 = random.randint(leftbound, rightbound - 1)
		y2 = random.randint(y1, image.height)
		x2 = rightbound
		color = (random.randint(0, 255),
		 random.randint(0, 255),
		 random.randint(0, 255),
		 random.randint(64, 200))
		rows.rectangle((x1,
		 y1,
		 x2,
		 y2), fill=color)
		cps = rightbound

	new_img = PIL.Image.alpha_composite(tnspimg, base)
	return new_img







def Noise(image, pixels):
	for x in range(1, pixels):
		image.putpixel((random.randint(1, image.width - 1), random.randint(1, image.height - 1)), (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))

	new_img = image
	return new_img
