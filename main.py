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
        pygame.display.set_caption("Bug Knights Shooter Edition - 벌레 전사의 새로운 모험");

        self.clock = pygame.time.Clock();
        self.screen = pygame.display.set_mode(Screen().getSize());

        self.score = 0;
        self.lastScore = 0;
        self.maxScore = 0;

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

    def createButtons(self, buttonTexts, mousePos, y):
        buttons = []

        for i, text in enumerate(buttonTexts):
            btnRect = pygame.Rect(0, 0, 250, 60);
            btnRect.center = (Screen().getCenterX(), y + i * 80);

            mousePos = pygame.mouse.get_pos();

            isHover = btnRect.collidepoint(mousePos);
            bgColor = Color().gray() if isHover else Color().white();
            textColor = Color().white() if isHover else Color().black();

            btnSurface = self.defaultFont.render(text, True, textColor);
            buttons.append((btnSurface, btnRect, text, bgColor));

        return buttons;

    def midTextRender(self, text, addY):
        self.screen.blit(text, (
            Screen().getCenterX() - text.get_width() // 2,
            Screen().getCenterY() + addY
        ));

    # 타이틀 화면
    def title(self):
        buttonTexts = ["게임 시작", "게임 설명", "게임 종료"];
    
        while True:
            mousePos = pygame.mouse.get_pos();

            # 버튼 생성
            buttons = self.createButtons(buttonTexts, mousePos, Screen().getCenterY());

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
            
            lastScoreText = f"Last Score: {self.lastScore}";
            lastScoreSurface = self.defaultFont.render(lastScoreText, True, Color().black());
            self.screen.blit(lastScoreSurface, (10, 10));

            MaxScoreText = f"Max Score: {self.maxScore}";
            MaxScoreSurface = self.defaultFont.render(MaxScoreText, True, Color().black());
            self.screen.blit(MaxScoreSurface, (10, 30));

            pygame.display.update();     

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit();
                elif event.type == pygame.MOUSEMOTION:
                    mousePos = pygame.mouse.get_pos();
                    buttons = [];
                    self.createButtons(buttonTexts, mousePos, Screen().getCenterY());
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos();
                    for _, rect, label, _ in buttons:
                        if rect.collidepoint(mousePos):
                            if label == "게임 시작":
                                return;
                            elif label == "게임 설명":
                                self.gameInfo();
                            elif label == "게임 종료":
                                pygame.quit();
                                sys.exit();
    
    # 게임 설명 화면
    def gameInfo(self):
        infoTexts = [
            "벌레 전사의 새로운 모험을 다룬 슈팅게임입니다!",
            "최대한 많은 벌레를 죽이고 그들의 정점에 서십시오!",
            "← : 왼쪽으로 이동합니다.",
            "→ : 오른쪽으로 이동합니다.",
            "↑ 또는 Space Bar : 거미줄을 발사합니다.",
            "LCTRL + ← 또는 LCTRL + →",
            "진행 방향으로 구릅니다. (일시적으로 무적 상태가 됩니다.)",
            "LSHIFT : 필살기를 사용합니다.",
            "ESC를 눌러 돌아갑니다..."
        ];

        while True:
            self.screen.fill(Color().white());
            tempY = -270;

            for i in range(len(infoTexts)):
                text = self.defaultFont.render(infoTexts[i], True, Color().black());
                if i == 2 or i == 8:
                    tempY += 90;
                else:
                    tempY += 40;
                self.midTextRender(text, tempY);

            pygame.display.update();

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit();
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return;  # title() 루프로 복귀

    # 게임 오버
    def gameOver(self):
        texts = [
            "벌레 전사는 최후를 맞이했습니다.",
            "Score",
            f"당신의 전사는 {self.score}의 명성을 얻었습니다.",
            "Miss",
            f"당신의 전사는 {self.misses}번 빗맞췄습니다."
        ];

        buttonsTexts = [
            "타이틀로",
            "게임 종료"
        ];

        while True:
            mousePos = pygame.mouse.get_pos();

            # 버튼 생성
            buttons = self.createButtons(buttonsTexts, mousePos, Screen().getCenterY() + 100);

            self.screen.fill(Color().white());

            # 결과 문구
            tempY = -270;
            for i in range(len(texts)):
                text = self.defaultFont.render(texts[i], True, Color().black());
                if i == 1:
                    tempY += 90;
                elif i == 2 or i == 4:
                    tempY += 20;
                else:
                    tempY += 40;
                
                self.midTextRender(text, tempY);
            
            # 버튼
            for surface, rect, __, bgColor in buttons:
                # 배경색
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
                    self.createButtons(buttonsTexts, mousePos, Screen().getCenterY() + 100);
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos();
                    for _, rect, label, _ in buttons:
                        if rect.collidepoint(mousePos):
                            if label == "타이틀로":
                                self.reset();
                                self.title();
                                self.run();
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
        self.score = 0;

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
    
    # 체력 바
    def drawHealthBar(self, surface, x, y, width, height, currentHealth, maxHealth):
        x -= width;
        # 백그라운드 바 (회색)
        pygame.draw.rect(surface, Color().gray(), (x, y, width, height), border_radius=5);

        # 체력 비율 계산
        healthRatio = max(0, currentHealth / maxHealth);  # 0 미만으로 안 내려가게
        currentWidth = int(width * healthRatio);

        # 실제 체력 바 (빨간색)
        pygame.draw.rect(surface, Color().red(), (x, y, currentWidth, height), border_radius=5);

        # 테두리
        pygame.draw.rect(surface, Color().black(), (x, y, width, height), 2, border_radius=5);

    # 메인 루프
    def update(self, deltaTime):
        # Score 표시
        scoreText = self.defaultFont.render(f"Score : {self.score}", True, Color().black());
        self.screen.blit(scoreText, (10, 10));

        if self.score >= self.maxScore:
            scoreColor = Color().red();
            self.maxScore = self.score;
        else:
            scoreColor = Color().black();
        
        maxScoreText = self.defaultFont.render(f"Max Score : {self.maxScore}", True, scoreColor);
        self.screen.blit(maxScoreText, (10, 30));

        # 체력 표시
        self.drawHealthBar(
            surface=self.screen,
            x = Screen().getWidth(),
            y = 10,
            width=200,
            height=25,
            currentHealth=self.player.health,
            maxHealth=5
        );

        # 스킬 쿨타임 표시
        if self.player.skillTimer > 0:
            cooldownText = self.defaultFont.render(f"스킬 상태 : {self.player.skillTimer:.1f}초 남음", True, Color().black());
        else:
            cooldownText = self.defaultFont.render("스킬 상태 : 준비됨!", True, Color().red());
        self.screen.blit(cooldownText, (10, 50));

        # 키 입력 감지
        pressedKeys = pygame.key.get_pressed();
    
        # 탄막 발사
        if time.time() - self.lastBulletTime > 0.15:
            if pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_SPACE]:
                self.player.attack(self.bullets);
                self.lastBulletTime = time.time();
        
        if pressedKeys[pygame.K_LSHIFT]:
            self.player.allAttackSkill(self.bullets);

        # 이동 및 회피
        self.player.move(pressedKeys, deltaTime);

        if pressedKeys[pygame.K_LCTRL]:
            if pressedKeys[pygame.K_LEFT]:
                self.player.dodge("left");
            elif pressedKeys[pygame.K_RIGHT]:
                self.player.dodge("right");
        
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
                    # Score
                    if isinstance(self.monsters[i], MobFly):
                        self.score += 1000;
                    elif isinstance(self.monsters[i], MobBee):
                        self.score += 5000;
                    elif isinstance(self.monsters[i], MobWater):
                        self.score += 10000;
                    
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
                        if self.score > self.maxScore:
                            self.maxScore = self.score;
                        self.lastScore = self.score;
                        self.gameOver();
    


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