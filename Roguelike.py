import pygame as p, pygame_menu
from pygame_menu import themes
import random as r
import datafile
from tkinter import *

file = datafile.file()
root = Tk()

p.init()
t = 0
font = p.font.Font(None, 40)
display_wide = root.winfo_screenwidth() / 1.5 #화면 가로 크기
display_height = root.winfo_screenheight() / 1.5 #화면 세로 크기
display = p.display.set_mode((display_wide,display_height)) #화면 크기 설정
fps = p.time.Clock()
p.display.set_caption("Roguelike") #게임 이름
mainmenu = pygame_menu.Menu('Roguelike', display_wide, display_height, theme=themes.THEME_SOLARIZED)
midslime = p.transform.scale(file.slime,(60,60)) #중간 크기 슬라임
smallslime = p.transform.scale(file.slime,(30,30)) #작은 크기 슬라임

class entity: #entity 클래스 hp, x, y 값을 가짐
    def __init__(self,hp,x,y):
        self.x = x
        self.y = y
        self.hp = hp

class monster(entity): #monster 클래스
    def __init__(self, hp, x, y):
        entity.__init__(self,hp,x,y)
        monster_list.append(self)
    
    def remove(self): #hp 0 이하로 떨어지면 죽음
        global exp
        if self.hp <= 0:
            monster_list.remove(self)   
            exp += self.expr

    def attack(self, att): #데미지를 받음
        self.hp -= att
    
    def move(self): #플레이어 방향으로 움직임
        if self.x > player.x:
            self.x -= self.speed
        elif self.x < player.x:
            self.x += self.speed
        
        if self.y > player.y:
            self.y -= self.speed
        elif self.y < player.y:
            self.y += self.speed

    def player_move(self): 
        self.x -= player.speed * player.dirx
        self.y -= player.speed * player.diry
        
                
class projectile: #투사체 클래스 x, y 값을 가짐
    global prevx,prevy
    def __init__(self,x,y):
        self.x = x
        self.y = y
        if player.dirx != 0 or player.diry != 0:
            self.dirx = player.dirx
            self.diry = player.diry
        else:
            self.dirx = prevx
            self.diry = prevy
        self.size = (projectile_size, projectile_size)
    
    def remove(self): #화면 밖으로 나가면 삭제
        if(self.x >= display_wide + 50 or self.x <= -50):
            arrow_list.remove(self)
       
    def move(self): #투사체 속도만큼 움직임
        self.x += self.dirx * player.projectile_speed
        self.y += self.diry * player.projectile_speed
    
    
    def delete(self):
        arrow_list.remove(self)

    def player_move(self):
        self.x -= player.speed * player.dirx
        self.y -= player.speed * player.diry


class zombie(monster):
    def __init__(self,hp,x,y):
        monster.__init__(self,hp,x,y)
        self.size = (80,108)
        self.speed = 2
        self.expr = 2

    def draw(self):
        display.blit(file.monster_png, (self.x, self.y))

class large_slime(monster):
    def __init__(self,hp,x,y):
        monster.__init__(self,hp,x,y)
        self.size = (100,100)
        self.speed = 3
        self.expr = 5

    def draw(self):
        display.blit(file.slime, (self.x, self.y))

    def remove(self):
        global exp
        if self.hp <= 0:
            monster_list.remove(self)   
            exp += self.expr
            middle_slime_p = middle_slime(16,self.x - 30,self.y)
            middle_slime_p = middle_slime(16,self.x + 30,self.y)

class middle_slime(monster):
    def __init__(self,hp,x,y):
        monster.__init__(self,hp,x,y)
        self.size = (60,60)
        self.speed = 2
        self.expr = 3

    def draw(self):
        display.blit(midslime, (self.x, self.y))
    
    def remove(self):
        global exp
        if self.hp <= 0:
            monster_list.remove(self)   
            exp += self.expr
            small_slime_p = small_slime(8,self.x - 30,self.y)
            small_slime_p = small_slime(8,self.x + 30,self.y)

class small_slime(monster):
    def __init__(self,hp,x,y):
        monster.__init__(self,hp,x,y)
        self.size = (30,30)
        self.speed = 1
        self.expr = 1

    def draw(self):
        display.blit(smallslime, (self.x, self.y))

class skeleton(monster):
    def __init__(self,hp,x,y):
        monster.__init__(self,hp,x,y)
        self.size = (80,108)
        self.speed = 2
        self.expr = 1

    def draw(self):
        display.blit(file.skeleton, (self.x, self.y))



class chara(entity): #플레이어 
    def __init__(self, hp, x, y):
        entity.__init__(self,hp,x,y)
        self.dmg = 5
        self.attack_speed = 75
        self.speed = 5
        self.projectile_speed = 8
        self.bow = 0
        self.sword = 0
        self.dirx = 0
        self.diry = 0
        self.size = (80, 108)

