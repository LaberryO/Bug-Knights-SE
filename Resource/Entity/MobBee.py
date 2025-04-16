from ..Data.Screen import Screen;
from ..System.PathLoader import imageLoader;
from ..System.ImageEditor import rescale;
from .Monster import Monster;

import math, time;

# 벌 (몬스터)
class MobBee(Monster):
    def __init__(self, player):
        super().__init__();

        # MobBee Init
        self.hitSpeed = 2.5; # 벌이 플레이어에게 돌진하는 속도
        self.detectRange = Screen().getCenterY(); # 감지 범위
        self.alertTime = 1.0; # 경고 시간 (초)
        self.alertStart = None; # 경고 시작
        self.state = "idle"; # 현재 상태 idle : 배회, alert : 경고, chase : 추격
        self.direction = None;

        self.player = player;

        # Image
        self.image = [
            rescale(imageLoader("mobBee_0.png"), self.size),
            rescale(imageLoader("mobBee_1.png"), self.size)
        ];

        self.alertImage = rescale(imageLoader("mobBee_2.png"), self.size);
    def move(self, deltaTime):
        target_x = self.player.x + self.player.size / 2;
        target_y = self.player.y + self.player.size / 2;
        bee_x = self.x + self.size / 2;
        bee_y = self.y + self.size / 2;

        dx = target_x - bee_x;
        dy = target_y - bee_y;
        distance = math.sqrt(dx**2 + dy**2);

        if self.state == "idle":
            # 감지 범위 안에 들어오면 경고 상태로 전환
            if distance < self.detectRange:
                self.state = "alert";
                self.alertStart = time.time();  # 경고 시작 시간 기록
            else:
                self.dy += self.accSpeed;  # 가속도가 적용되어 속도 증가
                self.y += self.dy * deltaTime;  # 가속도에 의한 위치 업데이트
        
        elif self.state == "alert":
            # 경고 시간이 지나면 돌진 방향을 설정하고 charge 상태로 전환
            if time.time() - self.alertStart >= self.alertTime:
                if distance > 0:
                    dx /= distance;
                    dy /= distance;
                self.direction = (dx, dy);  # 돌진 방향 고정
                self.state = "charge";

        elif self.state == "charge":
            accSpeed = self.accSpeed * 3;
            self.hitSpeed += accSpeed;
            # 고정된 방향으로 직진 돌진
            self.x += self.direction[0] * self.hitSpeed * deltaTime;
            self.y += self.direction[1] * self.hitSpeed * deltaTime;
    
        super().move(deltaTime);

    def draw(self, screen):
        if self.state == "alert":
            screen.blit(self.alertImage, (self.x, self.y));
        else:
            super().draw(screen);

    def offScreen(self):
        return super().offScreen();

    def takeHit(self, bullets):
        return super().takeHit(bullets);