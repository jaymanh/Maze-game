import pygame
import random
import MapGen

def game(screen, backgroundcolour):
    running = True

    points = 0
    pointsoffest = 0

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    movespeed = 10

    mazeh = int((screen.get_height() / 10) - 1)
    mazew = int((screen.get_width() / 10) - 1)

    maze = MapGen.MapGeneration.generate_maze(mazew, mazeh)  # Create a maze
    cell_width = 10
    cell_height = 10
    wall = MapGen.MapGeneration.maze_to_rectangles(maze, cell_width, cell_height)

    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)

    apple = False
    enimies = MapGen.MapGeneration.place_ent()

    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(backgroundcolour)

        # Spawn an apple if there isn't one already
        if not apple:
            appleloc = spawnapple(screen, wall)
            apple = True

        # Draw apple and player
        pygame.draw.circle(screen , (255, 0, 0), appleloc, 4)
        pygame.draw.circle(screen, (255, 255, 255), player_pos, 4)
        text_surface = font.render(str(points), False, (0, 0, 0))
        for vertices in wall:
            pygame.draw.polygon(screen, (0, 255, 0), vertices)

        button = pygame.key.get_pressed()

        # Move player based on keypresses
        if button[pygame.K_UP]:
            new_player_pos_y = player_pos.y - movespeed
            new_position = (player_pos.x, new_player_pos_y)
            if not is_point_inside_walls(new_position, wall):
                player_pos.y -= movespeed

        if button[pygame.K_DOWN]:
            new_player_pos_y = player_pos.y + movespeed
            new_position = (player_pos.x, new_player_pos_y)
            if not is_point_inside_walls(new_position, wall):
                player_pos.y += movespeed

        if button[pygame.K_LEFT]:
            new_player_pos_x = player_pos.x - movespeed
            new_position = (new_player_pos_x, player_pos.y)
            if not is_point_inside_walls(new_position, wall):
                player_pos.x -= movespeed

        if button[pygame.K_RIGHT]:
            new_player_pos_x = player_pos.x + movespeed
            new_position = (new_player_pos_x, player_pos.y)
            if not is_point_inside_walls(new_position, wall):
                player_pos.x += movespeed

        if button[pygame.K_p]:
            player_pos.x, player_pos.y = appleloc

        if button[pygame.K_ESCAPE]:
            return

        # Check if player is on apple and handle scoring
        player_posround = round(player_pos)

        if player_posround == appleloc:
            apple = False
            points += 1

            if points - pointsoffest >= 10:
                maze = MapGen.MapGeneration.generate_maze(mazew, mazeh)
                wall = MapGen.MapGeneration.maze_to_rectangles(maze, cell_width, cell_height)
                player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                appleloc = spawnapple(screen, wall)
                apple = True
                pointsoffest = points

        # Display the current score on the screen
        screen.blit(text_surface, (0, 0))
        pygame.display.flip()

        clock.tick(60) / 1000

def spawnapple(screen, wall):
    screenw = screen.get_width()
    screenh = screen.get_height()
    while True:
        appleloc = (
            (random.randint(1, ((screenw // 10) - 1)) * 10),
            (random.randint(1, ((screenh // 10) - 1))) * 10
        )

        if not is_point_inside_walls(appleloc, wall):
            return appleloc

def is_point_inside_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_intercept = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= x_intercept:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def is_point_inside_walls(point, walls):
    for wall_polygon in walls:
        if is_point_inside_polygon(point, wall_polygon):
            return True
    return False

