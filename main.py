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

# 색상 선언
black = (0,0,0);

# 리스트
monster = MobFly();

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT :
            sys.exit();

    screen.fill(black);
    monster.draw(screen);

    pygame.display.update();