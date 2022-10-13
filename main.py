from curses import keyname
from tkinter import font
import pygame as pg
import os
import sys 
import random as rand
import time

objects = []


#peremenii
FPS = 60

Wid = 800
Hei = 600
Window = pg.display.set_mode((Wid, Hei))
TITLEWID = 32
TITLEHEI = 32
#game
gameRun = True
#inis
pg.init()
#fps lock
clock = pg.time.Clock()
#color
blue = (0,0,255)
white = (255,255,255)
red = (255,0,0)
yellow = (255, 168,0)
green = (0, 214, 120)
purple = (139, 0, 255)

DIRECTS = [[0,-1],[1,0],[0,1],[-1,0]]

fontUI = pg.font.Font(None, 30)
#random pos
startPosxPl1 = rand.randint(0 , 800)
startPosYPl1 = rand.randint(0, 600)
startPosxpl2 = rand.randint(0 , 800)
startPosypl2 = rand.randint(0 , 600)

bonusTimet = 180

#load img
imgBuff = [
    pg.image.load('images/bonus_tank.png'),
    pg.image.load('images/bonus_star.png')
    ]
imgBush = pg.image.load('images/block_bushes.png')
imgArmor = pg.image.load('images/block_armor.png')
imgBrick = pg.image.load('images/block_brick.png')
imgTank2 = [
    pg.image.load('images/gtank1.png')
]
imgTanks = [
    pg.image.load('images/tank1.png'),
    pg.image.load('images/tank2.png'),
    pg.image.load('images/tank3.png'),
    pg.image.load('images/tank4.png'),
    pg.image.load('images/tank5.png'),
    pg.image.load('images/tank6.png'),
    pg.image.load('images/tank7.png'),
    pg.image.load('images/tank8.png'),
]
imgBangs = [
    pg.image.load('images/bang1.png'),
    pg.image.load('images/bang2.png'),
    pg.image.load('images/bang3.png'),
]

#pg.mixer.music.load("sounds/engine.wav")
#pg.mixer.music.play()
soundShoot = pg.mixer.Sound("sounds/shot.wav")
soundMove = pg.mixer.Sound("sounds/move.wav")
soundDead = pg.mixer.Sound("sounds/dead.wav")

MOVE_SPEED = [1,2,2,1,2,3,3,2]
BULLET_SPEED = [4,5,6,5,5,5,6,7]
BULLET_DAMAGE = [1,1,2,3,2,2,3,4]
SHOT_DELAY = [60,50,30,40,30,25,25,30]

#gameclass
class UI(object):
    def __init__(self):
        pass
    def update(self):
        pass
    def draw(self):
        pl = 0
        for obj in objects:
            if obj.type == "tank":
                pg.draw.rect(Window, obj.color, (5 + pl * 70, 5, 22, 22))
                text = fontUI.render(str(obj.helth), 1, obj.color)
                rect = text.get_rect(center = (5 + pl * 70 + 32, 5 +11))
                Window.blit(text, rect)
                pl += 1

class Tank(object):
    
    def __init__(self, color, px, py, direct, keyList, playername, numb):
        self.playername = playername
        objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rect = pg.Rect(px, py, TITLEHEI, TITLEWID)
        self.direct = direct
        self.moveSpeed = 2
        self.bulDamage = 1
        self.bulSpeed = 5
        self.helth = 5
        self.ShotTimer = 0
        self.ShotDilei = 60
        self.rangTank = 0
        self.image = pg.transform.rotate(imgTanks[self.rangTank],-self.direct * 90)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.numb = numb
        self.kill = 0

        self.keyLeft = keyList[0]
        self.keyUp = keyList[1]
        self.keyRigh = keyList[2]
        self.keyDown = keyList[3]
        self.keyShot = keyList[4]
    
    def update(self):
        self.image = pg.transform.rotate(imgTanks[self.rangTank],-self.direct * 90)
        self.image = pg.transform.scale(self.image, (self.image.get_width()- 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center = self.rect.center)
        
        self.moveSpeed = MOVE_SPEED[self.rangTank]
        self.ShotDilei = SHOT_DELAY[self.rangTank]
        self.bulSpeed = BULLET_SPEED[self.rangTank]
        self.bulDamage = BULLET_DAMAGE[self.rangTank]
        
        oldX, oldY = self.rect.topleft

        if keys[self.keyLeft]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        if keys[self.keyUp]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        if keys[self.keyRigh]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        if keys[self.keyDown]:
            self.rect.y += self.moveSpeed
            self.direct = 2
        if self.rect.right > Wid:
            self.rect.right = Wid
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.y > Hei:
            self.rect.y = Hei
        if self.rect.y > 576:
            self.rect.y = 576


        #print(self.rect.y)
        for obj in objects:
            if obj != self and obj.type == "block" and obj.type != "buff" and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX , oldY

        if keys[self.keyShot] and self.ShotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulSpeed
            dy = DIRECTS[self.direct][1] * self.bulSpeed
            
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulDamage)
            self.ShotTimer = self.ShotDilei
            soundShoot.play()

        if self.ShotTimer > 0: self.ShotTimer -= 1


    def draw(self):
        Window.blit(self.image, self.rect)

    def damage(self, value):
        self.helth -= value
        if self.helth <= 0:
            soundDead.play()
            objects.remove(self)
            print(self.playername, 'dead')
            if self.numb == 1 and self.helth <= 0:
                self.kill += 1
                print(self.kill)
                Tank1 = Tank(blue, startPosxPl1, startPosYPl1, 0, (pg.K_a, pg.K_w,pg.K_d,pg.K_s, pg.K_SPACE),"Player 1", 1)
            if self.numb == 2 and self.helth <=0:
                Tank2 = Tank(red, startPosxpl2, startPosypl2, 0, (pg.K_LEFT, pg.K_UP,pg.K_RIGHT,pg.K_DOWN, pg.K_0), "Player 2", 2)
                self.kill += 1
                print(self.kill)


