import colormath
from colormath.color_objects import RGBColor,LabColor

class Bucket:
	def __init__(self, r, g, b, count=1):
		self.col = RGBColor(round(r),round(g),round(b)).convert_to('lab')
		self.rgb_aves = (float(r), float(g), float(b))
		self.count = count
	def __repr__(self):
		return "(" + repr(self.rgb_aves[0]) + "," + repr(self.rgb_aves[1]) + "," + repr(self.rgb_aves[2]) + "): " + repr(self.count)
		
	def getRGBA(self, a):
		return (round(self.rgb_aves[0]), round(self.rgb_aves[1]), round(self.rgb_aves[2]), a)