from ..Data.Screen import Screen;
from ..System.PathLoader import ImageLoader;
import random, pygame, os;

# 파리 (몬스터)
class MobFly:
    # 초기값 설정
    def __init__(self):
        self.x = random.randint(0, Screen().getWidth());
        self.y = 100;

        # Image
        self.image = [
            pygame.image.load(ImageLoader("mobFly_0.png")),
            pygame.image.load(ImageLoader("mobFly_1.png"))
        ];
    def draw(self, screen):
        screen.blit(self.image[0], (self.x, self.y));

        