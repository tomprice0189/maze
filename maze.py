
import collections

VisitedCell = collections.namedtuple("VisitedCell", ["up", "down", "left", "right"])
MazeCell = collections.namedtuple("MazeCell", ["x", "y"])

class Maze:
	def open(self, file_name):
		lines = [line.rstrip('\n') for line in open('maze.txt')]
		if len(lines) < 5:
			print("error reading file, less than 4 lines")
			return

		# get the width and height
		w_h = lines[0].split(',')

		width = int(w_h[0])
		height = int(w_h[1])

		# init new maze with the size
		self.maze = [[0 for x in range(width)] for x in range(height)]
		self.visited = [[VisitedCell(up=0, down=0, left=0, right=0) for x in range(width)] for x in range(height)]

		for idx, line in enumerate(lines[2:]):
			for chidx, ch in enumerate(line):
				self.maze[idx][chidx] = ch;

		# get the starting co-ord
		start_coords = lines[1].split(',')
		self.move_token(None, MazeCell(x=int(start_coords[0]), y=int(start_coords[1])))

	def move_token(self, old_cell, new_cell):
		#if not old_cell is None:
			# clear the old value
			
		self.maze[new_cell.x][new_cell.y] = 'O'

	def print_maze(self):
		for line in self.maze:
			str = ''.join(line)
			print(str)



maze = Maze()
maze.open('maze.txt')
maze.print_maze();