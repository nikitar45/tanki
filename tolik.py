import pygame
from random import randint

pygame.init()
WIDTH, HEIGHT = 576, 672
FPS = 60
TILE = 32

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fontUI = pygame.font.Font(None, 30)

imgBrick = pygame.image.load('images/block_brick.png')
imgIndestructible = pygame.image.load('images/block_armor.png')
imgTanks = [
    pygame.image.load('images/tank1.png'),
]
imgBangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png'),
]

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
MOVE_SPEED =    [1, 2, 2, 1, 2, 3, 3, 2]
BULLET_SPEED =  [4, 5, 6, 5, 5, 5, 6, 7]
BULLET_DAMAGE = [1, 1, 2, 3, 2, 2, 3, 4]
SHOT_DELAY =    [60, 50, 30, 40, 30, 25, 25, 30]


class Tank:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.hp = 5
        self.shotTimer = 0
        self.moveSpeed = 2
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1
        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]
        self.rank = 0
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)
    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.moveSpeed = MOVE_SPEED[self.rank]
        self.shotDelay = SHOT_DELAY[self.rank]
        self.bulletSpeed = BULLET_SPEED[self.rank]
        self.bulletDamage = BULLET_DAMAGE[self.rank]
        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2
        for obj in objects:
            if obj != self and getattr(obj, 'type', None) == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY
        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay
        if self.shotTimer > 0:
            self.shotTimer -= 1
    def draw(self):
        window.blit(self.image, self.rect)
    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'dead')

class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage
    def update(self):
        self.px += self.dx
        self.py += self.dy
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and getattr(obj, 'type', None) != 'bang':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Bang(self.px, self.py)
                        break
    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)

class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'
        self.px, self.py = px, py
        self.frame = 0
    def update(self):
        self.frame += 0.2
        if self.frame >= 3:
            objects.remove(self)
    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)

class Block:
    def __init__(self, px, py, size, indestructible=False):
        objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px, py, size, size)
        self.indestructible = indestructible
        self.hp = 1 if not indestructible else None
    def update(self):
        pass
    def draw(self):
        if self.indestructible:
            window.blit(imgIndestructible, self.rect)
        else:
            window.blit(imgBrick, self.rect)
    def damage(self, value):
        if self.indestructible:
            return
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)

bullets = []
objects = []

Tank('blue', 275, 100, 2, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('red', 275, 540, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RCTRL))
level_map = [
    "##################",
    "#................#",
    "#.####......####.#",
    "#................#",
    "#..##.##..##.##..#",
    "#..#..##..##..#..#",
    "#..#.##....##.#..#",
    "#................#",
    "##..#..####..#..##",
    "#...#........#...#",
    "#.###........###.#",
    "#...#........#...#",
    "##..#..####..#..##",
    "#................#",
    "#..#.##....##.#..#",
    "#..#..##..##..#..#",
    "#..##.##..##.##..#",
    "#................#",
    "#.####......####.#",
    "#................#",
    "##################"
]

rows = len(level_map)
cols = len(level_map[0])
for row_index, row in enumerate(level_map):
    for col_index, char in enumerate(row):
        if char == "#":
            if row_index == 0 or row_index == rows - 1 or col_index == 0 or col_index == cols - 1:
                Block(col_index * TILE, row_index * TILE, TILE, indestructible=True)
            else:
                Block(col_index * TILE, row_index * TILE, TILE)

play = True

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    keys = pygame.key.get_pressed()
    for bullet in bullets[:]:
        bullet.update()
    for obj in objects[:]:
        obj.update()
    tank_count = sum(1 for obj in objects if getattr(obj, 'type', None) == 'tank')
    if tank_count < 2:
        play = False
    window.fill('black')
    for bullet in bullets:
        bullet.draw()
    for obj in objects:
        obj.draw()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
