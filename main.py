import os, pygame, sys, time, random;
import pygame.locals;

from pygame.image import load;

# 사용자 지정 객체
from Resource.Data.Screen import Screen;
from Resource.Data.Color import Color;

from Resource.Entity.MobFly import MobFly;
from Resource.Entity.MobBee import MobBee;
from Resource.Entity.MobWater import MobWater;
from Resource.Entity.Player import Player;

from Resource.System.PathLoader import imageLoader;

class Game:
    def __init__(self):
        # main.py를 기준으로 경로 설정
        os.chdir(os.path.dirname(os.path.abspath(__file__)));
        
        # 기초 설정
        pygame.init();
        pygame.display.set_caption("벌레 전사 2 - 또 다른 모험의 시작");

        self.clock = pygame.time.Clock();
        self.screen = pygame.display.set_mode(Screen().getSize());

        # Time
        self.lastSpawnTime = 0;
        self.lastBulletTime = 0;
        self.prevTime = time.time();

        # Status
        self.inGame = True;
        self.misses = 0;
        self.isDeath = False;
        self.isTitle = False;

        # 글꼴 정의
        self.defaultFont = pygame.font.Font("Resource/Ui/Font/NanumBarunGothic.ttf", 20);

        # 이미지 정의
        self.titleImage = load(imageLoader("title_0.png"));
        self.gameOverImage = load(imageLoader("game_over.png")); # 임시 이미지

        # 오브젝트
        self.monsters = [];
        self.player = Player();
        self.bullets = [];

    def createButtons(self, buttonTexts, mousePos):
        buttons = []

        for i, text in enumerate(buttonTexts):
            btnRect = pygame.Rect(0, 0, 250, 60);
            btnRect.center = (Screen().getCenterX(), Screen().getCenterY() + i * 80);

            mousePos = pygame.mouse.get_pos();

            isHover = btnRect.collidepoint(mousePos);
            bgColor = Color().gray() if isHover else Color().white();
            textColor = Color().white() if isHover else Color().black();

            btnSurface = self.defaultFont.render(text, True, textColor);
            buttons.append((btnSurface, btnRect, text, bgColor));

        return buttons;

    def title(self):
        buttonTexts = ["게임 시작", "게임 설명", "게임 종료"];
    
        while True:
            mousePos = pygame.mouse.get_pos();

            # 버튼 생성
            buttons = self.createButtons(buttonTexts, mousePos);

            self.screen.fill(Color().lightGray());

            # 타이틀 이미지
            self.screen.blit(self.titleImage, (
                Screen().getCenterX() - self.titleImage.get_width() // 2,
                Screen().getCenterY() // 2 - self.titleImage.get_height() // 2
            ));

            # 버튼들
            for surface, rect, _, bgColor in buttons:
                # 배경색 (hover 여부에 따라 바뀜)
                pygame.draw.rect(self.screen, bgColor, rect, border_radius=10);

                # 테두리
                pygame.draw.rect(self.screen, Color().black(), rect, 3, border_radius=10);

                # 텍스트
                self.screen.blit(surface, (
                    rect.centerx - surface.get_width() // 2,
                    rect.centery - surface.get_height() // 2
                ));

            pygame.display.update();     

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit();
                elif event.type == pygame.MOUSEMOTION:
                    mousePos = pygame.mouse.get_pos();
                    buttons = [];
                    self.createButtons(buttonTexts, mousePos);
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos();
                    for _, rect, label, _ in buttons:
                        if rect.collidepoint(mousePos):
                            if label == "게임 시작":
                                return;
                            elif label == "게임 설명":
                                return;
                            elif label == "게임 종료":
                                pygame.quit();
                                sys.exit();

    # 리셋
    def reset(self):
        self.monsters = [];
        self.player = Player();
        self.bullets = [];
        self.misses = 0;
        self.isDeath = False;
        self.lastSpawnTime = time.time();
        self.lastBulletTime = time.time();

    def spawnMonsters(self):
        now = time.time();
        # 몬스터 스폰
        if now - self.lastSpawnTime > 0.5 :
            selectedMonster = random.randint(1, 8);
            # 개체수 랜덤
            spawnValue = random.randint(1, 4);
            for _ in range(spawnValue):
                if selectedMonster == 1:
                    self.monsters.append(MobBee(self.player));
                elif selectedMonster == 2:
                    self.monsters.append(MobWater());
                else:
                    self.monsters.append(MobFly());
            self.lastSpawnTime = now;

    def handleEvents(self):
        # 게임 종료
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                self.inGame = False;
                pygame.quit();
                sys.exit();
            # 공격 종료 감지
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    self.player.idle();

    def update(self, deltaTime):
        # 키 입력 감지
        pressedKeys = pygame.key.get_pressed();
    
        # 탄막 발사
        if time.time() - self.lastBulletTime > 0.15:
            if pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_SPACE]:
                self.player.attack(self.bullets);
                self.lastBulletTime = time.time();

        # 이동 및 회피
        self.player.move(pressedKeys, deltaTime);

        if pressedKeys[pygame.K_LCTRL]:
            if pressedKeys[pygame.K_LEFT]:
                self.player.dodge("left", deltaTime);
            elif pressedKeys[pygame.K_RIGHT]:
                self.player.dodge("right", deltaTime);
        
        self.player.update(deltaTime);

        # 탄막 움직임
        i = 0;
        while i < len(self.bullets):
            self.bullets[i].move(deltaTime);
            self.bullets[i].draw(self.screen);
            if self.bullets[i].offScreen():
                del self.bullets[i];
                self.misses += 1;
                continue;
            i += 1;

        # 몬스터 움직임
        i = 0;
        while i < len(self.monsters):
            self.monsters[i].move(deltaTime);
            self.monsters[i].draw(self.screen);
            if self.monsters[i].offScreen() or self.monsters[i].isDamaged:
                del self.monsters[i];
                continue;
            i += 1;
            
        self.handleCollisions();

    # 충돌 체크
    def handleCollisions(self):
        # Monster
        i = 0;
        while i < len(self.monsters):
            j = 0;
            while j < len(self.bullets):
                if self.monsters[i].takeHit(self.bullets[j]):
                    del self.monsters[i];
                    del self.bullets[j];
                    i -= 1;
                    break;
                j += 1;
            i += 1;

        # Player
        for monster in self.monsters:
            if self.player.hitBy(monster):
                if not monster.isDamaged:
                    self.isDeath = self.player.damage(monster);
                    monster.isDamaged = True;
                    if self.isDeath:
                        self.screen.blit(self.gameOverImage, (Screen().getCenterX() - 50, Screen().getCenterY() - 50));
                        while True:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    sys.exit();
                            pygame.display.update();
    def run(self):
        # 타이틀 먼저
        if not self.isTitle:
            self.title();
            self.isTitle = True;
        
        # 메인 루프
        while self.inGame:
            # DeltaTime
            now = time.time();
            deltaTime = now - self.prevTime;
            self.prevTime = now;

            self.handleEvents();
            self.spawnMonsters();

            self.screen.fill(Color().customYellow());
            self.update(deltaTime);
            self.player.draw(self.screen);

            pygame.display.update();

if __name__ == "__main__":
    game = Game();
    game.run();