class Bullet(object):
    def __init__(self, parent, px, py, dx, dy, damage):
        bullet.append(self)
        self.px = px
        self.py = py
        self.damage = damage
        self.dx = dx
        self.dy = dy
        self.parent = parent

    def update(self):
        self.px += self.dx 
        self.py += self.dy
        if self.px < 0 or self.px > Wid or self.py < 0 or self.py > Hei:
            bullet.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type !="bang" and obj.type != "buff" and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullet.remove(self)
                    Bang(self.px, self.py)
                    break

    def draw(self):
        pg.draw.circle(Window,yellow,(self.px, self.py),2)

class BlockArmor(object):
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = "block"
        self.rect = pg.Rect(px, py, TITLEWID, TITLEHEI)
        self.hp = 4

    def update(self):
        pass

    def draw(self):
        Window.blit(imgArmor, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0 : objects.remove(self)

class BlockBrick(object):
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = "block"
        self.rect = pg.Rect(px, py ,TITLEWID, TITLEHEI)
        self.hp = 1

    def update(self):
        pass
    
    def draw(self):
        Window.blit(imgBrick, self.rect)
        #pg.draw.rect(Window, green, self.rect, 2)
        #pg.draw.rect(Window, purple, self.rect, 2)
    
    def damage(self, value):
        self.hp -= value
        if self.hp<=0 : objects.remove(self)

class Bonus(object):
    def __init__(self, px, py, bonusNum):
        objects.append(self)
        self.type = "bonus"
        self.image = imgBuff[bonusNum]
        self.rect = self.image.get_rect(center = (px,py))
        self.timer = 600
        self.bonusNum = bonusNum 
    def update(self):
        if self.timer > 0: self.timer -= 1
        else: objects.remove(self)
        for obj in objects:
            if obj.type =="tank" and self.rect.colliderect(obj.rect):
                if self.bonusNum == 0:
                    if obj.rangTank < len(imgTanks) - 1:
                        obj.rangTank +=1
                        objects.remove(self)
                        break
                elif self.bonusNum == 1:
                    obj.helth += 1
                    objects.remove(self)
                    break
    def draw(self):
        if self.timer %30 < 15:
            Window.blit(self.image, self.rect)

class BlockBush(object):
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = "Bush"
        self.rect = pg.Rect(px,py, TITLEWID, TITLEHEI)
        self.hp = 1
        
    def update(self):
        pass
    
    def draw(self):
        Window.blit(imgBush, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <=0 : objects.remove(self)

#class init
bullet = []
Tank1 = Tank(blue, startPosxPl1, startPosYPl1, 0, (pg.K_a, pg.K_w,pg.K_d,pg.K_s, pg.K_SPACE),"Player 1", 1)
Tank2 = Tank(red, startPosxpl2, startPosypl2, 0, (pg.K_LEFT, pg.K_UP,pg.K_RIGHT,pg.K_DOWN, pg.K_KP_ENTER), "Player 2", 2)
UI = UI()


#alg for spawn block
for _ in range (100):
    while True:
        
        x = rand.randint(0, Wid // TITLEHEI - 1) * TITLEHEI
        y = rand.randint(0, Hei // TITLEWID - 1 )* TITLEHEI
        rect = pg.Rect(x, y, TITLEWID, TITLEHEI)
        finded = False
        
        for obj in objects:
            if rect.colliderect(obj.rect): finded == True
        
        if not finded: break
    BlockBrick(x,y,TITLEHEI)

for _ in range (20):
    while True:
        
        x = rand.randint(0, Wid // TITLEHEI - 1) * TITLEHEI
        y = rand.randint(0, Hei // TITLEWID - 1 )* TITLEHEI
        rect = pg.Rect(x, y, TITLEWID, TITLEHEI)
        finded = False
        
        for obj in objects:
            if rect.colliderect(obj.rect): finded == True
        
        if not finded: break
    BlockArmor(x,y,TITLEHEI)



for _ in range (40):
    while True:
        
        x = rand.randint(0, Wid // TITLEHEI - 1) * TITLEHEI
        y = rand.randint(0, Hei // TITLEWID - 1 )* TITLEHEI
        rect = pg.Rect(x, y, TITLEWID, TITLEHEI)
        finded = False
        
        for obj in objects:
            if rect.colliderect(obj.rect): finded == True
        
        if not finded: break
    BlockBush(x,y,TITLEHEI)
#class bang
class Bang(object):
    def __init__(self, px, py):
        objects.append(self)
        self.type = "bang"
        self.px, self.py = px,py
        self.frame = 0
        
    def update(self):
        self.frame += 1
        if self.frame >= 3: objects.remove(self)

    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center = (self.px, self.py))
        Window.blit(image, rect)
        
#main
def main(gameRun,bonusTimet):
    
    
    while gameRun:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
                pg.quit()

        global keys
        keys = pg.key.get_pressed()    

        if bonusTimet > 0: bonusTimet -= 1
        else:
            Bonus(rand.randint(50, Wid - 50), rand.randint(50, Hei - 50),rand.randint(0, len(imgBuff) - 1))
            bonusTimet = rand.randint(120, 240)
        for obj in objects:obj.update()
        for bul in bullet:bul.update()
        UI.update()
        Window.fill((0,0,0))
        for bul in bullet:bul.draw()
        for obj in objects: obj.draw()
        UI.draw()

        pg.display.update()
        clock.tick(FPS)

main(gameRun, bonusTimet)