class arrow(projectile):
    def __init__(self, x, y):
        projectile.__init__(self,x,y)

    def draw(self):
        global arrow_png
        if self.dirx != 0 or self.diry != 0:
            display.blit(arrow_png ,(self.x,self.y))


def rect(x,y): #충돌 판정 함수
    if 0 <= x.x - y.x <= y.size[0] or 0 <= y.x - x.x <= x.size[0]:
        if 0 <= x.y - y.y <= y.size[1] or 0 <= y.y - x.y <= x.size[1]:
            return True
    
    return False

def pausing(): #일시정지
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

def init(): #게임 초기화
    global running, health, respawn_time, pause
    global attack,attack_delay,inv,inv_delay, t
    global level,exp,sp, arrow_list, monster_list
    global respawn_delay, start, projectile_size, player, arrow_png
    global displayx, displayy, time_check, prevx, prevy
    
    running = True
    projectile_size = 40
    arrow_png = p.transform.scale(file.arrow_png, (projectile_size, projectile_size))
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
    pause = 0
    t = 0
    player = chara(3, display_wide / 2 - 40, display_height / 2 - 54)
    player.bow = 1
    displayx = -300
    displayy = -300
    time_check = 5
    prevx = 1
    prevy = 1
    
def display_health(): #hp UI 띄우기
    cnt = 2
    localHealth = health
    while cnt > -1:
        x = 30*cnt + 5
        if localHealth - cnt <= 0:
            display.blit(file.empty_heart, (x, 5))
        elif localHealth % 1 != 0:
            display.blit(file.half_heart, (x, 5))
            localHealth -= 0.5
        else:
            display.blit(file.heart, (x, 5))
        cnt -= 1

def moving(): #움직임 구현
    global displayx, displayy, prevx, prevy
    key = p.key.get_pressed()
    
    if key[p.K_LEFT]:
        displayx += player.speed
        player.dirx = -1
        prevx = -1
        if key[p.K_UP]:
            prevy = -1
            player.diry = -1
        elif key[p.K_DOWN]:
            prevy = 1
            player.diry = 1
        else:
            prevy = 0
    elif key[p.K_RIGHT]:
        displayx -= player.speed
        player.dirx = 1
        prevx = 1
        if key[p.K_UP]:
            prevy = -1
            player.diry = -1
        elif key[p.K_DOWN]:
            prevy = 1
            player.diry = 1
        else:
            prevy = 0
    elif key[p.K_UP]:
        displayy += player.speed
        player.diry = -1
        prevy = -1
        prevx = 0
    elif key[p.K_DOWN]:
        displayy -= player.speed
        player.diry = 1
        prevy = 1
        prevx = 0

def respawn(): #몬스터 생성 구현
    global respawn_time, respawn_delay, time_check
    if respawn_time >= respawn_delay:
            respawn_time = 0
            minusx = list(range(int(player.x - 600), int(player.x - 500)))
            minusy = list(range(int(player.y - 500), int(player.y - 400)))
            plusx = list(range(int(player.x + 500), int(player.x + 600)))
            plusy = list(range(int(player.y + 500), int(player.y + 600)))
            spawnx = r.sample(minusx + plusx,1)
            spawny = r.sample(minusy + plusy,1)
            spawn_mob = r.sample(list(range(1,101)), 1)
            spawn_mob = spawn_mob[0]
            if time_check < 1:
                zombie_p = zombie(10,spawnx[0],spawny[0])
            elif time_check < 3:
                if spawn_mob <= 20:
                    middle_slime_p = middle_slime(16,spawnx[0],spawny[0])
                else:
                    zombie_p = zombie(10,spawnx[0],spawny[0])
            elif time_check < 5:
                if spawn_mob <= 50:
                    middle_slime_p = middle_slime(16,spawnx[0],spawny[0])
                else:
                    zombie_p = zombie(10,spawnx[0],spawny[0])
            elif time_check < 8:
                if spawn_mob <= 10:
                    large_slime_p = large_slime(24,spawnx[0],spawny[0])
                elif spawn_mob <= 80:
                    middle_slime_p = middle_slime(16,spawnx[0],spawny[0])
                else:
                    zombie_p = zombie(10,spawnx[0],spawny[0])


