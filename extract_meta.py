from color_base import Bucket
import Image
import math

def mergeWith(a, b):
	if a is None:
		return b
	tot = float(a.count + b.count)
	r = (a.count/tot)*a.rgb_aves[0] + (b.count/tot)*b.rgb_aves[0]
	g = (a.count/tot)*a.rgb_aves[1] + (b.count/tot)*b.rgb_aves[1]
	b = (a.count/tot)*a.rgb_aves[2] + (b.count/tot)*b.rgb_aves[2]
	return Bucket(r, g, b, tot)

def cutoff((dist, bucket)):
	return dist <= 6

def topPercent((howmany, bucket)):
	return bucket.count / float(max(howmany,1)) >= 0.1

def bucketize(r, g, b, buckets):
	nb = Bucket(r, g, b)
	matches = filter(cutoff, [(nb.col.delta_e(bucket.col), bucket) for bucket in buckets])
	numMatches = len(matches)
	if numMatches == 0:
		buckets.append(nb)
	elif numMatches == 1:
		ind = buckets.index(matches[0][1])
		buckets[ind].count += 1
	else:
		for (diff,bucket) in matches:
			buckets.remove(bucket)
		b = reduce(mergeWith, [bucket for (diff,bucket) in matches], nb)
		buckets.append(b)
		
		
def extractPhotoInfo(photo):
	print "\n" + str(photo)
	im = Image.open(photo)
	pix = im.load()
	size = im.size

	buckets = []
	howmany = 0
	for x in range(0, size[0], 4):
		for y in range(0, size[1], 4):
			if pix[x,y][3] != 0:
				howmany += 1
				if howmany % 1000 == 0:
					print howmany
				bucketize(pix[x,y][0], pix[x,y][1], pix[x,y][2], buckets)
	buckets = sorted(buckets, key=lambda bucket: bucket.count, reverse=True)

	print "\n" + str(howmany)
	print len(buckets)

	maxDiff, minDiff, average, howmany = 0, 1000, 0, 0
	for bucketA in buckets:
		for bucketB in buckets:
			if bucketA == bucketB:
				continue
			diff = bucketA.col.delta_e(bucketB.col, 'cie2000')
			if diff > maxDiff:
				maxDiff = diff
			if diff < minDiff:
				minDiff = diff
			howmany += 1
			average += diff
	print "maxDiff=" + str(maxDiff)
	print "minDiff=" + str(minDiff)
	print "howmany=" + str(howmany)
	print "average=" + str (average/max(howmany,1))

	bestBuckets = [bucket for (count,bucket) in filter(topPercent, [(howmany, bucket)  for bucket in buckets])]

#	for x in range(size[0]):
#		if x % 50 == 0:
#			print x / float(size[0])
#		for y in range(size[1]):
#			(r,g,b,a) = im.getpixel((x,y))
#			if a != 0:
#				pix = Bucket(r,g,b)
#				sortedBuckets = sorted([(pix.col.delta_e(bucket.col), bucket) for bucket in bestBuckets])
#				bestBucket = sortedBuckets[0][1]
#				im.putpixel((x,y), bestBucket.getRGBA(a))

#	im.show()
	
	return bestBuckets
	