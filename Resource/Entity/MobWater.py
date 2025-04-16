from ..Data.Screen import Screen;
from ..System.PathLoader import imageLoader;
from ..System.ImageEditor import rescale;
from .Monster import Monster;

import random;

class MobWater(Monster):
    # 초기값 설정
    def __init__(self):
        super().__init__();
        self.dx = random.choice((-1, 1)) * random.randint(300, 600);

        # Image
        self.image = [
            rescale(imageLoader("mobWater_0.png"), self.size),
            rescale(imageLoader("mobWater_1.png"), self.size),
            rescale(imageLoader("mobWater_2.png"), self.size)
        ];
    
    def move(self, deltaTime):
        # 튕기기 알고리즘
        if self.x < 0 or self.x > Screen().getWidth():
            self.dx *= -1;
        
        # 가속도와 델타 타임
        self.x += self.dx * deltaTime;
        self.dy += self.accSpeed;
        self.y += self.dy * deltaTime;
    
        super().move(deltaTime);
    
    def draw(self, screen):
        super().draw(screen);
    
    def offScreen(self):
        return super().offScreen();

    def takeHit(self, bullets):
        return super().takeHit(bullets);