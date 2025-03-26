from ..Data.Screen import Screen;
from ..System.PathLoader import imageLoader;
from ..System.ImageEditor import rescale;
from .Entity import Entity;
import pygame;

# 플레이어
class Player(Entity):
    # 초기값 설정
    def __init__(self):
        self.x = Screen().getWidth() / 2;
        self.y = Screen().getHeight() - 70;
        self.speed = Screen().getWidth() / 2.5;
        self.heading = 0;
        # Image
        self.image = [
            rescale(imageLoader("player_0.png"), 64),
            rescale(imageLoader("player_1.png"), 64),
            rescale(imageLoader("player_2.png"), 64),
            rescale(imageLoader("player_3.png"), 64)
        ];
    def move(self, keys, deltaTime):
        if keys == []:
            self.heading = 2;
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed * deltaTime;
            self.heading = 3;
        if keys[pygame.K_RIGHT] and self.x < Screen().getWidth():
            self.x += self.speed * deltaTime;
            self.heading = 1;
    def draw(self, screen):
        screen.blit(self.image[self.heading], (self.x, self.y));
