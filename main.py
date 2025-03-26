import os, pygame, sys, random, time;
import pygame.locals;

# 사용자 지정 객체
from Resource.Data.Screen import Screen;
from Resource.Entity.MobFly import MobFly;
from Resource.Entity.Player import Player;

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
inGame = True;

# Color
black = (0,0,0);
customYellow = (255, 199, 30);
customGreen = (168, 255, 108);

# Moveable Object
monsters = [];
player = Player();

# Reset Function
def resetGame():
    global monsters, player;

    monsters = [];
    player = Player();

# Main Loop
while inGame:
    # DeltaTime
    now = time.time();
    deltaTime = now - prevTime;
    prevTime = now;

    # Game Quit
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT :
            inGame = False;
            sys.exit();
    
    # Pressed Key
    pressed_keys = pygame.key.get_pressed();

    # Monster Spawn
    if now - lastSpawnTime > 0.5 :
        monsters.append(MobFly());
        lastSpawnTime = now;

    # Background
    screen.fill(customYellow);
    
    # Player Movement
    player.move(pressed_keys, deltaTime);
    player.draw(screen);

    # Monster Movement
    i = 0;
    while i < len(monsters):
        monsters[i].move(deltaTime);
        monsters[i].draw(screen);
        if monsters[i].offScreen():
            del monsters[i];
            i -= 1;
        i += 1;


    pygame.display.update();