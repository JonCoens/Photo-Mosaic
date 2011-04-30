from color_base import Bucket
import Image
import collections

def createThumbnails(d):
	thumbs = collections.defaultdict(str)
	for name in d:
		im = Image.open(name)
		th = im.resize((50, 50))
		thumbs[name] = th
	return thumbs

def generateImage(labels, thumbs):
	thumbSize = (50, 50)
	labelWidth = len(labels)
	im = Image.new("RGBA", (thumbSize[0]*labelWidth, thumbSize[1]*labelWidth))
	
	for x in range(labelWidth):
		for y in range(len(labels[x])):
			box = (x * thumbSize[0], y * thumbSize[1])
			im.paste(thumbs[labels[x][y]], box)
			
	return im

def createMosaic(db, photo_filename):
	im = Image.open(photo_filename)
	pix = im.load()
	size = im.size
	print size
	
	labels = [[None for x in range(size[1])] for y in range(size[0])]
	d = collections.defaultdict(int)
	
	for x in range(size[0]):
		if x % 50 == 0:
			print x / float(size[0])
		for y in range(size[1]):
			(r,g,b) = im.getpixel((x,y))
			pix = Bucket(r,g,b)
			orderedPhotos = sorted([(pix.col.delta_e(sample[1][0].col), sample) for sample in db])
			bestSample = orderedPhotos[0][1]
			d[bestSample[0]] += 1
			labels[x][y] = bestSample[0]	
	
	thumbs = createThumbnails(d)
	result = generateImage(labels, thumbs)
	return result