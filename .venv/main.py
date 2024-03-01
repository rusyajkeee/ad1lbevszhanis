from pygame import *

window_width = 700
window_height = 500
player_speed = 10

window = display.set_mode((window_width, window_height))
display.set_caption("ad1lbek vs jeniss")

background = transform.scale(image.load("background.jpg"), (window_width, window_height))
finalscreen = transform.scale(image.load("final.png"), (window_width, window_height))
lostscreen = transform.scale(image.load("lost.png"), (window_width, window_height))


class GameSprite(sprite.Sprite):
    def __init__(self, filename, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(filename), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, filename, x, y, width, height, speed):
        super().__init__(filename, x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > window_width:
            self.kill()


class Player(GameSprite):
    def __init__(self, filename, x, y, width, height, x_speed, y_speed):
        super().__init__(filename, x, y, width, height)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.x += self.x_speed
        platform_touched = sprite.spritecollide(self, walls, False)
        if self.x_speed > 0:
            for p in platform_touched:
                self.rect.right = p.rect.left
        if self.x_speed < 0:
            for p in platform_touched:
                self.rect.left = p.rect.right

        self.rect.y += self.y_speed
        platform_touched = sprite.spritecollide(self, walls, False)
        if self.y_speed > 0:
            for p in platform_touched:
                self.rect.bottom = p.rect.top
        if self.y_speed < 0:
            for p in platform_touched:
                self.rect.top = p.rect.bottom

    def fire(self):
        bullet = Bullet("noj.jpg", self.rect.right, self.rect.centery, 100, 50, 20)


        bullets.add(bullet)


class Enemy(GameSprite):
    def __init__(self, filename, x, y, width, height, speed):
        super().__init__(filename, x, y, width, height)
        self.speed = speed
        self.direction = "left"

    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        if self.rect.x <= 250:
            self.direction = "right"
        if self.rect.x >= 420:
            self.direction = "left"





player = Player("hero.jpg", 100, 100, 80, 80, 0, 0)

walls = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()

wall1 = GameSprite("wall.png", 500, 200, 300, 50)
wall2 = GameSprite("wall.png", 200, 250, 50, 300)
walls.add(wall1)
walls.add(wall2)
walls.draw(background)
enemy = Enemy("enemy.jpg", 250, 260, 80, 80, 5)
enemy2 = Enemy("enemy.jpg", 0, 0, 80, 80, 5)
monsters.add(enemy)
monsters.add(enemy2)

goal = GameSprite("goal.jpg", 500, 400, 80, 80)

finish = False
run = True
lost = False
while run:
    time.delay(52)
    display.update()
    bullets.update()
    bullets.draw(background)
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_RIGHT:
                player.x_speed = player_speed
            if e.key == K_LEFT:
                player.x_speed = -player_speed
            if e.key == K_DOWN:
                player.y_speed = player_speed
            if e.key == K_UP:
                player.y_speed = -player_speed
            if e.key == K_SPACE:
                player.fire()


        if e.type == KEYUP:
            if e.key == K_RIGHT:
                player.x_speed = 0
            if e.key == K_LEFT:
                player.x_speed = 0
            if e.key == K_DOWN:
                player.y_speed = 0
            if e.key == K_UP:
                player.y_speed = 0

    for entity in monsters:
        for bullet in bullets:
            if bullet.rect.colliderect(entity):
                entity.kill()
                bullet.kill()

    for bullet in bullets:
        for wall in walls:
            if bullet.rect.colliderect(wall):
                bullet.kill()

    for entity in monsters:
        if player.rect.colliderect(entity):
            run = False
            lost = True
    if lost == True:
        window.blit(lostscreen, (0, 0))

    if player.rect.colliderect(goal) == True:
        finish = True
    if finish == True:
        window.blit(finalscreen, (0, 0))
    if finish == False:
        window.blit(background, (0, 0))

        player.reset()
        player.update()

        monsters.draw(window)
        monsters.update()

        goal.reset()