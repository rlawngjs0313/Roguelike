import pygame as p
import random as r
import os

p.init()
display_wide = 1024
display_height = 768
display = p.display.set_mode((display_wide,display_height))
fps = p.time.Clock()
p.display.set_caption("Roguelike")

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'src')


background = p.image.load(os.path.join(DIR_IMAGE, "background.png"))
character = p.image.load(os.path.join(DIR_IMAGE, "character.png"))
character = p.transform.scale(character,(80,108))
monster_png = p.image.load(os.path.join(DIR_IMAGE, "monster.jpeg"))
monster_png = p.transform.scale(monster_png,(80,108))
arrow_png = p.image.load(os.path.join(DIR_IMAGE, "arrow.png"))
arrow_png = p.transform.scale(arrow_png,(50,50))
heart = p.image.load(os.path.join(DIR_IMAGE, "heart.png"))
heart = p.transform.scale(heart,(30,30))
half_heart = p.image.load(os.path.join(DIR_IMAGE, "half_heart.png"))
half_heart = p.transform.scale(half_heart,(30,30))
empty_heart = p.image.load(os.path.join(DIR_IMAGE, "no_heart.png"))
empty_heart = p.transform.scale(empty_heart,(30,30))


character_size = (80,108)
monster_size = (80,108)
arrow_size = (50,50)


prevy = 0
prevx = 0
running = True
curx,cury = 0,500
attack = 1
attack_delay = 0
respawn_time = 0

arrow_list = []
monster_list = []

class monster:
    x = 0
    y = 0
    def __init__(self, hp, dmg, x, y):
        self.x = x
        self.y = y
        self.hp = hp
        self.dmg = dmg
        self.full = hp
        monster_list.append(self)
    
    def draw(self):
        display.blit(monster_png, (self.x, self.y))
    
    def remove(self):
        if self.hp <= 0:
            monster_list.remove(self)   

    def attack(self, att):
        self.hp -= att


class chara:
    def __init__(self, hp, dmg, attack_speed, speed):
        self.hp = hp
        self.dmg = dmg
        self.attack_speed = attack_speed
        self.speed = speed
    bow = 0
    sword = 0
    dirx = 0
    diry = 0

class arrow:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dirx = player.dirx
        self.diry = player.diry
    
    def remove(self):
        if(self.x >= display_wide + 50 or self.x <= -50):
            arrow_list.remove(self)

    def draw(self):
        if self.dirx != 0 or self.diry != 0:
            display.blit(arrow_png ,(self.x,self.y))
       
    def move(self):
        self.x += self.dirx * 10
        self.y += self.diry * 10
    
    def delete(self):
        arrow_list.remove(self)
        

player = chara(3,10,10,5)
player.bow = 1
health = 3
inv = 0
inv_delay = 0
respawn_delay = 10
monster_p = monster(10,10,500,500)

def display_health():
    if health == 0.5:
        display.blit(half_heart,(5,5))
        display.blit(empty_heart,(35,5))
        display.blit(empty_heart,(65,5))
    elif health == 1:
        display.blit(heart,(5,5))
        display.blit(empty_heart,(35,5))
        display.blit(empty_heart,(65,5))
    elif health == 1.5:
        display.blit(heart,(5,5))
        display.blit(half_heart,(35,5))
        display.blit(empty_heart,(65,5))
    elif health == 2:
        display.blit(heart,(5,5))
        display.blit(heart,(35,5))
        display.blit(empty_heart,(65,5))
    elif health == 2.5:
        display.blit(heart,(5,5))
        display.blit(heart,(35,5))
        display.blit(half_heart,(65,5))
    elif health == 3:
        display.blit(heart,(5,5))
        display.blit(heart,(35,5))
        display.blit(heart,(65,5))


while running:
    dt = fps.tick(60)
    display.blit(background, (0,0))
    display_health()
    
    if health == 0:
        running = False

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    
    player.dirx = 0
    player.diry = 0

    key = p.key.get_pressed()
    
    if key[p.K_LEFT]:
        curx -= player.speed
        player.dirx = -1
        prevx = -1
    if key[p.K_RIGHT]:
        curx += player.speed
        player.dirx = 1
        prevx = -1
    if key[p.K_UP]:
        cury -= player.speed
        player.diry = -1
        prevy = -1
    if key[p.K_DOWN]:
        cury += player.speed
        player.diry = 1
        prevy = 1

    if (key[p.K_LCTRL] or key[p.K_RCTRL]) and attack:
        if player.bow == 1:
            attack = 0
            delay = player.attack_speed
            arrow_p = arrow(curx,cury)
            arrow_list.append(arrow_p)
    
    respawn_time += 0.1
    if respawn_time >= respawn_delay:
        respawn_time = 0
        spawnx = r.sample(range(1,display_wide - 50),1)
        spawny = r.sample(range(1,display_height - 50),1)
        monster_p = monster(10,10,spawnx[0],spawny[0])
        

    if attack == 0:
        attack_delay += 0.5

    if attack_delay >= player.attack_speed:
        attack = 1
        attack_delay = 0
    
    if player.bow == 1:
        for i in arrow_list:
            i.move()
            i.draw()
            i.remove()
            for j in monster_list:
                if 0 <= i.x - j.x <= monster_size[0] or 0 <= j.x - i.x <= arrow_size[0]:
                    if 0 <= i.y - j.y <= monster_size[1] or 0 <= j.y - i.y <= arrow_size[1]:
                        i.delete()
                        j.attack(player.dmg)
                        break
    
    if inv == 1:
        inv_delay += 0.1

    if inv == 1 and inv_delay >= 4:
        inv = 0
        inv_delay = 0

    for i in monster_list:
        i.draw()
        i.remove()
        if 0 <= curx - i.x <= character_size[0] or 0 <= i.x - curx <= character_size[0]:
            if 0 <= cury - i.y <= character_size[1] or 0 <= i.y - cury <= character_size[1]:  
                if inv == 0:  
                    health -= 0.5
                    inv = 1



    
    display.blit(character, (curx,cury))
    
    p.display.update()



p.quit()