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
        self.velocity = 1;
        self.speed = Screen().getHeight() / 4;

        # Image
        self.image = load(imageLoader("bullet.png"));

        # 이미지 원본 사이즈 저장
        self.tempWidth, self.tempHeight = self.image.get_size();
        del self.tempWidth; # width 는 저장 안해도 되니까 삭제

        # 탄막 가로가 너무 짧아서 늘림
        self.image = scale(self.image, (self.size, self.tempHeight));
    
    def move(self, deltaTime):
        self.y -= self.speed * self.velocity * deltaTime;
    
    def draw(self, screen):
        screen.blit(self.image, (self.x - self.size/2, self.y + self.tempHeight/2));

    def offScreen(self):
        return self.y < -self.tempHeight;

    # 가속도 수정
    def setVelocity(self, velocity):
        self.velocity = velocity;