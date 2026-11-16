# LIBRARIES
import pygame as py

class Checkpoint:
    def __init__(self, x, y, w, h, num):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.number = num
        self.rect = py.Rect(x,y,w,h)
        
    def draw(self, screen):
        py.draw.rect(screen, (0,0,0), (self.x,self.y,self.w,self.h))