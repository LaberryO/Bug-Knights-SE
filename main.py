import os, pygame, sys, time;
import pygame.locals;

# 사용자 지정 객체
from Resource.Data.Screen import Screen;
from Resource.Entity.MobFly import MobFly;
from Resource.Entity.Player import Player;
# from Resource.Entity.Bullet import Bullet;

# main.py를 기준으로 경로 설정
os.chdir(os.path.dirname(os.path.abspath(__file__)));

# 기초 설정
pygame.init();
pygame.display.set_caption("벌레 전사 2 - 또 다른 모험의 시작");
clock = pygame.time.Clock();
screen = pygame.display.set_mode(Screen().getSize());

# 변수 초기화
lastSpawnTime = 0;
lastBulletTime = 0;
prevTime = time.time();
inGame = True;
misses = 0;

# 글꼴 정의
defaultFont = pygame.font.Font("Resoruce/Ui/Font/NanumBarunGothic.ttf", 20);

# 색상 정의
black = (0,0,0);
customYellow = (255, 199, 30);
customGreen = (168, 255, 108);

# Moveable Object
monsters = [];
player = Player();
bullets = [];

# 리셋
def resetGame():
    global monsters, player, bullets, misses;

    monsters = [];
    player = Player();
    bullets = [];
    misses = 0;

# 메인 루프
while inGame:
    # DeltaTime
    now = time.time();
    deltaTime = now - prevTime;
    prevTime = now;

    # 게임 종료
    for event in pygame.event.get():
        if event.type == pygame.QUIT :
            inGame = False;
            sys.exit();
        # 공격 종료 감지
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                player.idle();
    
    # 키 입력 감지
    pressedKeys = pygame.key.get_pressed();

    # 탄막 발사
    if now - lastBulletTime > 0.1:
        if pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_SPACE]:
            player.attack(bullets);
            lastBulletTime = now;

    # 몬스터 스폰
    if now - lastSpawnTime > 0.5 :
        monsters.append(MobFly());
        lastSpawnTime = now;

    # 뒷 배경
    screen.fill(customYellow);
    
    # 탄막 움직임
    i = 0;
    while i < len(bullets):
        bullets[i].move(deltaTime);
        bullets[i].draw(screen);
        if bullets[i].offScreen():
            del bullets[i];
            misses += 1;
            continue;
        i += 1;
    
    # 플레이어 움직임
    player.move(pressedKeys, deltaTime);
    player.draw(screen);

    # 몬스터 움직임
    i = 0;
    while i < len(monsters):
        monsters[i].move(deltaTime);
        monsters[i].draw(screen);
        if monsters[i].offScreen():
            del monsters[i];
            continue;
        i += 1;

    pygame.display.update();