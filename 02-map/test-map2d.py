import pygame

WIDTH = 320
HEIGHT = 240

MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

MAP_ROWS = len(MAP)
MAP_COLS = len(MAP[0])

BLOCK_SIZE = WIDTH / MAP_COLS

FPS = 60

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
mainloop = True   

player = type('', (), {})
player.pos = pygame.math.Vector2(40, 40)
player.dir = pygame.math.Vector2(0, 1)
player.vision = type('', (), {})
player.vision.fov = 60
player.vision.distance = 100
player.speed = 150

while mainloop:
    # Do not go faster than this framerate.
    milliseconds = clock.tick(FPS) 
    delta_time = milliseconds / 1000.0
    
    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False
           
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        new_pos = player.pos + player.speed * player.dir * delta_time
        #RAW Collision System
        cell_col = int(new_pos.x / BLOCK_SIZE)
        cell_row = int(new_pos.y / BLOCK_SIZE)
        value = MAP[cell_row][cell_col]
        if value == 0:
            player.pos = new_pos

    if keys[pygame.K_LEFT]:
        rot_speed = player.speed * delta_time
        player.dir = player.dir.rotate(-rot_speed)
    if keys[pygame.K_RIGHT]:
        rot_speed = player.speed * delta_time
        player.dir = player.dir.rotate(rot_speed)
                
    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.3f} DELTA: {1:.3f}".format(clock.get_fps(), delta_time)
    pygame.display.set_caption(text)
    screen.fill((0, 0, 0))
    for row in range(MAP_ROWS):
        for col in range(MAP_COLS):
            cell = MAP[row][col]
            screen_x = col * BLOCK_SIZE
            screen_y = row * BLOCK_SIZE
            if cell == 1 :
                block = pygame.Rect(screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, (255, 0, 0), block)

    pygame.draw.circle(screen, (0, 255, 0), (int(player.pos.x), int(player.pos.y)), int(BLOCK_SIZE/2))

    start = player.pos;
    dist = player.vision.distance
    half_fov = player.vision.fov / 2
    left = start + dist*player.dir.rotate(-half_fov)
    right = start + dist*player.dir.rotate(half_fov)
    pygame.draw.polygon(screen, (0, 0, 255), [start, left, right], 0)

    #Update Pygame display.
    pygame.display.flip()

pygame.quit()
