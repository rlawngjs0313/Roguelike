import pygame as p, pygame_menu
from pygame_menu import themes
import random as r
import datafile

file = datafile.file()

p.init()
t = 0
font = p.font.Font(None, 40)
display_wide = 1024
display_height = 768
display = p.display.set_mode((display_wide,display_height))
fps = p.time.Clock()
p.display.set_caption("Roguelike")
mainmenu = pygame_menu.Menu('Roguelike', display_wide, display_height, theme=themes.THEME_SOLARIZED)


class entity:
    def __init__(self,hp,x,y):
        self.x = x
        self.y = y
        self.hp = hp


class monster(entity):
    def __init__(self, hp, x, y):
        entity.__init__(self,hp,x,y)
        monster_list.append(self)

    def remove(self):
        global exp
        if self.hp <= 0:
            monster_list.remove(self)   
            exp += self.expr

    def attack(self, att):
        self.hp -= att
    
    def move(self):
        if self.x > player.x:
            self.x -= self.speed
        elif self.x < player.x:
            self.x += self.speed
        
        if self.y > player.y:
            self.y -= self.speed
        elif self.y < player.y:
            self.y += self.speed

class projectile:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.dirx = player.dirx
        self.diry = player.diry
        self.size = (projectile_size,projectile_size) 

    def remove(self):
        if(self.x >= display_wide + 50 or self.x <= -50):
            arrow_list.remove(self)
    
    def move(self):
        self.x += self.dirx * player.projectile_speed
        self.y += self.diry * player.projectile_speed
    
    def delete(self):
        arrow_list.remove(self)


class zombie(monster):
    def __init__(self,hp,x,y):
        monster.__init__(self,hp,x,y)
        self.size = (80,108)
        self.speed = 1
        self.expr = 2

    def draw(self):
        display.blit(file.monster_png, (self.x, self.y))

class chara(entity):
    def __init__(self, hp, x, y):
        entity.__init__(self,hp,x,y)
        self.dmg = 10
        self.attack_speed = 75
        self.speed = 5
        self.projectile_speed = 10
        self.bow = 0
        self.sword = 0
        self.dirx = 0
        self.diry = 0
        self.size = (80, 108)

class arrow(projectile):
    def __init__(self, x, y):
        projectile.__init__(self,x,y)
        
    def draw(self):
        if self.dirx != 0 or self.diry != 0:
            display.blit(file.arrow_png ,(self.x,self.y))
       


def rect(x,y):
    if 0 <= x.x - y.x <= y.size[0] or 0 <= y.x - x.x <= x.size[0]:
        if 0 <= x.y - y.y <= y.size[1] or 0 <= y.y - x.y <= x.size[1]:
            return True
    
    return False

def pausing():
    global pause, elapsed,t ,start_time
    if pause:
        t = elapsed
    while pause:
        for event in p.event.get():
            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE:
                    pause = 0
                    start_time = p.time.get_ticks()
        p.display.update()

def init():
    global running, health, respawn_time, pause
    global attack,attack_delay,inv,inv_delay, t
    global level,exp,sp, arrow_list, monster_list
    global respawn_delay, start, projectile_size, player
    
    running = True
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
    pause = 0
    t = 0
    player = chara(3, 500 , 300)
    player.bow = 1
    
def display_health():
    if health == 0.5:
        display.blit(file.half_heart,(5,5))
        display.blit(file.empty_heart,(35,5))
        display.blit(file.empty_heart,(65,5))
    elif health == 1:
        display.blit(file.heart,(5,5))
        display.blit(file.empty_heart,(35,5))
        display.blit(file.empty_heart,(65,5))
    elif health == 1.5:
        display.blit(file.heart,(5,5))
        display.blit(file.half_heart,(35,5))
        display.blit(file.empty_heart,(65,5))
    elif health == 2:
        display.blit(file.heart,(5,5))
        display.blit(file.heart,(35,5))
        display.blit(file.empty_heart,(65,5))
    elif health == 2.5:
        display.blit(file.heart,(5,5))
        display.blit(file.heart,(35,5))
        display.blit(file.half_heart,(65,5))
    elif health == 3:
        display.blit(file.heart,(5,5))
        display.blit(file.heart,(35,5))
        display.blit(file.heart,(65,5))

def start_the_game():
    global running, health, respawn_time, t, pause
    global attack,attack_delay,inv,inv_delay, elapsed
    global level,exp,sp,start,projectile_size,player, start_time

    init()
    
    while running :
        pausing()
        if start == 0:
            start_time = p.time.get_ticks()
        start = 1

        elapsed = int((p.time.get_ticks() - start_time) / 1000) + t
        dt = fps.tick(60)
        display.blit(file.background, (0, 0))
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
                    global arrow_png
                    arrow_png = p.transform.scale(file.arrow_png,(projectile_size,projectile_size))
                elif event.key == p.K_4:
                    sp -= 1
                    if health >= 2:
                        health = 3
                    else:
                        health += 1

            if event.type == p.KEYDOWN:
                if event.key == p.K_ESCAPE and pause == 0:
                    pause = 1
                elif event.key == p.K_ESCAPE and pause == 1:
                    pause = 0

    
        player.dirx = 0
        player.diry = 0

        key = p.key.get_pressed()
    
        if key[p.K_LEFT]:
            player.x -= player.speed
            player.dirx = -1
        if key[p.K_RIGHT]:
            player.x += player.speed
            player.dirx = 1
        if key[p.K_UP]:
            player.y -= player.speed
            player.diry = -1
        if key[p.K_DOWN]:
            player.y += player.speed
            player.diry = 1
        if key[p.K_F5]: #f5 누르면 재시작
            mainmenu.mainloop(display)

        if exp >= 2 * level ** 2:
            exp -= 2 * level ** 2
            level += 1
            sp += 1
        

        if (key[p.K_LCTRL] or key[p.K_RCTRL]) and attack:
            if player.bow == 1:
                attack = 0
                delay = player.attack_speed
                arrow_p = arrow(player.x,player.y)
                arrow_list.append(arrow_p)
    
        respawn_time += 1
        if respawn_time >= respawn_delay:
            respawn_time = 0
            minusx = list(range(player.x - 600, player.x - 500))
            minusy = list(range(player.y - 500, player.y - 400))
            plusx = list(range(player.x + 500, player.x + 600))
            plusy = list(range(player.y + 500, player.y + 600))
            spawnx = r.sample(minusx + plusx,1)
            spawny = r.sample(minusy + plusy,1)
            zombie_p = zombie(10,spawnx[0],spawny[0])
        

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
                    if rect(i,j):
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
            if rect(player, i):
                if inv == 0:  
                    health -= 0.5
                    inv = 1

        display.blit(file.character, (player.x,player.y))
        if sp:
            display.blit(sp_display,(900,50))
        display.blit(time_display,(490,10))
        display.blit(level_display,(900,10))
        display.blit(size_display,(600,720))
        display.blit(exp_display,(750,10))
        display.blit(dmg_display,(750,720))
        display.blit(as_display,(900,720))
    
        p.display.update()

mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)
mainmenu.mainloop(display)