from ..Data.Screen import Screen;
from ..System.PathLoader import imageLoader;
from ..System.ImageEditor import rescale;
from .Entity import Entity;
import pygame, time;

# 플레이어
class Player(Entity):
    # 초기값 설정
    def __init__(self):
        self.size = 64;
        self.x = Screen().getCenterX() - self.size / 2;
        self.y = Screen().getHeight() - 70;
        self.speed = Screen().getWidth() / 2.5;
        self.heading = 0;
        self.shots = 0;
        self.isAttack = False;
        self.defaultSpeed = self.speed;
        self.health = 5;

        # Dodge
        self.isDodging = False;
        self.dodgeSpeed = self.speed * 2;
        self.dodgeTime = 0.15;
        self.dodgeCooldown = 0.5;
        self.dodgeTimer = 0;
        self.dodgeDirection = 0;
        self.lastAfterImageTime = 0;

        # Invincible
        self.isInvincible = False;
        self.invincibleTime = 0;
        self.invincibleDuration = 0.15; # 지속 시간 (초)

        # Skills
        self.isUsingSkill = False;
        self.skillCooldown = 20.0;
        self.skillDuration = 1.0;
        self.skillTimer = 0;
        self.skillStartTime = 0;

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
    
        # 잔상
        self.afterImages = [];

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
        # 잔상 그리기
        now = time.time();
        for image, pos, createdTime, in self.afterImages[:]:
            if now - createdTime > 0.3: # 잔상 지속 시간
                self.afterImages.remove((image, pos, createdTime));
                continue;
            tempImage = image.copy();
            tempImage.set_alpha(100);
            screen.blit(tempImage, pos);
        
        screen.blit(self.image[self.heading], (self.x, self.y));
    
    def attack(self, bullets):
        if self.isDodging:
            return;

        from .Bullet import Bullet;
        self.isAttack = True;
        # 몇발 쐈는지 체크하는 변수
        self.shots += 1;
        bullets.append(Bullet(self, self.x + self.centerX, "normalAttack"));

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
    def dodge(self, direction):
        if self.dodgeTimer > 0:
            return;

        self.isDodging = True;
        self.isInvincible = True;
        self.invincibleTime = self.invincibleDuration;

        self.dodgeStartTime = time.time();

        if direction == "left" and self.x > 0:
            self.dodgeDirection = -1;
        elif direction == "right" and self.x < Screen().getWidth() - self.size:
            self.dodgeDirection = 1;
        
        # 타이머
        self.dodgeTimer = self.dodgeCooldown;
    
        afterImage = (self.image[self.heading].copy(), (self.x, self.y), time.time());
        self.afterImages.append(afterImage);
    
    # 특수 스킬
    def allAttackSkill(self, bullets):
        if self.skillTimer > 0 or self.isUsingSkill:
            return;

        self.isUsingSkill = True;
        self.skillStartTime = time.time();
        self.skillTimer = self.skillCooldown;
    
        from .Bullet import Bullet
        for offset in range(0, Screen().getWidth(), 10):
            bullets.append(Bullet(self, offset, "allAttackSkill"));

    # 자체 업데이트
    def update(self, deltaTime):
        if self.isDodging:
            if time.time() - self.dodgeStartTime < self.dodgeTime:  # Dodge가 끝날 때까지
                new_x = self.x + self.dodgeDirection * self.dodgeSpeed * deltaTime;

                # 벽 충돌 감지
                if new_x < 0:  # 왼쪽 벽
                    new_x = 0;
                    self.isDodging = False;  # 회피 종료
                elif new_x > Screen().getWidth() - self.size:  # 오른쪽 벽
                    new_x = Screen().getWidth() - self.size;
                    self.isDodging = False;  # 회피 종료
                
                self.x = new_x;  # 최종적으로 x 값 설정

                self.x += self.dodgeDirection * self.dodgeSpeed * deltaTime;  # x 값을 점진적으로 변경
                if time.time() - self.lastAfterImageTime > 0.05:  # 간격을 두고 잔상 추가
                    afterImage = (self.image[self.heading].copy(), (self.x, self.y), time.time());
                    self.afterImages.append(afterImage);
                    self.lastAfterImageTime = time.time();
            else:
                self.isDodging = False;  # Dodge 종료
                self.dodgeDirection = 0;
        
        # 무적 시간
        if self.isInvincible:
            self.invincibleTime -= deltaTime;
            if self.invincibleTime <= 0:
                self.isInvincible = False;

        if self.dodgeTimer > 0:
            self.dodgeTimer -= deltaTime;

        # update 함수 안에 필살기 처리 추가
        if self.isUsingSkill:
            if time.time() - self.skillStartTime > self.skillDuration:
                self.isUsingSkill = False;

        if self.skillTimer > 0:
            self.skillTimer -= deltaTime;

