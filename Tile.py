
from tkinter import *
from utils import *
import random

from Strategy import *
from PIL import Image, ImageFilter, ImageTk
import itertools
import colorsys

class Tile:


	def __init__(self, parent, tile_index, root):

		self.width = 0
		self.height = 0

		self.parent = parent
		self.tile_index = tile_index
		self.root = root

		self.strategy = Strategy()
		self.img = None

		self.draw(init=True)

		return

	def draw(self, init=False):

		if init:

			bg = "black" #random.choice(["blue", "green", "white", "red", "black"])
			self.canvas = Canvas(self.root, width = self.width, height = self.height, bg=bg, highlightthickness=2, highlightbackground="#222222")
			self.canvas.bind('<Button-1>', self.onClick)
			self.canvas.bind('<Button-3>', self.onRightClick)

			self.img = self.getStrategyImage()

			self.resize()

	def setWidth(self, new_width):
		self.width = new_width

	def setHeight(self, new_height):
		self.height = new_height


	def reset(self):
		self.canvas.configure(highlightbackground="#111111")


	def onClick(self, event=[]):
		print("you clicked on:", self.tile_index)

		self.parent.addProgenitor(self.tile_index)

		self.canvas.configure(highlightbackground="white")

	def onRightClick(self, event=[]):
		print("you right clicked on:", self.tile_index)

		self.parent.regenerate(self.tile_index)


	def setStrategy(self, new_strategy):
		self.strategy = new_strategy

	def recalculateImage(self):
		self.img = self.getStrategyImage()

		self.resize()


	def getStrategyImage(self):

		random_img = makeRandomTile(self.strategy, size=self.parent.img_size, num_steps=self.parent.steps, has_edge=self.parent.has_edge)
		#random_img = random_img.resize((200, 200), Image.NEAREST)

		return random_img
	
	def resize(self, event=[]):
		

		self.width = int(self.width)
		self.height= int(self.height)

		self.tk_image = ImageTk.PhotoImage(self.img.resize((max(1, self.width), max(1, self.height)))) #, Image.NEAREST))
		self.tk_image_index = self.canvas.create_image((self.width//2, self.height//2), image=self.tk_image)



def makeRandomTile(strategy, size, num_steps, has_edge=False):

	img = Image.new('RGB', size, "black")
	pix = img.load()


	# x y pixel locations
	cur_x = size[0]//2 #random.randint(0, size[0]-1)
	cur_y = size[1]//2 #random.randint(0, size[1]-1)

	consec_invalid_moves = 0

	for _ in range(num_steps):

		if consec_invalid_moves > 10:
			continue
			#cur_x = random.randint(0, size[0]-1)
			#cur_y = random.randint(0, size[1]-1)
			#consec_invalid_moves = 0

		# get neighbor colours
		neighbor_colours = []
		for o_x, o_y in itertools.product([-1, 0, 1], [-1, 0, 1]):
			try:
				#print("in bounds")
				if has_edge:
					colour = pix[cur_y+o_y,cur_x+o_x]
				else:
					colour = pix[(cur_y+o_y)%size[1],(cur_x+o_x)%size[0]]
			except:
				#print("out of bounds")
				colour = (0, 0, 0)

				consec_invalid_moves += 1

			h, s, v = colorsys.rgb_to_hsv(*[val/255. for val in colour])


			neighbor_colours.append((h, s, v))


		position = (2.*cur_x/size[0] - 1., 2.*cur_y/size[1] - 1.)

		(dx, dy), (dh, ds, dv) = strategy.getAction(neighbor_colours, position)

		cur_rgb = pix[cur_y,cur_x]
		cur_h, cur_s, cur_v = colorsys.rgb_to_hsv(*[val/255. for val in cur_rgb])

		new_h = (cur_h + dh)%1
		new_s = clip(0, 1, cur_s+ds)
		new_v = clip(0, 1, cur_v+dv)

		# convert back to rgb
		c = (new_h, new_s, new_v)


		r, g, b = colorsys.hsv_to_rgb(*c)
		r = int(r*255.)
		g = int(g*255.)
		b = int(b*255.)

		pix[cur_y,cur_x] = (r, g, b)

		# apply movement

		if has_edge:
			cur_x = clip(0, size[0]-1, cur_x+dx)
			cur_y = clip(0, size[1]-1, cur_y+dy)
		else:
			cur_x = (cur_x+dx) % size[0] #clip(0, size[0]-1, cur_x+dx)
			cur_y = (cur_y+dy) % size[1] #clip(0, size[1]-1, cur_y+dy)




	return img