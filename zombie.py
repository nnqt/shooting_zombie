import pygame
import spritesheet
import random
from math import *

LIGHTBLUE = (104,164,255)

class Zombie(pygame.sprite.Sprite, ):
    FRAME_WIDTH, FRAME_HEIGHT = 33, 50
    no_frame = 7
    current_frame = 0
    last_update = 0
    animation_cooldown = 90
    animation_list_head = []
    animation_list_body = []
    x, y = 0,0
    angle = -90
    image_scale = 2

    timer = 0

    heath = 100

    def __init__(self, img_path, speed, x, y, timer):
        super().__init__()

        sprite_sheet_image = pygame.image.load(img_path).convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
        
        for i in range(self.no_frame):
            self.animation_list_head.append(sprite_sheet.get_image(i, self.FRAME_WIDTH, self.FRAME_HEIGHT - 26, self.image_scale, LIGHTBLUE))

        for i in range(self.no_frame):
            self.animation_list_body.append(sprite_sheet.get_image(i, self.FRAME_WIDTH, self.FRAME_HEIGHT, self.image_scale, LIGHTBLUE))    

        self.mask_head = pygame.mask.from_surface(self.animation_list_head[self.current_frame])
        self.mask_body = pygame.mask.from_surface(self.animation_list_body[self.current_frame])
        self.speed = speed
        self.x = x
        self.y = y
        self.y_first = y
        self.timer = timer
        
        # self.frame_0 = sprite_sheet.get_image(0, 24, 24, 3, (0,0,0))


    def updateFrame(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            if self.current_frame == self.no_frame:
                self.current_frame = 0
            else:
                self.current_frame += 1
            self.last_update = current_time
        self.mask = pygame.mask.from_surface(self.animation_list_body[self.current_frame])  

    def animation(self, window):
        # window.blit(self.frame_0, (0,0))
        self.updateFrame()
        window.blit(self.animation_list_body[self.current_frame], (self.x,self.y))
        
        
        # for x in range (1):
        #     window.blit(self.animation_list[x], (0,0))
        
    def appear(self):
        if((self.y_first - self.y) < 97):
            self.y -= self.speed
    
    def move(self,window):
        direct = random.choice([1, 0, -1])

        if direct == -1:
            self.angle += 10
        elif direct == 1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0

        self.x -= self.speed 
        self.y += self.speed * cos(radians(self.angle))

        if self.y < 0:
            # print("------------------------------")
            # print(self.y)
            # print(self.angle)
            # print("+++")
            self.y -= self.speed * cos(radians(self.angle))
            self.angle += -180
            # print(self.y)
            # print(self.angle)
        elif self.y + self.FRAME_HEIGHT * self.image_scale > window.get_height():
            # print("------------------------------")
            # print(self.y + self.FRAME_HEIGHT * self.image_scale)
            # print("+++")
            self.y -= self.speed * cos(radians(self.angle))
            self.angle += -180
            # print(self.y + self.FRAME_HEIGHT * self.image_scale)
        # elif (self.x < 0) or (self.x + self.FRAME_WIDTH) < window.get_width():
        #     self.x -= self.speed * sin(radians(self.angle))
            
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getHeath(self):
        return self.heath

    def getTimer(self):
        return self.timer

    def decreaseHeath(self, mount):
        self.heath -= mount

    def get_frame_img(self, sheet, frame, width, height, scale, transparent):
        pass
