import pygame

# Инициализация Pygame
pygame.init()

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Определение размеров окна
WINDOW_SIZE = (800, 600)

# Создание окна
screen = pygame.display.set_mode(WINDOW_SIZE)

# Заголовок окна
pygame.display.set_caption("Дорожная сеть города")

# Определение параметров светофоров
LIGHT_RADIUS = 5
LIGHT_MARGIN = 5
LIGHT_VERTICAL_OFFSET = 5

# Основной цикл программы
done = False
while not done:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Заливка экрана белым цветом
    screen.fill(WHITE)

    # Рисование горизонтальных линий дорог
    for y in range(0, WINDOW_SIZE[1], 150):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_SIZE[0], y), 5)

    # Рисование вертикальных линий дорог
    for x in range(0, WINDOW_SIZE[0], 150):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_SIZE[1]), 5)

    # Рисование светофоров на перекрестках
    for x in range(50, WINDOW_SIZE[0], 100):
        for y in range(50, WINDOW_SIZE[1], 100):
            pygame.draw.circle(screen, BLACK, (x, y + LIGHT_VERTICAL_OFFSET), LIGHT_RADIUS)
            pygame.draw.circle(screen, BLACK, (x + LIGHT_MARGIN + LIGHT_RADIUS * 2, y + LIGHT_VERTICAL_OFFSET), LIGHT_RADIUS)
            pygame.draw.circle(screen, BLACK, (x + LIGHT_MARGIN * 2 + LIGHT_RADIUS * 4, y + LIGHT_VERTICAL_OFFSET), LIGHT_RADIUS)
            pygame.draw.circle(screen, RED, (x, y + LIGHT_VERTICAL_OFFSET), LIGHT_RADIUS)
            pygame.draw.circle(screen, GREEN, (x + LIGHT_MARGIN + LIGHT_RADIUS * 2, y + LIGHT_VERTICAL_OFFSET), LIGHT_RADIUS)
            pygame.draw.circle(screen, BLACK, (x + LIGHT_MARGIN * 2 + LIGHT_RADIUS * 4, y + LIGHT_VERTICAL_OFFSET), LIGHT_RADIUS)

    # Обновление экрана
    pygame.display.flip()

# Закрытие Pygame
pygame.quit()
