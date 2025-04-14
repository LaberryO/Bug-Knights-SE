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
        self.health = 5;

        # Dodge
        self.isDodging = False;
        self.dodgeTime = 0;
        self.dodgeCooldown = 0.5;
        self.dodgeTimer = 0;

        # Invincible
        self.isInvincible = False;
        self.invincibleTime = 0;
        self.invincibleDuration = 1.0; # 지속 시간 (초)

        # Image
        self.image = [
            rescale(imageLoader("player_0.png"), self.size),
            rescale(imageLoader("player_1.png"), self.size),
            rescale(imageLoader("player_2.png"), self.size),
            rescale(imageLoader("player_3.png"), self.size)
        ];

        # Center
        self.centerX = self.size / 2;
        self.centerY = self.size / 2;

    def move(self, keys, deltaTime):
        # 회피 중에 일반 기동 방지
        if self.isDodging:
            return;
        # 공격 중에 위 보고 속도 느려지게
        if self.isAttack:
            self.speed = self.defaultSpeed / 2;
            self.heading = 2;
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
        bullets.append(Bullet(self, self.x + self.centerX));

    def idle(self):
        self.isAttack = False;
        self.speed = self.defaultSpeed;

    def hitBy(self, monster):
        # 플레이어 피격 범위
        # self.x + self.centerX / 2 ~ self.x + self.size - self.centerX / 2
        # self.y + self.centerY / 2 ~ self.y + self.size - self.centerY / 2

        # monsters.x + monsters.size > self.x + self.centerX / 2 왼쪽 피격
        # monsters.x < self.x + self.size - self.centerX / 2 오른쪽 피격
        # monsters.y + monsters.size > self.y + self.centerY / 2 위쪽 피격
        # 아래쪽은 어차피 감지 안해도 됨
        # 아래쪽 감지 안해서 죽음 FUCK
        return (
            monster.x + monster.size > self.x + self.centerX / 2 and
            monster.x < self.x + self.size - self.centerX / 2 and
            monster.y + monster.size > self.y + self.centerY / 2 and
            monster.y < self.y + self.size - self.centerY / 2
        )
    
    def damage(self, monster):
        if self.isInvincible:
            return False;
    
        self.health -= monster.damage;
        if self.health <= 0:
            return True;
        else:
            return False;

    # 회피
    def dodge(self, direction, deltaTime):
        if self.dodgeTimer > 0:
            return;

        self.isDodging = True;
        self.isInvincible = True;
        self.invincibleTime = self.invincibleDuration;

        dodgeDistance = self.size;
        if direction == "left" and self.x > 0:
            self.x = max(0, self.x - dodgeDistance);
        elif direction == "right" and self.x < Screen().getWidth() - self.size:
            self.x = min(Screen().getWidth() - self.size, self.x + dodgeDistance);

        # 타이머
        self.dodgeTime = 0.2; # Dodge 지속 시간
        self.dodgeTimer = self.dodgeCooldown;

    # 자체 업데이트
    def update(self, deltaTime):
        if self.isDodging:
            self.dodgeTime -= deltaTime;
            if self.dodgeTime <= 0:
                self.isDodging = False;
        
        # 무적 시간
        if self.isInvincible:
            self.invincibleTime -= deltaTime;
            if self.invincibleTime <= 0:
                self.isInvincible = False;

        if self.dodgeTimer > 0:
            self.dodgeTimer -= deltaTime;

