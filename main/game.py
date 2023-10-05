import pygame
import random
import time
import os 
from os import path

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")


WIDTH = 480
HEIGHT = 600 
FPS = 60 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (64, 29, 77)
RED = (150, 8, 38)
GREEN = (126, 235, 16)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game1")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("fixedsys")

def draw_text(surf, text, size, x , y ):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 10
    fill = (pct / 150) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10 
        self.speedx = 0 
        self.shield = 150
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20: 
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y 
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0: self.kill()

background = pygame.image.load(path.join(img_dir, "BG2.jpg")).convert() 
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect() 
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert() 
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 
               'meteorBrown_med3.png', 'meteorGrey_big1.png', 'meteorGrey_med1.png', 'meteorGrey_med2.png', 'meteorGrey_small1.png', 'meteorGrey_small2.png', 'meteorGrey_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "pew.wav"))
pygame.mixer.music.load(path.join(snd_dir, "BG.wav"))
pygame.mixer.music.set_volume(0.5)
expl_sound = [] 
expl_list = ["expl3.wav", "expl6.wav"]
for snd in expl_list:
    expl_sound.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert()


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
# time.sleep(2)
for i in range(8):
    newmob()
score = 0

pygame.mixer.music.play(loops= -1)
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
       
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits: 
        random.choice(expl_sound).play()
        score += 50 - hit.radius
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    for hit in hits: 
        player.shield = player.shield - 10
        # newmob()
        if player.shield <= 0:
            running = False
        

    all_sprites.update()
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    pygame.display.flip()
pygame.quit()