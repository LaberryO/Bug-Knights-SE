import os, pygame, sys, random, time;
import pygame.locals;

# 사용자 지정 객체
from Resource.Data.Screen import Screen;
from Resource.Entity.MobFly import MobFly;

# main.py를 기준으로 경로 설정
os.chdir(os.path.dirname(os.path.abspath(__file__)));

# 기초 설정
pygame.init();
pygame.display.set_caption("벌레 전사 2 - 또다른 모험의 시작");
clock = pygame.time.Clock();
screen = pygame.display.set_mode(Screen().getSize());

# 변수 초기화
lastSpawnTime = 0;
prevTime = time.time();

# 색상 선언
black = (0,0,0);

# 리스트
monsters = [];

# 리셋
def resetGame():
    global monsters;

    monsters = [];

# 게임 루프
while True:
    # 델타 타임
    now = time.time();
    deltaTime = now - prevTime;
    prevTime = now;

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT :
            sys.exit();
    
    if now - lastSpawnTime > 0.5 :
        monsters.append(MobFly());
        lastSpawnTime = now;

    screen.fill(black);
    
    i = 0;
    while i < len(monsters):
        monsters[i].move(deltaTime);
        monsters[i].draw(screen);
        if monsters[i].offScreen():
            del monsters[i];
            i -= 1;
        i += 1;


    pygame.display.update();