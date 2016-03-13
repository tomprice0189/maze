
import collections
from enum import Enum

#VisitedCell = collections.namedtuple("VisitedCell", ["up", "down", "left", "right"])
MazeCell = collections.namedtuple("MazeCell", ["x", "y"])

class Direction(Enum):
	up = 1
	down = 2
	left = 3
	right = 4

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
			
		self.maze[new_cell.y][new_cell.x] = 'O'
		return new_cell

	def get_cell_val(self, cell):
		return self.maze[cell.y][cell.x]

	def check_move_valid(self, cell, direction):
		print(self.visited[cell.y][cell.x])
		if self.get_cell_val(cell) != '#':
			if direction == Direction.up:
				if self.visited[cell.y][cell.x].up == False:
					return True
			elif direction == Direction.down:
				if self.visited[cell.y][cell.x].down == False:
					return True
			elif direction == Direction.left:
				if self.visited[cell.y][cell.x].left == False:
					return True
			elif direction == Direction.right:
				if self.visited[cell.y][cell.x].right == False:
					return True

		return False

	def mark_cell_invalid(self, cell, direction):
			t = self.visited[cell.y][cell.x]
			if direction == Direction.up:				
				self.visited[cell.y][cell.x] = VisitedCell(up=True, down=t.down, left=t.left, right=t.right)
			elif direction == Direction.down:
				self.visited[cell.y][cell.x] = VisitedCell(up=t.up, down=True, left=t.left, right=t.right)
			elif direction == Direction.left:
				self.visited[cell.y][cell.x] = VisitedCell(up=t.up, down=t.down, left=True, right=t.right)
			elif direction == Direction.right:
				self.visited[cell.y][cell.x] = VisitedCell(up=t.up, down=t.down, left=t.left, right=True)

	def print_maze(self):
		for line in self.maze:
			str = ''.join(line)
			print(str)
		print('\n')

	def solve(self):
		current_cell = self.start_coords

		test = 0;
		while True:
			if test == 5:
				break;

			test += 1
			# check up down left and right
			#up
			#print("Current cell x: " + str(current_cell.x) + " current cell y: " + str(current_cell.y))


			if current_cell.y > 0 and self.check_move_valid(MazeCell(x=current_cell.x, y=current_cell.y -1), Direction.up):
				self.mark_cell_invalid(current_cell, Direction.up)
				current_cell = self.move_token(current_cell, MazeCell(current_cell.x, current_cell.y - 1))
				self.print_maze()
				continue

			if current_cell.y < self.height - 1 and self.check_move_valid(MazeCell(x=current_cell.x, y=current_cell.y + 1), Direction.down):
				self.mark_cell_invalid(current_cell, Direction.down)
				current_cell = self.move_token(current_cell, MazeCell(current_cell.x, current_cell.y + 1))
				self.print_maze()
				continue



maze = Maze()
maze.open('maze.txt')
maze.print_maze()
maze.solve()
