from ..Data.Screen import Screen;

from abc import ABC, abstractmethod;

import random;

class Monster(ABC):
    @abstractmethod
    def __init__(self):
        self.size = 48;
        self.x = random.randint(0, Screen().getWidth() - self.size);
        self.y = -100;
        self.dy = 0.1;
        self.accSpeed = 0.15;
        self.damage = 1;
        self.isDamaged = False;
    
        # 애니메이션 변수
        self.currentFrame = 0;
        self.frameTime = 0.0; # 누적 시간 저장
        self.frameInterval = 0.25; # 초 기준

    @abstractmethod
    def move(self, deltaTime):
        self.frameTime += deltaTime;
        if self.frameTime >= self.frameInterval:
            self.frameTime = 0;
            # 애니메이션 확장성을 위한 구문
            # 일종의 시계처럼 계속 루프함.
            self.currentFrame = (self.currentFrame + 1) % len(self.image);
    
    @abstractmethod
    def draw(self, screen):
        screen.blit(self.image[self.currentFrame], (self.x, self.y));

    @abstractmethod
    def offScreen(self):
        return self.y > Screen().getHeight();

    @abstractmethod
    def takeHit(self, bullets):
        # 피타고라스 정리를 활용한 원형 거리 계산법
        if bullets.attackType == "allAttackSkill":
            return self.y < bullets.graphic.y + bullets.tempHeight and self.y + self.size > bullets.graphic.y;
        else:
            return (self.x + self.size / 2 - bullets.x)**2 + (self.y + self.size / 2 - bullets.y)**2 < (self.size / 2)**2;