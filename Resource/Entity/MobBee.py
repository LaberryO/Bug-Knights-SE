from ..Data.Screen import Screen;
from ..System.PathLoader import imageLoader;
from ..System.ImageEditor import rescale;
from .Entity import Entity;

import random, pygame;

# 벌 (몬스터)
class MobBee(Entity):
    def __init__(self):
        self.size = 48;
        self.x = random.randint(0, Screen().getWidth() - self.size);
        self.y = -100;
        self.dy = 0.1;
        self.accSpeed = 0.15;
        self.damage = 1;
        self.isDamaged = False;

        # Image
        self.image = [
            rescale(imageLoader("mobBee_0.png"), self.size),
            rescale(imageLoader("mobBee_1.png"), self.size)
        ];

        # 애니메이션 변수
        self.currentFrame = 0;
        self.frameTime = 0.0; # 누적 시간 저장
        self.frameInterval = 0.25; # 초 기준

    def move(self, deltaTime):
        self.dy += self.accSpeed;
        self.y += self.dy * deltaTime;
    
        self.frameTime += deltaTime;
        if self.frameTime >= self.frameInterval:
            self.frameTime = 0;
            # 애니메이션 확장성을 위한 구문
            # 일종의 시계처럼 계속 루프함.
            self.currentFrame = (self.currentFrame + 1) % len(self.image);

    def draw(self, screen):
        screen.blit(self.image[self.currentFrame], (self.x, self.y));

    def offScreen(self):
        return self.y > Screen().getHeight();

    def takeHit(self, bullets):
        # 피타고라스 정리를 활용한 원형 거리 계산법
        return (self.x + self.size / 2 - bullets.x)**2 + (self.y + self.size / 2 - bullets.y)**2 < (self.size / 2)**2