def start_the_game(): #게임 시작
    global running, health, respawn_time, t, pause
    global attack,attack_delay,inv,inv_delay, elapsed, arrow_png
    global level,exp,sp,start,projectile_size,player, start_time
    global displayx, displayy, time_check, respawn_delay

    init()
    
    while running :
        pausing()
        if start == 0:
            start_time = p.time.get_ticks()
        start = 1

        if displayx <= -800 or displayx >= 0: #x축을 벗어나면 다시 돌아옴
            displayx = -300

        if displayy <= -800 or displayy >= 0: #y축을 벗어나면 다시 돌아옴
            displayy = -300
        elapsed = int((p.time.get_ticks() - start_time) / 1000) + t #시간 경과 표현
        dt = fps.tick(60) #프레임 60 제한
        display.blit(file.background, (displayx, displayy)) #화면 표현
        display_health()

        time_display = font.render("%02d : %02d" %(int(elapsed / 60),elapsed % 60), True, (0,0,0))
        level_display = font.render("level " + str(level), True,(0,0,0))
        exp_display = font.render("exp %.2f" %(100 * exp / (2 * level ** 2)), True, (0,0,0))
        sp_display = font.render("sp " + str(sp), True, (0,0,0))
        size_display = font.render("size %d" %projectile_size, True, (0,0,0))
        dmg_display = font.render("dmg " + str(player.dmg), True, (0,0,0))
        as_display = font.render("as %.2f" %(60 / player.attack_speed), True, (0,0,0))

        if health == 0: #hp가 0이면 게임 종료
            running = False

        for event in p.event.get():
            if event.type == p.QUIT: #강제 종료하면 게임 종료
                running = False
            

            if event.type == p.KEYDOWN and sp >= 1: #스킬 포인트가 1 이상 있을 때
                if event.key == p.K_1:
                    sp -= 1
                    player.dmg += 3
                elif event.key == p.K_2:
                    sp -= 1
                    player.attack_speed *= 0.9
                elif event.key == p.K_3:
                    sp -= 1
                    projectile_size *= 1.2
                    arrow_png = p.transform.scale(file.arrow_png,(projectile_size,projectile_size))
                elif event.key == p.K_4:
                    sp -= 1
                    if health >= 2:
                        health = 3
                    else:
                        health += 1

            if event.type == p.KEYDOWN: #일시 정지 esc키
                if event.key == p.K_ESCAPE and pause == 0:
                    pause = 1
                elif event.key == p.K_ESCAPE and pause == 1:
                    pause = 0

    
        player.dirx = 0
        player.diry = 0

        key = p.key.get_pressed()
        moving()

        if key[p.K_F5]: #f5 누르면 재시작
            mainmenu.mainloop(display)

        if exp >= 2 * level ** 2: #레벨 업 하는데 필요한 경험치 량
            exp -= 2 * level ** 2
            level += 1
            sp += 1
        

        if (key[p.K_LCTRL] or key[p.K_RCTRL]) and attack: #공격 키
            if player.bow == 1: #무기가 활일 때
                attack = 0
                delay = player.attack_speed
                arrow_p = arrow(player.x,player.y)
                arrow_list.append(arrow_p)
    
        respawn_time += 1 #몬스터 리젠 시간(60에 1초)
        respawn()

        if time_check < elapsed / 60000: #1분마다 몬스터 리젠 시간 감소
            time_check += 1
            respawn_delay *= 0.95
        

        if attack == 0: #공격 불가능 일 때
            attack_delay += 1 

        if attack_delay >= player.attack_speed: #공격 속도 설정
            attack = 1 #공격 가능
            attack_delay = 0
    
        

        if player.bow == 1: 
            for i in arrow_list:
                i.move()
                i.draw()
                i.remove()
                i.player_move()
                for j in monster_list: 
                    if rect(i,j): #화살과 몬스터가 충돌 할 때
                        i.delete() #화살 삭제
                        j.attack(player.dmg) #몬스터가 데미지 받음
                        break
    
        if inv == 1: 
            inv_delay += 0.1

        if inv == 1 and inv_delay >= 4: #무적이고 무적이 된지 0.66초가 지나면
            inv = 0 #무적 해제
            inv_delay = 0


        for i in monster_list:
            i.draw()
            i.remove()
            i.move()
            i.player_move()
            if rect(player, i): #플레이어와 몬스터가 충돌 할 때
                if inv == 0: #무적이 아니면
                    health -= 0.5 #hp 반 칸 줄음
                    inv = 1 #무적 상태가 됨

        display.blit(file.character, (player.x,player.y))
        if sp:
            display.blit(sp_display,(display_wide - 100,50))
        display.blit(time_display,(display_wide / 2 - 45,10))
        display.blit(level_display,(display_wide - 100,10))
        display.blit(exp_display,(display_wide - 250,10))

        if key[p.K_TAB]:
            display.blit(dmg_display,(750,720))
            display.blit(as_display,(900,720))
            display.blit(size_display,(600,720))
        
        p.display.update()

mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)
mainmenu.mainloop(display)