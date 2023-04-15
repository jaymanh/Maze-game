import random

class MapGeneration:
    @staticmethod
    def place_ent():
        print("place_ent")

    @staticmethod
    def generate_maze(width, height):
        # Initialize maze with all 0s
        maze = [[0] * width for _ in range(height)]
        
        # Check if given x and y are within the maze
        def is_valid(x, y):
            return 0 <= x < width and 0 <= y < height

        # Generate maze using recursive backtracking
        def recursive_backtracking(x, y):
            maze[y][x] = 1
            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny) and maze[ny][nx] == 0:
                    maze[y + dy // 2][x + dx // 2] = 1
                    recursive_backtracking(nx, ny)
                    
        # Choose random start point
        start_x = random.randrange(1, width - 1, 2)
        start_y = random.randrange(1, height - 1, 2)
        recursive_backtracking(start_x, start_y)
        return maze

    @staticmethod
    def maze_to_rectangles(maze, cell_width, cell_height):
        rectangles = []
        x_offset, y_offset = 5, 5  # Set the offsets for x and y

        # Iterate through maze and generate rectangles for each wall
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 0:
                    top_left = (x * cell_width + x_offset, y * cell_height + y_offset)
                    top_right = ((x + 1) * cell_width + x_offset, y * cell_height + y_offset)
                    bottom_right = ((x + 1) * cell_width + x_offset, (y + 1) * cell_height + y_offset)
                    bottom_left = (x * cell_width + x_offset, (y + 1) * cell_height + y_offset)
                    rectangles.append([top_left, top_right, bottom_right, bottom_left])
        return rectangles
