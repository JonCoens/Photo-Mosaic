import os.path
import sys
import glob
import extract_meta
import mosaic
import pickle

db_filename = 'db.p'

if not os.path.isfile(db_filename):
	photos = glob.glob("photos/*.png")
	db = [(photo, extract_meta.extractPhotoInfo(photo)) for photo in photos]
	db_file = open(db_filename, 'wb')
	pickle.dump(db, db_file)
else:
	db_file = open(db_filename, 'r')
	db = pickle.load(db_file)
		
print "Have " + str(len(db)) + " samples"

photos = glob.glob("*.png")

result = mosaic.createMosaic(db, photos[0])
result.show()
result.save('result-Cartesian.png', 'PNG')


result = mosaic.createMosaicHex(db, photos[0])
result.show()
result.save('result-Hex.png', 'PNG')