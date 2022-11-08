import pygame as p
import os

DIR_PATH = os.path.dirname(__file__)
DIR_IMAGE = os.path.join(DIR_PATH, 'src') # 이미지 저장 경로

class file:
    def __init__(self):
        self.background = p.image.load(os.path.join(DIR_IMAGE, "background.png"))
        self.character = p.image.load(os.path.join(DIR_IMAGE, "character.png"))
        self.character = p.transform.scale(self.character,(80,108))
        self.monster_png = p.image.load(os.path.join(DIR_IMAGE, "zombie.png"))
        self.monster_png = p.transform.scale(self.monster_png,(80,108))
        self.arrow_png = p.image.load(os.path.join(DIR_IMAGE, "arrow.png"))
        self.arrow_png = p.transform.scale(self.arrow_png,(50,50))
        self.heart = p.image.load(os.path.join(DIR_IMAGE, "heart.png"))
        self.heart = p.transform.scale(self.heart,(30,30))
        self.half_heart = p.image.load(os.path.join(DIR_IMAGE, "half_heart.png"))
        self.half_heart = p.transform.scale(self.half_heart,(30,30))
        self.empty_heart = p.image.load(os.path.join(DIR_IMAGE, "no_heart.png"))
        self.empty_heart = p.transform.scale(self.empty_heart,(30,30))
        self.slime = p.image.load(os.path.join(DIR_IMAGE, "slime.png"))
        self.slime = p.transform.scale(self.slime, (120, 120))
        self.skeleton = p.image.load(os.path.join(DIR_IMAGE, "skeleton.png"))
        self.skeleton = p.transform.scale(self.skeleton, (80, 108))
        self.pick_window = p.image.load(os.path.join(DIR_IMAGE, "pickup_window.png"))
        self.pick_window = p.transform.scale(self.pick_window, (400, 50))   # 원본 픽셀값: 400, 50
        self.Image_attackSpeed = p.image.load(os.path.join(DIR_IMAGE, "attackSpeed.png"))
        self.Image_attackSpeed = p.transform.scale(self.Image_attackSpeed, (40, 40))    # 원본 픽셀값: 40, 40
        self.Image_power = p.image.load(os.path.join(DIR_IMAGE, "power.png"))
        self.Image_power = p.transform.scale(self.Image_power, (40, 40))    # 원본 픽셀값: 40, 40
        self.level_state = p.image.load(os.path.join(DIR_IMAGE, "level_state.png")) # 원본 픽셀값: 40, 40
        self.level_state = p.transform.scale(self.level_state, (40, 40))
        self.monster_hp = p.image.load(os.path.join(DIR_IMAGE, "monsterHp.png"))    # 원본 픽셀값: 100, 30
        self.monster_hp = p.transform.scale(self.monster_hp, (100, 30))
        self.monster_hp_layer = p.image.load(os.path.join(DIR_IMAGE, "monsterHpLayer.png")) # 원본 픽셀값: 100, 30
        self.monster_hp_layer = p.transform.scale(self.monster_hp_layer, (100, 30))