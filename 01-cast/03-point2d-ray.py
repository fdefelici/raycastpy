import pygame
import math

def verti_ray(pos, ray, angle): 
    if ray.x < 0:
        step = -1
        Vx = int(pos.x / BLOCK_SIZE) * BLOCK_SIZE - 1
    else:
        step = 1
        Vx = int(pos.x / BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE

    Vy = pos.y + int ( (pos.x - Vx)*math.tan(math.radians(90-angle)) )
    pygame.draw.circle(screen, (255, 0, 0), (int(Vx), int(Vy)), 3)

    deltaX = step * BLOCK_SIZE
    deltaY = (step*-1)*BLOCK_SIZE * math.tan(math.radians(90-angle))

    i = 0
    hit = False
    mapRow = -1
    mapCol = -1
    while True:
        posX = int(Vx+deltaX*i)
        posY = int(Vy+deltaY*i)
        if (posX < 0 or posX >= WIDTH): break
        if (posY < 0 or posY >= HEIGHT): break
        pygame.draw.circle(screen, (255, 0, 0), (posX, posY), 3)

        mapCol = int(posX / BLOCK_SIZE)
        mapRow = int(posY / BLOCK_SIZE)

        if MAP[mapRow][mapCol] == 1:
            hit = True
            break
        i += 1

    len = -1
    if hit: 
        c1 = abs(pos.x) - abs(posX)
        c2 = abs(pos.y) - abs(posY)
        len =  math.sqrt(c1*c1 + c2*c2)
    return (hit, len, mapRow, mapCol)

def horiz_ray(pos, ray, angle): 
    if ray.y < 0:
        Hy = int(pos.y / BLOCK_SIZE) * BLOCK_SIZE - 1
        stepY = -1
    else: 
        Hy = int(pos.y / BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE
        stepY = 1

    Hx = pos.x + int ( (pos.y - Hy)/math.tan(math.radians(90-angle)) )
    #pygame.draw.circle(screen, BLOCK_GREE, (int(Hx), int(Hy)), 3)

    deltaY = stepY * BLOCK_SIZE
    deltaX = (stepY*-1)*BLOCK_SIZE / math.tan(math.radians(90-angle))

    i = 0
    hit = False
    mapRow = -1
    mapCol = -1
    while True:
        posX = int(Hx+deltaX*i)
        posY = int(Hy+deltaY*i)
        if (posX < 0 or posX >= WIDTH): break
        if (posY < 0 or posY >= HEIGHT): break
        pygame.draw.circle(screen, BLOCK_GREE, (posX, posY), 3)

        mapCol = int(posX / BLOCK_SIZE)
        mapRow = int(posY / BLOCK_SIZE)

        if MAP[mapRow][mapCol] == 1:
            hit = True
            break
        i += 1

    len = -1
    if hit: 
        c1 = abs(pos.x) - abs(posX)
        c2 = abs(pos.y) - abs(posY)
        len =  math.sqrt(c1*c1 + c2*c2)
    return (hit, len, mapRow, mapCol)

def raycast(pos, ray, angle):     
    # NEXT HORIZONTAL LINE 
    hitH, lenH, rowH, colH = horiz_ray(pos, ray, angle)
    hitV, lenV, rowV, colV = verti_ray(pos, ray, angle)

    if hitH and hitV:
        found = True
        if lenH < lenV:
            blockColor = BLOCK_GREE
            row = rowH
            col = colH
        else:
            blockColor = BLOCK_RED
            row = rowV
            col = colV
    elif hitH:
        found = True
        blockColor = BLOCK_GREE
        row = rowH
        col = colH
    elif hitV:
        found = True
        blockColor = BLOCK_RED
        row = rowV
        col = colV
    else:
        found = False

    if found:
        block = pygame.Rect(col*BLOCK_SIZE, row*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, blockColor, block)

WIDTH = 300
HEIGHT = 300

MAP2 = [
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

MAP = [
    [1, 0, 1],
    [0, 0, 0],
    [0, 0, 1],
]

MAP_ROWS = len(MAP)
MAP_COLS = len(MAP[0])

BLOCK_SIZE = WIDTH / MAP_COLS

BLOCK_RED = (255,0,0)
BLOCK_GREE = (0,255,0)

FPS = 60

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
mainloop = True   

player = type('', (), {})
player.pos = pygame.math.Vector2(50, 250)
player.dir = pygame.math.Vector2(1, -1).normalize()
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

    '''
    for row in range(MAP_ROWS):
        screen_y = row * BLOCK_SIZE
        for col in range(MAP_COLS):
            cell = MAP[row][col]
            screen_x = col * BLOCK_SIZE
            if cell == 1 :
                block = pygame.Rect(screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, (255, 0, 0), block)
    '''
    pygame.draw.circle(screen, (0, 255, 0), (int(player.pos.x), int(player.pos.y)), int(BLOCK_SIZE/6))

    '''
    start = player.pos;
    dist = player.vision.distance
    half_fov = player.vision.fov / 2
    left = start + dist*player.dir.rotate(-half_fov)
    right = start + dist*player.dir.rotate(half_fov)
    pygame.draw.polygon(screen, (0, 0, 255), [start, left, right], 0)
    angle_step = 60
    angle = -half_fov + angle_step
    ''' 
    #ray_dir = player.dir.rotate(angle)

    pygame.draw.line(screen, (255, 0, 0), player.pos, player.pos + player.dir * 30)
    
   # has_hit, r, c, x, y = raycast(player.pos, ray_dir)
    up = pygame.math.Vector2(0, -1)
    angle = up.angle_to(player.dir)
    raycast(player.pos, player.dir, angle)
    #print(player.dir)

    '''
    r, c, x, y = raycast(player.pos, angle, ray_dir)
    if (r is None): continue
    #pygame.draw.line(screen, (255, 255, 255), player.pos, player.pos + ray_dir*40)

    target = pygame.math.Vector2(x, y)
    pygame.draw.line(screen, (255, 255, 255), player.pos, target)

    cell = MAP[r][c]
    screen_x = r * BLOCK_SIZE
    screen_y = c * BLOCK_SIZE
    if cell == 1 :
        block = pygame.Rect(screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), block)
    '''

    for row in range(MAP_ROWS):
        screen_y = row * BLOCK_SIZE
        pygame.draw.line(screen, (25,255,255), (0, screen_y), (WIDTH, screen_y))
        for col in range(MAP_COLS):
            cell = MAP[row][col]
            screen_x = col * BLOCK_SIZE
            pygame.draw.line(screen, (25,255,255), (screen_x, 0), (screen_x, HEIGHT))
          
    #Update Pygame display.
    pygame.display.flip()

pygame.quit()
