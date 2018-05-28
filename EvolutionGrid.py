
from tkinter import *
import pyscreenshot as ImageGrab
import time
import numpy as np

from Tile import *
from Strategy import *

class EvolutionGrid:

	def __init__(self, pop_grid_size=(4, 4), num_steps=500, tile_pix_size=(100, 100), window_size=(1000, 1000)):

		self.pop_grid_size = pop_grid_size

		self.pop_num = self.pop_grid_size[0]*self.pop_grid_size[1]

		self.root = Tk()
		self.window_width, self.window_height = window_size

		self.tiles = []

		self.steps = num_steps
		self.img_size = tile_pix_size
		self.has_edge = False

		self.draw(init=True)

		self.progenitors = []

		self.root.mainloop()

		return

	def draw(self, init=False):

		if init:

			self.root.resizable(False, False)
			self.root.wm_title("EvolutionGrid")
			self.root.geometry("%dx%d" % (self.window_width, self.window_height))
			self.root.configure(background="white")
			self.root.bind("<Configure>", self.resize)
			self.root.bind('<Control-Key-s>', self.save)
			
			self.root.bind("<Key>", self.handleKey)

			self.resize()

			# draw icons
			for i in range(self.pop_num):
				T = Tile(parent=self, tile_index=i, root=self.root)
				self.tiles.append(T)

			self.resize()

		self.root.update()

	def resize(self, event=[]):

		self.window_width=self.root.winfo_width()
		self.window_height=self.root.winfo_height()


		if len(self.tiles) == 0: return

		sWidth = self.window_width / self.pop_grid_size[0]
		sHeight = self.window_height / self.pop_grid_size[1]

		for i in range(len(self.tiles)):
			curX = (i % self.pop_grid_size[0])*sWidth
			curY = int(i/self.pop_grid_size[0])*sHeight

			S = self.tiles[i]
			S.canvas.place(x=curX, y=curY, width=sWidth, height=sHeight)

			S.setWidth(sWidth)
			S.setHeight(sHeight)
			S.resize()

	def handleKey(self, event=[]):

		print(str(event.keysym))

		if event.keysym == "Return":
			self.nextGeneration()

		elif event.keysym == "Up":
			print("Increasing timesteps")

			self.steps += 250
			print(self.steps)
		
		elif event.keysym == "Down":
			print("Decreasing timesteps")

			self.steps -= 250
			self.steps = max(250, self.steps)

			print(self.steps)
		
		elif event.keysym == "Left":
			print("Decreasing img_size")

			size = self.img_size[0]
			size = max(25, size - 25)
			self.img_size = (size, size)
			print(self.img_size)
		
		elif event.keysym == "Right":
			print("Increasing img_size")

			size = self.img_size[0]
			size = size + 25
			self.img_size = (size, size)
			print(self.img_size)
		
		elif event.keysym == "e":
			print("Toggling edge")
			self.has_edge = not self.has_edge
			print("\t", self.has_edge)


		return

	def addProgenitor(self, index):

		self.progenitors.append(index)


	def regenerate(self, index):

		#choices = [t.strategy for i, t in enumerate(self.tiles) if i != index]

		new_strategy_weights = []

		for _ in range(1):
			parent_A = self.tiles[index].strategy
			parent_B = self.tiles[index].strategy

			child_strategy_weights = reproduceStrategies(parent_A=parent_A, parent_B=parent_B, mutation_rate=0.025)

			new_strategy_weights.append(child_strategy_weights)


		s = new_strategy_weights[0]
		T = self.tiles[index]

		print("Generating", index)
		T.reset()
		T.strategy.setWeights(s)
		T.recalculateImage()


	def nextGeneration(self):

		choices = [self.tiles[i].strategy for i in self.progenitors]

		new_strategy_weights = [c.model.get_weights() for c in choices] # fix the top three

		for _ in range(self.pop_num - len(choices)):
			parent_A = random.choice(choices)
			parent_B = random.choice(choices)


			child_strategy_weights = reproduceStrategies(parent_A=parent_A, parent_B=parent_B, mutation_rate=np.random.uniform(0., 0.2))

			new_strategy_weights.append(child_strategy_weights)


		for i, (s, T) in enumerate(zip(new_strategy_weights, self.tiles)):
			print("Generating", i)
			T.reset()
			T.strategy.setWeights(s)
			T.recalculateImage()


		self.progenitors = []


	def save(self, event=[]):

		f_name = "output/"+time.strftime("%Y%b%d-%H:%M:%S")+".png"

		#self.canvas.postscript(file=f_name, colormode='color')

		print("SAVING AS:", f_name)
		#print("STR:", self.__str__())

		x=self.root.winfo_rootx()
		y=self.root.winfo_rooty()
		x1=x+self.root.winfo_width()
		y1=y+self.root.winfo_height()
		ImageGrab.grab().crop((x,y,x1,y1)).save(f_name)



if __name__ == "__main__":

	EG = EvolutionGrid(pop_grid_size=(4, 4), num_steps=500, window_size=(800, 800))