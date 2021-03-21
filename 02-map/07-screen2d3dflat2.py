import pygame
import math

class RayHit:
    def noHit():
        return RayHit()
    
    def hit(len, row, col, x, y):
        result = RayHit()
        result.hasHit = True
        result.len = len
        result.row = row
        result.col = col
        result.x = x 
        result.y = y
        return result

    def shortest(hit1, hit2):
        if hit1.isShortest(hit2):
            return hit1
        else:
            return hit2
        
    def __init__(self):
        self.hasHit = False
        self.len = math.inf
        self.row = -1
        self.col = -1
        self.x = -1
        self.y = -1
    
    def isShortest(self, otherRay):
        if self.len < otherRay.len: return True
        return False

def verti_ray(pos, ray, angle): 
    tan = math.tan(math.radians(angle))
    if abs(tan) < 0.0001: return RayHit.noHit()

    if ray.x < 0:
        step = -1
        Vx = int(pos.x / BLOCK_SIZE) * BLOCK_SIZE - 1
    else:
        step = 1
        Vx = int(pos.x / BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE

    Vy = pos.y + int ( (pos.x - Vx)*tan )
    
    if Vx < 0 or Vx > WIDTH: return RayHit.noHit()
    if Vy < 0 or Vy > HEIGHT: return RayHit.noHit()

    #pygame.draw.circle(screen, (255, 0, 0), (int(Vx), int(Vy)), 3)

    deltaX = step * BLOCK_SIZE
    deltaY = (step*-1)*BLOCK_SIZE * tan

    i = 0
    hit = False
    mapRow = -1
    mapCol = -1
    while True:
        posX = int(Vx+deltaX*i)
        posY = int(Vy+deltaY*i)
        if (posX < 0 or posX >= WIDTH): break
        if (posY < 0 or posY >= HEIGHT): break
        #pygame.draw.circle(screen, (255, 0, 0), (posX, posY), 3)

        mapCol = int(posX / BLOCK_SIZE)
        mapRow = int(posY / BLOCK_SIZE)

        if MAP[mapRow][mapCol] == 1:
            hit = True
            break
        i += 1

    if hit: 
        c1 = abs(pos.x) - abs(posX)
        c2 = abs(pos.y) - abs(posY)
        len =  math.sqrt(c1*c1 + c2*c2)
        return RayHit.hit(len, mapRow, mapCol, posX, posY)
    else:
        return RayHit.noHit()

def horiz_ray(pos, ray, angle):
    tan = math.tan(math.radians(angle))
    if abs(tan) < 0.0001: return RayHit.noHit()

    if ray.y < 0:
        Hy = int(pos.y / BLOCK_SIZE) * BLOCK_SIZE - 1
        stepY = -1
    else: 
        Hy = int(pos.y / BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE
        stepY = 1

    Hx = pos.x + int ( (pos.y - Hy)/tan )
    
    if Hx < 0 or Hx > WIDTH: return RayHit.noHit()
    if Hy < 0 or Hy > HEIGHT: return RayHit.noHit()

    deltaY = stepY * BLOCK_SIZE
    deltaX = (stepY*-1)*BLOCK_SIZE / tan

    i = 0
    hit = False
    mapRow = -1
    mapCol = -1
    while True:
        posX = int(Hx+deltaX*i)
        posY = int(Hy+deltaY*i)
        if (posX < 0 or posX >= WIDTH): break
        if (posY < 0 or posY >= HEIGHT): break
        #pygame.draw.circle(screen, BLOCK_GREE, (posX, posY), 3)

        mapCol = int(posX / BLOCK_SIZE)
        mapRow = int(posY / BLOCK_SIZE)

        if MAP[mapRow][mapCol] == 1:
            hit = True
            break
        i += 1

    if hit: 
        c1 = abs(pos.x) - abs(posX)
        c2 = abs(pos.y) - abs(posY)
        len =  math.sqrt(c1*c1 + c2*c2)
        return RayHit.hit(len, mapRow, mapCol, posX, posY)
    else:
        return RayHit.noHit()

def raycast(pos, ray):
    # Uso UP per trovare sempre l'angolo positivo rispetto al ray
    up = pygame.math.Vector2(0, -1)
    angle = up.angle_to(ray)
    angle = 90 - angle

    hitH = horiz_ray(pos, ray, angle)
    hitV = verti_ray(pos, ray, angle)
    return RayHit.shortest(hitH, hitV)

def render2d():
    surf = pygame.Surface((WIDTH2D, HEIGHT2D))
    
    # Player
    pygame.draw.circle(surf, (0, 255, 0), (int(player.pos.x), int(player.pos.y)), int(BLOCK_SIZE/6))

    # Direzione del Player
    pygame.draw.line(surf, (255, 0, 0), player.pos, player.pos + player.dir * 30)

    # Raycast for each angle within FOV
    half_fov = player.vision.fov / 2
    for i, each in enumerate(range(player.vision.fov)):
        angleFov = each - half_fov
        rayDir =  player.dir.rotate(angleFov)
        rayHit = raycast(player.pos, rayDir)
        pygame.draw.line(surf, (255, 0, 0), player.pos, player.pos + rayDir * 300)
        '''
        if (i == 0):
            pygame.draw.line(surf, (255, 0, 0), player.pos, player.pos + rayDir * 300)
        elif i == player.vision.fov - 1:
            pygame.draw.line(surf, (255, 0, 0), player.pos, player.pos + rayDir * 300)
        '''
        if rayHit.hasHit:
            block = pygame.Rect(rayHit.col*BLOCK_SIZE, rayHit.row*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surf, (255, 100, 100), block)

   
    # DRAW GRID
    for row in range(MAP_ROWS):
        screen_y = row * BLOCK_SIZE
        pygame.draw.line(surf, (25,255,255), (0, screen_y), (WIDTH, screen_y))
        for col in range(MAP_COLS):
            cell = MAP[row][col]
            screen_x = col * BLOCK_SIZE
            pygame.draw.line(surf, (25,255,255), (screen_x, 0), (screen_x, HEIGHT))
    
    return surf

def render3d():
    surf = pygame.Surface((WIDTH3D, HEIGHT3D))

    numRays = WIDTH3D
    deltaRayAngle = player.vision.fov / numRays

    half_fov = player.vision.fov / 2
    for rayIndex in range(numRays):
        angleFov = rayIndex * deltaRayAngle - half_fov
        rayDir =  player.dir.rotate(angleFov)
        rayHit = raycast(player.pos, rayDir)
        
        if not rayHit.hasHit : continue
        
        lenFishEye = rayHit.len
        lenNoFishEye = lenFishEye * math.cos(math.radians(angleFov))
        #rayLen = lenNoFishEye
        rayLen = lenFishEye

        lineH = HEIGHT / rayLen * 100
        top = HEIGHT/2 - lineH/2
        #block = pygame.Rect(rayIndex, int(top), 1, int(lineH))
        #pygame.draw.rect(surf, (255, 100, 100), block)
        pygame.draw.line(surf, (255, 100, 100), (rayIndex, int(top)), (rayIndex, int(top) + lineH))
    
    return surf

WIDTH = 480
HEIGHT = 320

WIDTH2D=480
HEIGHT2D=320

WIDTH3D=480
HEIGHT3D=320

MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

MAP2 = [
    [1, 0, 1],
    [0, 0, 0],
    [0, 0, 1],
]

MAP_ROWS = len(MAP)
MAP_COLS = len(MAP[0])

BLOCK_SIZE = WIDTH3D / MAP_COLS

BLOCK_RED = (255,0,0)
BLOCK_GREE = (0,255,0)

FPS = 60

pygame.init()
screen=pygame.display.set_mode((WIDTH2D+WIDTH3D+10, HEIGHT2D if HEIGHT2D > HEIGHT3D else HEIGHT3D))
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
    screen.fill((200, 200, 200))

    surf2d = render2d()
    surf3d = render3d()

    screen.blit(surf2d, (0,0))
    screen.blit(surf3d, (WIDTH2D+10, 0))
   
    #Update Pygame display.
    pygame.display.flip()

pygame.quit()
