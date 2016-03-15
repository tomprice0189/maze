import collections
from enum import Enum
import time

MazeCell = collections.namedtuple("MazeCell", ["x", "y"])

class Direction(Enum):
	up = 1
	down = 2
	left = 3
	right = 4
	invalid = 5

class Maze:
	def open(self, file_name):
		lines = [line.rstrip('\n') for line in open('maze.txt')]
		if len(lines) < 5:
			print("error reading file, less than 4 lines")
			return

		# get the width and height
		w_h = lines[0].split(',')

		self.width = int(w_h[0])
		self.height = int(w_h[1])

		# init new maze with the size
		self.maze = [[0 for x in range(self.width)] for x in range(self.height)]
		self.visited = [[-1	for x in range(self.width)] for x in range(self.height)]

		for idx, line in enumerate(lines[2:]):
			for chidx, ch in enumerate(line):
				self.maze[idx][chidx] = ch;

		# get the starting co-ord
		start_coords_split = lines[1].split(',')
		self.start_coords = MazeCell(x=int(start_coords_split[0]), y=int(start_coords_split[1]))
		# check it is a valid start
		self.move_token(None, self.start_coords)

	def move_token(self, old_cell, new_cell):
		if not old_cell is None:
			self.maze[old_cell.y][old_cell.x] = ' '
		
		if self.maze[new_cell.y][new_cell.x] != 'X':
			self.maze[new_cell.y][new_cell.x] = 'O'
		return new_cell

	def get_cell_val(self, cell):
		return self.maze[cell.y][cell.x]

	def decrement_cell(self, cell):
		self.visited[cell.y][cell.x] = self.visited[cell.y][cell.x] - 1
			
	def set_valid_moves(self, cell):		
		incr = 0
		best_dir = Direction.invalid

		if cell.x > 0 and self.maze[cell.y][cell.x-1] != '#':
			incr += 1
			if self.visited[cell.y][cell.x-1] == -1 or best_dir == Direction.invalid:
				best_dir = Direction.left
		if cell.x < self.width -1 and self.maze[cell.y][cell.x+1] != '#':
			incr += 1
			if self.visited[cell.y][cell.x+1] == -1 or best_dir == Direction.invalid:
				best_dir = Direction.right
		if cell.y > 0 and self.maze[cell.y-1][cell.x] != '#':
			incr += 1
			if self.visited[cell.y-1][cell.x] == -1 or best_dir == Direction.invalid:
				best_dir = Direction.up
		if cell.y < self.height -1 and self.maze[cell.y+1][cell.x] != '#':
			incr += 1
			if self.visited[cell.y+1][cell.x] == -1 or best_dir == Direction.invalid:
				best_dir = Direction.down
		
		# only set the visited node count if we haven't been here before
		if self.visited[cell.y][cell.x] == -1:
			self.visited[cell.y][cell.x] = incr
		
		#print("Moves available = " + str(incr))
		return best_dir

	def print_maze(self):
		for line in self.maze:
			str = ''.join(line)
			print(str)
		print('\n')

	def print_visited(self):
		for line in self.visited:
			for chr in line:			
				print(str(chr), end=" ")
			print('\n')
		print('\n')

	def solve(self):
		current_cell = self.start_coords

		test = 0;
		while True:
			print("----------------------------------------------")
			self.print_maze()

			if self.maze[current_cell.y][current_cell.x] == 'X':
				print("YOU WON")
				break

			best_dir = self.set_valid_moves(current_cell)
			#self.print_visited()
			
			if best_dir == Direction.invalid:
				print("Cannot continue, must be stuck in a loop or something")
				break;
			elif best_dir == Direction.up:
				self.decrement_cell(current_cell)
				current_cell = self.move_token(current_cell, MazeCell(current_cell.x, current_cell.y - 1))
			elif best_dir == Direction.down:
				self.decrement_cell(current_cell)
				current_cell = self.move_token(current_cell, MazeCell(current_cell.x, current_cell.y + 1))
			elif best_dir == Direction.left:
				self.decrement_cell(current_cell)
				current_cell = self.move_token(current_cell, MazeCell(current_cell.x -1, current_cell.y))
			elif best_dir == Direction.right:
				self.decrement_cell(current_cell)
				current_cell = self.move_token(current_cell, MazeCell(current_cell.x + 1, current_cell.y))

			time.sleep(0.5)

maze = Maze()
maze.open('maze.txt')
maze.solve()
