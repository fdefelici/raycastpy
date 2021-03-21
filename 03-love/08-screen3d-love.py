import pygame
import math

#Per evitare valori pari a 0
EPSILON=0.001 

planeDir = pygame.math.Vector2(0, 0.66)

def render3d():
    surf = pygame.Surface((WIDTH, HEIGHT))
    w = WIDTH
    h = HEIGHT
    posX = player.pos.x
    posY = player.pos.y
    dirX = player.dir.x
    dirY = player.dir.y
    planeX = planeDir.x
    planeY = planeDir.y
    for x in range(WIDTH):
        
        #calculate ray position and direction
        cameraX = 2 * x / float(w) - 1

        rayDirX = dirX + planeX * cameraX + EPSILON
        rayDirY = dirY + planeY * cameraX + EPSILON
        
        mapX = int(posX)
        mapY = int(posY)

        #length of ray from current position to next x or y-side
        sideDistX = 0
        sideDistY = 0

        #length of ray from one x or y-side to next x or y-side
        if rayDirX == 0: deltaDistX = 0.01
        else: deltaDistX = abs(1 / rayDirX)
        
        if rayDirY == 0: deltaDistY = 0.01
        else: deltaDistY = abs(1 / rayDirY)
        perpWallDist = 0
    
        #what direction to step in x or y-direction (either +1 or -1)
        stepX = 0
        stepY = 0

        hit = 0
        side = 0 #was a NS or a EW wall hit?
        #calculate step and initial sideDist
        if (rayDirX < 0): 
            stepX = -1
            sideDistX = (posX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - posX) * deltaDistX

        if (rayDirY < 0):
            stepY = -1
            sideDistY = (posY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - posY) * deltaDistY
        
        #perform DDA
        while (hit == 0):
        #jump to next map square, OR in x-direction, OR in y-direction
            if (sideDistX < sideDistY):
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1

            #Check if ray has hit a wall
            if (worldMap[mapX][mapY] > 0): hit = 1
            
        #Calculate distance projected on camera direction (Euclidean distance will give fisheye effect!)
        if (side == 0): perpWallDist = (mapX - posX + (1 - stepX) / 2) / rayDirX
        else:           perpWallDist = (mapY - posY + (1 - stepY) / 2) / rayDirY

        #Calculate height of line to draw on screen
        lineHeight = int(h / perpWallDist)

        #calculate lowest and highest pixel to fill in current stripe
        drawStart = -lineHeight / 2 + h / 2
        if(drawStart < 0): drawStart = 0
        drawEnd = lineHeight / 2 + h / 2
        if(drawEnd >= h): drawEnd = h - 1

        #choose wall color
        color = (0, 0, 0)
        val = worldMap[mapX][mapY]
        if   val == 0: color = (255, 0, 0)
        elif val == 1: color = (0, 255, 0)
        elif val == 2: color = (0, 255, 0)
        elif val == 3: color = (0, 0, 255)
        elif val == 4: color = (255, 255, 255)
        else: color = (0, 255, 255)
        
        #give x and y sides different brightness
        '''
        if perpWallDist > 15:
            color = (color[0] / 4, color[1] / 4, color[2] / 4)
        elif perpWallDist > 13:
            color = (color[0] / 3, color[1] / 3, color[2] / 3)
        elif perpWallDist > 11:
            color = (color[0] / 2, color[1] / 2, color[2] / 2)
        '''    
        if (side == 1): color = (color[0] / 2, color[1] / 2, color[2] / 2)



        #draw the pixels of the stripe as a vertical line
        pygame.draw.line(surf, color, (x, drawStart), (x, drawEnd))
    
    return surf    


WIDTH = 512
HEIGHT = 384

MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
    [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

worldMap = MAP

MAP_ROWS = len(MAP)
MAP_COLS = len(MAP[0])

BLOCK_SIZE = WIDTH / MAP_COLS

RED = (255,0,0)
GREEN = (0,255,0)

FPS = 60

pygame.init()
screen=pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
mainloop = True   

player = type('', (), {})
player.pos = pygame.math.Vector2(12, 22)
player.dir = pygame.math.Vector2(-1, 0).normalize()
player.vision = type('', (), {})
player.vision.fov = 60
player.vision.distance = 100
player.speed = 10

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
        #if value == 0:
        player.pos = new_pos
    
    if keys[pygame.K_LEFT]:
        rot_speed = player.speed * delta_time
        player.dir = player.dir.rotate(rot_speed*5)
        planeDir = planeDir.rotate(rot_speed*5)
    if keys[pygame.K_RIGHT]:
        rot_speed = player.speed * delta_time
        player.dir = player.dir.rotate(-rot_speed*5)
        planeDir = planeDir.rotate(-rot_speed*5)
                
    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.3f} DELTA: {1:.3f}".format(clock.get_fps(), delta_time)
    pygame.display.set_caption(text)
    screen.fill((200, 200, 200))

    surf3d = render3d()

    screen.blit(surf3d, (0, 0))
   
    #Update Pygame display.
    pygame.display.flip()

pygame.quit()
