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

# Игрок
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 5

# Враги
enemy_size = 30
enemies = []

# Счет
score = 0
font = pygame.font.Font(None, 36)

# Функция для создания нового врага
def create_enemy():
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        x = random.randint(0, WIDTH - enemy_size)
        y = -enemy_size
    elif side == 'bottom':
        x = random.randint(0, WIDTH - enemy_size)
        y = HEIGHT
    elif side == 'left':
        x = -enemy_size
        y = random.randint(0, HEIGHT - enemy_size)
    else:
        x = WIDTH
        y = random.randint(0, HEIGHT - enemy_size)
    return {'x': x, 'y': y}

# Основной игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
        player_y += player_speed

    # Создание новых врагов
    if random.randint(1, 30) == 1:
        enemies.append(create_enemy())

    # Обновление позиций врагов и проверка столкновений
    for enemy in enemies[:]:
        if enemy['x'] < player_x:
            enemy['x'] += 2
        elif enemy['x'] > player_x:
            enemy['x'] -= 2
        if enemy['y'] < player_y:
            enemy['y'] += 2
        elif enemy['y'] > player_y:
            enemy['y'] -= 2

        # Проверка столкновения
        if (player_x < enemy['x'] + enemy_size and
            player_x + player_size > enemy['x'] and
            player_y < enemy['y'] + enemy_size and
            player_y + player_size > enemy['y']):
            running = False

    # Увеличение счета
    score += 1

    # Отрисовка
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy['x'], enemy['y'], enemy_size, enemy_size))

    # Отображение счета
    score_text = font.render(f"Счет: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()