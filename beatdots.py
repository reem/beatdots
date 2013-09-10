class Board(object):
	def __init__(self, color_grid):
		self.grid = color_grid
		self.color_lookup = {}
		self.points = set()
		self.color_nums = {k:0 for k in ['Y', 'P', 'B', 'G', 'R']}
		for y, i in enumerate(self.grid):
			for x, j in enumerate(self.grid[y]):
				self.color_lookup[(y, x)] = j
				self.color_nums[j] += 1
				self.points.add((y, x))
	def getBestMove(self):
		def getBestPath(init_coords, init_path):
			# defined here so it can use self attributes and we don't have to pass the board around.
			assert(init_path[-1] == init_coords)
			init_y, init_x = init_coords
			visited_points = set(init_path)
			possible_connections = [
									(init_y, init_x - 1),
									(init_y, init_x + 1),
									(init_y - 1, init_x),
									(init_y + 1, init_x)
								   ]
 			bestPath = []
			bestPathResult = 0
			bestPathColor = 'none'
			valid_neighbors = 0

			# Since we use a flat -2 to test if the neighbor is actually the point we came from, 
			# we need a special case for the first run in any given path calculation.
			if len(init_path) == 1:
				for neighbor in possible_connections:
					if neighbor in self.points:
						if self.color_lookup[neighbor] == self.color_lookup[init_coords]:
							new_path = init_path[:]
							new_path.append(neighbor)
							valid_neighbors += 1
							path, result, color = getBestPath(neighbor, new_path)
							if result > bestPathResult:
								bestPath, bestPathResult, bestPathColor = path, result, color
			else:
				for neighbor in possible_connections:
					if neighbor in self.points:
						if neighbor not in visited_points:
							if self.color_lookup[neighbor] == self.color_lookup[init_coords]:
								if neighbor != init_path[len(init_path) - 2]:
									valid_neighbors += 1
									new_path = init_path[:]
									new_path.append(neighbor)
									path, result, color = getBestPath(neighbor, new_path)
									if result > bestPathResult:
										bestPath, bestPathResult, bestPathColor = path, result, color
						else:
							if self.color_lookup[neighbor] == self.color_lookup[init_coords]:
								if neighbor != init_path[len(init_path) - 2]:
									valid_neighbors += 1
									new_path = init_path[:]
									new_path.append(neighbor)
									path, result, color = new_path, self.color_nums[self.color_lookup[init_coords]], self.color_lookup[init_coords]
									if result > bestPathResult:
										bestPath, bestPathResult, bestPathColor = path, result, color
										break
			if valid_neighbors == 0:
				return init_path, len(init_path), self.color_lookup[init_coords]
			return bestPath, bestPathResult, bestPathColor

		# getBestMove definition
		bestPath = []
		bestPathResult = 0
		bestPathColor = 'none'
		for y, i in enumerate(self.grid):
			for x, j in enumerate(self.grid[y]):
				path, result, color = getBestPath((y, x), [(y, x)])
				if result > bestPathResult:
					bestPath, bestPathResult, bestPathColor = path, result, color

		bestPathWithColors = []
		for point in bestPath:
			bestPathWithColors.append((point, self.color_lookup[point]))

		return bestPath, bestPathResult, bestPathColor, bestPathWithColors

		
def prepOutput(path, result, color, board):
	path_grid = board.grid
	for y, row in enumerate(path_grid):
		for x, element in enumerate(row):
			if (y, x) in path:
				path_grid[y][x] += str(path.index((y, x)) + 1)
			else:
				path_grid[y][x] += "-"
	return path_grid

import random

def main():
	# color_grid = [
	# 				['G', 'G', 'P', 'R', 'Y', 'P'],
	# 				['Y', 'G', 'G', 'G', 'G', 'P'],
	# 				['Y', 'P', 'G', 'R', 'G', 'Y'],
	# 				['P', 'R', 'G', 'G', 'G', 'R'],
	# 				['R', 'P', 'R', 'R', 'P', 'R'],
	# 				['R', 'P', 'P', 'P', 'P', 'P']
	# 			   ]

	colors = ['Y', 'G', 'P', 'R', 'B']

	color_grid = [[random.choice(colors) for _ in range(6)] for _ in range(6)]

	board = Board(color_grid)
	bestPath, bestPathResult, bestPathColor, bestPathWithColors = board.getBestMove()
	
	path_grid = prepOutput(bestPath, bestPathResult, bestPathColor, board)	

	for row in path_grid:
		print row

	print bestPathWithColors, bestPathResult, bestPathColor

if __name__ == '__main__':
	main()
