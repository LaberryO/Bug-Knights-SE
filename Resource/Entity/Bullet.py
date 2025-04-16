# Bullet.py 탄막 객체
from ..Data.Screen import Screen;
from ..Data.Color import Color;
from ..System.PathLoader import imageLoader;
import pygame;
from pygame.image import load;
from pygame.transform import scale;

class Bullet():
    def __init__(self, player, x, attackType):
        self.player = player
        self.x = x;
        self.y = self.player.y - 10;
        self.size = 12;
        self.velocity = 2;
        self.speed = Screen().getHeight() / 4;
        self.attackType = attackType;

        # 일반 공격 구분
        if self.attackType == "allAttackSkill":
            self.tempHeight = 8;
            self.graphic = pygame.Rect((0, self.y), (Screen().getWidth(), self.tempHeight));
        else:
            width = self.size;
            self.graphic = load(imageLoader("bullet.png"));
            self.tempHeight = self.graphic.get_height();
            self.graphic = scale(self.graphic, (width, self.tempHeight));
            
            
    
    def move(self, deltaTime):
        if self.attackType == "allAttackSkill":
            speed = self.speed * 6;
            self.graphic.y -= speed * deltaTime;
        else:
            self.y -= self.speed * self.velocity * deltaTime;
    
    def draw(self, screen):
        if self.attackType == "allAttackSkill":
            pygame.draw.rect(screen, Color().aqua(), self.graphic);
        else:
            screen.blit(self.graphic, (self.x - self.size/2, self.y + self.tempHeight/2));

    def offScreen(self):
        return self.y < -self.tempHeight;

    # 가속도 수정
    def setVelocity(self, velocity):
        self.velocity = velocity;