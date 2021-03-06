# This file was originally copied from one of my other projects, 
# Project-Pixel, that turns images into pixel art
# Author: jormungandr

from re import X
from PIL import Image, ImageEnhance
import math
import cv2
from cv2 import COLOR_BGR2RGB

class ImageP:
	
	def __init__(self, filename,x,y):
		filename = cv2.cvtColor(filename,COLOR_BGR2RGB)
		self.x = x
		self.y = y
		self.o_image = Image.fromarray(filename)
		#self.o_image = Image.open(self.original)
		#enhancer = ImageEnhance.Contrast(self.o_image)
		factor = 1.25
		#self.o_image = enhancer.enhance(factor)
		#enhancer = ImageEnhance.Sharpness(self.o_image)
		factor = 2
		#self.o_image = enhancer.enhance(factor)
		#self.o_pixels = self.o_image.load()
		self.width, self.height = self.o_image.size
		self.r_image = self.o_image.resize((self.x,self.y),0)
		self.o_pixels = self.r_image.load()
		self.rgb_vals = []

	def save_modified_relative(self, filename):
		self.new_image.save("../{}.jpg".format(filename))

	def get_average(self, index0, index1, index2, index3):
		num_pixels = 0.0
		r_sum = 0.0
		g_sum = 0.0
		b_sum = 0.0
		for i in range(index0, index1):
			for j in range(index2, index3):
				triple = self.o_pixels[i,j]
				r_sum += triple[0]
				g_sum += triple[1]
				b_sum += triple[2]
				num_pixels += 1.0
		averages = (0,0,0)
		r_avg = math.floor((r_sum/num_pixels)+.5)
		g_avg = math.floor((g_sum/num_pixels)+.5)
		b_avg = math.floor((b_sum/num_pixels)+.5)
		averages = (r_avg,g_avg,b_avg)
		return averages

	def pixel_reduce(self, ppc_x, ppc_y):
		self.rgb_vals = []
		averages = ()
		for x in range(0,self.width,ppc_x):
			column = []
			for y in range(0,self.height,ppc_y):
				averages = self.get_average(x,min(x+ppc_x,self.width),y,min(y+ppc_y,self.height))
				column.append(averages)
			self.rgb_vals.append(column)

	def get_pixels(self):
		self.rgb_vals = []
		for x in range(self.x):
			column = []
			for y in range(self.y):
				column.append(self.o_pixels[x,y])
			self.rgb_vals.append(column)
