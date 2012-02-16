import os
import sys
import colormath_fast
from colormath_fast.color_objects import RGBColor,LabColor

class Bucket:
	def __init__(self, r, g, b, count=1):
		self.col = RGBColor(round(r),round(g),round(b)).convert_to('lab')
		self.rgb_aves = (float(r), float(g), float(b))
		self.count = count
		self.proportion = 1
	def __repr__(self):
		return "(" + repr(self.rgb_aves[0]) + "," + repr(self.rgb_aves[1]) + "," + repr(self.rgb_aves[2]) + "): " + repr(self.count)
		
	def getRGBA(self, a):
		return (round(self.rgb_aves[0]), round(self.rgb_aves[1]), round(self.rgb_aves[2]), a)
		
def mergeWith(a, b):
	if a is None:
		return b
	tot = float(a.count + b.count)
	r = (a.count/tot)*a.rgb_aves[0] + (b.count/tot)*b.rgb_aves[0]
	g = (a.count/tot)*a.rgb_aves[1] + (b.count/tot)*b.rgb_aves[1]
	b = (a.count/tot)*a.rgb_aves[2] + (b.count/tot)*b.rgb_aves[2]
	return Bucket(r, g, b, tot)