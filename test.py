import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра на выживание")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player:
    def __init__(self, x, y, size, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed

    def move(self, dx, dy):
        if dx != 0 and dy != 0:
            dx *= 0.7071
            dy *= 0.7071
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        self.rect.clamp_ip(screen.get_rect())

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

class Enemy:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = 2

    def move(self, target):
        if self.rect.x < target.x:
            self.rect.x += self.speed
        elif self.rect.x > target.x:
            self.rect.x -= self.speed
        if self.rect.y < target.y:
            self.rect.y += self.speed
        elif self.rect.y > target.y:
            self.rect.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

class Game:
    def __init__(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2, 50, 5)
        self.enemies = []
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def create_enemy(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            x = random.randint(0, WIDTH - 30)
            y = -30
        elif side == 'bottom':
            x = random.randint(0, WIDTH - 30)
            y = HEIGHT
        elif side == 'left':
            x = -30
            y = random.randint(0, HEIGHT - 30)
        else:
            x = WIDTH
            y = random.randint(0, HEIGHT - 30)
        self.enemies.append(Enemy(x, y, 30))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.player.move(dx, dy)

        if random.randint(1, 30) == 1:
            self.create_enemy()

        for enemy in self.enemies[:]:
            enemy.move(self.player.rect)
            if self.player.rect.colliderect(enemy.rect):
                return False

        self.score += 1
        return True

    def draw(self):
        screen.fill(WHITE)
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        score_text = self.font.render(f"Счет: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

def main():
    game = Game()
    clock = pygame.time.Clock()

    running = True
    while running:
        running = game.handle_events()
        if running:
            running = game.update()
        game.draw()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()