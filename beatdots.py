from collections import defaultdict

class Board(object):
    def __init__(self, color_grid):
        self.grid = color_grid
        self.color_lookup = dict()
        self.points = set()
        self.color_nums = defaultdict(int)
        for y, _ in enumerate(self.grid):
            for x, j in enumerate(self.grid[y]):
                self.color_lookup[(y, x)] = j
                self.color_nums[j] += 1
                self.points.add((y, x))
    def getBestMove(self):
        def _getBestPath(init_coords, init_path):
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
            bestPathColor = None
            valid_neighbors = 0

            # Since we use a flat -2 to test if the neighbor is actually the point we came from, 
            # we need a special case for the first run in any given path calculation.
            if len(init_path) == 1:
                for neighbor in possible_connections:
                    if neighbor in self.points:
                        if self.color_lookup[neighbor] == self.color_lookup[init_coords]:
                            new_path = init_path[:] + [neighbor]
                            valid_neighbors += 1
                            path, result, color = _getBestPath(neighbor, new_path)
                            if result > bestPathResult:
                                bestPath, bestPathResult, bestPathColor = path, result, color
            else:
                for neighbor in possible_connections:
                    if neighbor in self.points:
                        if neighbor not in visited_points:
                            if self.color_lookup[neighbor] == self.color_lookup[init_coords]:
                                if neighbor != init_path[-2]:
                                    valid_neighbors += 1
                                    new_path = init_path[:] + [neighbor]
                                    path, result, color = _getBestPath(neighbor, new_path)
                                    if result > bestPathResult:
                                        bestPath, bestPathResult, bestPathColor = path, result, color
                        else:
                            if self.color_lookup[neighbor] == self.color_lookup[init_coords]:
                                if neighbor != init_path[-2]:
                                    valid_neighbors += 1
                                    new_path = init_path[:] + [neighbor]
                                    path = new_path
                                    color = self.color_lookup[init_coords]
                                    result = self.color_nums[color]
                                    if result > bestPathResult:
                                        bestPath, bestPathResult, bestPathColor = path, result, color
                                        break
            if valid_neighbors == 0:
                return init_path, len(init_path), self.color_lookup[init_coords]
            return bestPath, bestPathResult, bestPathColor

        # getBestMove definition
        bestPath = []
        bestPathResult = 0
        bestPathColor = None
        for y, row in enumerate(self.grid):
            for x, _ in enumerate(row):
                path, result, color = _getBestPath((y, x), [(y, x)])
                if result > bestPathResult:
                    bestPath, bestPathResult, bestPathColor = path, result, color

        bestPathWithColors = zip(
                                map(lambda p: self.color_lookup[p], 
                                    bestPath),
                                bestPath
                             )

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

def randomgrid(colors, size):
    return [[random.choice(colors) 
                for _ in xrange(size)] 
            for _ in xrange(size)]

def test():
    color_grid = [
                  ['R', 'R', 'G', 'P', 'G', 'P'],
                  ['B', 'Y', 'B', 'B', 'Y', 'B'],
                  ['G', 'B', 'B', 'R', 'R', 'G'],
                  ['G', 'B', 'G', 'B', 'B', 'R'],
                  ['R', 'B', 'B', 'B', 'B', 'B'],
                  ['B', 'B', 'Y', 'B', 'R', 'R']
                 ]
    board = Board(color_grid)
    (bestPath, bestPathResult, 
     bestPathColor, bestPathWithColors) = board.getBestMove()
    
    assert bestPath == [(1, 2), (2, 2), (2, 1), (3, 1), (4, 1), 
                        (4, 2), (4, 3), (4, 4), (3, 4), (3, 3), 
                        (4, 3)]
    
    assert bestPathResult == 17
    assert bestPathColor == 'B'
    
    assert bestPathWithColors == [('B', (1, 2)), ('B', (2, 2)), 
                                  ('B', (2, 1)), ('B', (3, 1)), 
                                  ('B', (4, 1)), ('B', (4, 2)), 
                                  ('B', (4, 3)), ('B', (4, 4)), 
                                  ('B', (3, 4)), ('B', (3, 3)), 
                                  ('B', (4, 3))]
    
    print "All tests pass."
    
def main():
    test()
    size = 6
    color_grid = randomgrid(['Y','G','P','B','R'], size)

    board = Board(color_grid)
    bestPath, bestPathResult, bestPathColor, bestPathWithColors = board.getBestMove()

    if size <= 15:
        path_grid = prepOutput(bestPath, bestPathResult, bestPathColor, board)  

        for row in path_grid:
            print row

    print bestPathWithColors, bestPathResult, bestPathColor

if __name__ == '__main__':
    main()
