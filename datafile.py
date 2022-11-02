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
        self.slime = p.transform.scale(self.slime, (100, 100))
        self.skeleton = p.image.load(os.path.join(DIR_IMAGE, "skeleton.png"))
        self.skeleton = p.transform.scale(self.skeleton, (80, 108))