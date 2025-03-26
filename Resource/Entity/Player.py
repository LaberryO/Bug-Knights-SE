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
        self.size = 64;
        self.shots = 0;
        self.isAttack = False;
        self.defaultSpeed = self.speed;
        # Image
        self.image = [
            rescale(imageLoader("player_0.png"), self.size),
            rescale(imageLoader("player_1.png"), self.size),
            rescale(imageLoader("player_2.png"), self.size),
            rescale(imageLoader("player_3.png"), self.size)
        ];
    def move(self, keys, deltaTime):
        # 공격 중에 위 보고 속도 느려지게
        if self.isAttack:
            self.speed = self.defaultSpeed / 2;
            self.heading = 2;
        else:
            self.speed = self.defaultSpeed;
        # 안누르면 위 보게
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            self.heading = 2;
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed * deltaTime;
            if not self.isAttack:
                self.heading = 3;
        if keys[pygame.K_RIGHT] and self.x < Screen().getWidth() - self.size:
            self.x += self.speed * deltaTime;
            if not self.isAttack:
                self.heading = 1;
    def draw(self, screen):
        screen.blit(self.image[self.heading], (self.x, self.y));
    
    def attack(self, bullets):
        from .Bullet import Bullet;
        self.isAttack = True;
        # 몇발 쐈는지 체크하는 변수
        self.shots += 1;
        # print(f"Attack triggered, total shots: {self.shots}");
        bullets.append(Bullet(self, self.x+(self.size/2)));

    def idle(self):
        self.isAttack = False;

