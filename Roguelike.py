from time import sleep  
import pygame as p
import pygame_menu
from pygame_menu import themes
import random as r
import os

p.init()

font = p.font.Font(None, 40)
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
monster_png = p.image.load(os.path.join(DIR_IMAGE, "monster.png"))
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


class monster:
    x = 0
    y = 0
    def __init__(self, hp, x, y, speed, expr):
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed
        self.expr = expr
        monster_list.append(self)
    
    def remove(self):
        global exp
        if self.hp <= 0:
            monster_list.remove(self)   
            exp += self.expr

    def attack(self, att):
        self.hp -= att
    
    def move(self):
        if self.x > curx:
            self.x -= self.speed
        elif self.x < curx:
            self.x += self.speed
        
        if self.y > cury:
            self.y -= self.speed
        elif self.y < cury:
            self.y += self.speed

class zombie(monster):
    def __init__(self,hp,x,y,speed,expr):
        monster.__init__(self,hp,x,y,speed,expr)

    def draw(self):
        display.blit(monster_png, (self.x, self.y))
class slime(monster):
    def __init__(self,hp,x,y,speed,expr):
        monster.__init__(self,hp,x,y,speed,expr)
    


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


def init():
    global arrow_png
    global running
    global health
    global respawn_time
    global attack,attack_delay,inv,inv_delay
    global curx, cury
    global level,exp,sp
    global arrow_list, monster_list
    global respawn_delay, start, projectile_size, player

    running = True
    curx,cury = 300,500
    attack = 1
    attack_delay = 0
    respawn_time = 0
    exp = 0
    level = 1
    arrow_list = []
    monster_list = []
    health = 3
    inv = 0
    inv_delay = 0
    respawn_delay = 180
    sp = 0
    start = 0
    projectile_size = 50
    player = chara(3,5,75,5)
    player.bow = 1
    

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

surface = p.display.set_mode((display_wide, display_height))

 
def start_the_game():
    global arrow_png
    global running
    global health
    global respawn_time
    global attack,attack_delay,inv,inv_delay
    global curx, cury
    global level,exp,sp,start,projectile_size,player

    init()
    
    while running :
        if start == 0:
            start_time = p.time.get_ticks()
        start = 1

        elapsed = int((p.time.get_ticks() - start_time) / 1000)
        dt = fps.tick(60)
        display.blit(background, (0,0))
        display_health()

        time_display = font.render("%02d : %02d" %(int(elapsed / 60),elapsed % 60), True, (0,0,0))
        level_display = font.render("level " + str(level), True,(0,0,0))
        exp_display = font.render("exp %.2f" %(100 * exp / (2 * level ** 2)), True, (0,0,0))
        sp_display = font.render("sp " + str(sp), True, (0,0,0))
        size_display = font.render("size %d" %projectile_size, True, (0,0,0))
        dmg_display = font.render("dmg " + str(player.dmg), True, (0,0,0))
        as_display = font.render("as %.2f" %(60 / player.attack_speed), True, (0,0,0))

        if health == 0:

            running = False

        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            

            if event.type == p.KEYDOWN and sp >= 1:
                if event.key == p.K_1:
                    sp -= 1
                    player.dmg += 3
                elif event.key == p.K_2:
                    sp -= 1
                    player.attack_speed *= 0.9
                elif event.key == p.K_3:
                    sp -= 1
                    projectile_size *= 1.2
                    arrow_png = p.transform.scale(arrow_png,(projectile_size,projectile_size))
                elif event.key == p.K_4:
                    sp -= 1
                    if health >= 2:
                        health = 3
                    else:
                        health += 1

    
        player.dirx = 0
        player.diry = 0

        key = p.key.get_pressed()
    
        if key[p.K_LEFT]:
            curx -= player.speed
            player.dirx = -1
        if key[p.K_RIGHT]:
            curx += player.speed
            player.dirx = 1
        if key[p.K_UP]:
            cury -= player.speed
            player.diry = -1
        if key[p.K_DOWN]:
            cury += player.speed
            player.diry = 1
        if key[p.K_F5]: #f5 누르면 재시작
            mainmenu.mainloop(surface)

        if exp >= 2 * level ** 2:
            exp -= 2 * level ** 2
            level += 1
            sp += 1
        

        if (key[p.K_LCTRL] or key[p.K_RCTRL]) and attack:
            if player.bow == 1:
                attack = 0
                delay = player.attack_speed
                arrow_p = arrow(curx,cury)
                arrow_list.append(arrow_p)
    
        respawn_time += 1
        if respawn_time >= respawn_delay:
            respawn_time = 0
            minusx = list(range(curx - 600, curx - 500))
            minusy = list(range(cury - 500, cury - 400))
            plusx = list(range(curx + 500, curx + 600))
            plusy = list(range(cury + 500, cury + 600))
            spawnx = r.sample(minusx + plusx,1)
            spawny = r.sample(minusy + plusy,1)
            zombie_p = zombie(10,spawnx[0],spawny[0],1,2)
        

        if attack == 0:
            attack_delay += 1

        if attack_delay >= player.attack_speed:
            attack = 1
            attack_delay = 0
    
        if player.bow == 1:
            for i in arrow_list:
                i.move()
                i.draw()
                i.remove()
                for j in monster_list:
                    if 0 <= i.x - j.x <= monster_size[0] or 0 <= j.x - i.x <= projectile_size:
                        if 0 <= i.y - j.y <= monster_size[1] or 0 <= j.y - i.y <= projectile_size:
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
            i.move()
            if 0 <= curx - i.x <= character_size[0] or 0 <= i.x - curx <= character_size[0]:
                if 0 <= cury - i.y <= character_size[1] or 0 <= i.y - cury <= character_size[1]:  
                    if inv == 0:  
                        health -= 0.5
                        inv = 1

        display.blit(character, (curx,cury))
        if sp:
            display.blit(sp_display,(900,50))
        display.blit(time_display,(490,10))
        display.blit(level_display,(900,10))
        display.blit(size_display,(600,720))
        display.blit(exp_display,(750,10))
        display.blit(dmg_display,(750,720))
        display.blit(as_display,(900,720))
    
        p.display.update()
 

 
 
mainmenu = pygame_menu.Menu('Roguelike', display_wide, display_height, theme=themes.THEME_SOLARIZED)
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)
 
 
mainmenu.mainloop(surface)


p.quit()