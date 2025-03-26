# Bullet.py 탄막 객체
from .Entity import Entity;
from ..Data.Screen import Screen;
from ..System.PathLoader import imageLoader;
import pygame;
from pygame.image import load;
from pygame.transform import scale;

class Bullet(Entity):
    def __init__(self, player, x):
        self.player = player
        self.x = x;
        self.y = self.player.y - 10;
        self.size = 12;
        self.speed = Screen().getHeight() / 4;

        # Image
        self.image = load(imageLoader("bullet.png"));
        self.tempWidth, self.tempHeight = self.image.get_size();
        del self.tempWidth;
        self.image = scale(self.image, (self.size, self.tempHeight));
    
    def move(self, deltaTime):
        self.y -= self.speed * deltaTime;
    
    def draw(self, screen):
        screen.blit(self.image, (self.x - self.size/2, self.y + self.tempHeight/2));

    def offScreen(self):
        return self.y < -self.tempHeight;