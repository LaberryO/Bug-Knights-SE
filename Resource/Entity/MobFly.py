from ..Data.Screen import Screen;
from ..System.PathLoader import imageLoader;
from ..System.ImageEditor import rescale;
from .Entity import Entity;

import random, pygame;

# 파리 (몬스터)
class MobFly(Entity):
    # 초기값 설정
    def __init__(self):
        self.x = random.randint(0, Screen().getWidth() - self.size);
        self.y = -100;
        self.dy = 0.1;
        self.size = 64;

        # Image
        self.image = [
            rescale(imageLoader("mobFly_0.png"), self.size),
            rescale(imageLoader("mobFly_1.png"), self.size)
        ];
    def move(self, deltaTime):
        self.dy += 0.15;
        self.y += self.dy * deltaTime;
    def draw(self, screen):
        screen.blit(self.image[0], (self.x, self.y));
    def offScreen(self):
        return self.y > Screen().getHeight();