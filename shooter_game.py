#Создай собственный Шутер!
from pygame import *
from random import randint 
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Space shooter")
firesound = mixer.Sound("fire.ogg")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
rocket = ('rocket.png')
enemy = ('ufo.png')
bullet = ('bullet.png')
font.init()
font2 = font.SysFont("Arial", 36)
win = font2.render('YOU WiN', True, (255, 55, 255))
lose = font2.render('YOU LOSE', True, (255, 255, 55))
score = 0
lost = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet1 = Bullet(bullet, self.rect.centerx, self.rect.top, 15, 21, 15)
        bullets.add(bullet1)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.x = randint(80, 620)
            self.rect.y = -50
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill

monsters = sprite.Group()
for a in range(1, 6):
    monster = Enemy(enemy, randint(80, 620), -60, 80, 50, randint(1,5) )
    monsters.add(monster)
bullets = sprite.Group()  

ship = player(rocket, 5, win_height - 100, 80, 100, 13)
finish = False
game = True
while game != False:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                firesound.play()
                ship.fire()
    if not finish:
  
        window.blit(background, (0, 0))

        text_score = font2.render('Рахунок: ' + str(score), 1, (255, 255, 255))

        window.blit(text_score, (10, 20))


        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))

        window.blit(text_lose, (10, 50))

        ship.update()
        bullets.update()
        monsters.update()
        
        ship.reset()
        bullets.draw(window)
        monsters.draw(window)

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
           score += 1  
           monster = Enemy(enemy, randint(80, 629), -60, 80, 50, randint(1,5) )
           monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= 3:
            finish = True
            window.blit(lose, (250, 250))
        if score >= 10:
            window.blit(win, (250, 250))
            finish = True
        display.update()
    time.delay(30)

    