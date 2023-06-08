import pygame
from random import randrange as rnd

def win_menu():
    menu = True
    selected = "quit"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                menu = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        menu = False
                    if selected == "quit":
                        pygame.quit()
                        quit()

        screen.fill((50, 50, 120))
        title = text_format("YOU WIN!", font, 90, (0, 150, 200))
        if selected == "quit":
            text_quit = text_format("QUIT", font, 75, (255, 255, 255))
        else:
            text_quit = text_format("QUIT", font, 75, (0, 0, 0))

        title_rect = title.get_rect()
        quit_rect = text_quit.get_rect()

        screen.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_quit, (WIDTH / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        clock.tick(fps)
        pygame.display.set_caption("menu")


def lose_menu():
    menu = True
    selected = "quit"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                menu = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        menu = False
                    if selected == "quit":
                        pygame.quit()
                        quit()

        screen.fill((50, 50, 120))
        title = text_format("GAME OVER", font, 90, (0, 150, 200))
        if selected == "quit":
            text_quit = text_format("QUIT", font, 75, (255, 255, 255))
        else:
            text_quit = text_format("QUIT", font, 75, (0, 0, 0))

        title_rect = title.get_rect()
        quit_rect = text_quit.get_rect()

        screen.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_quit, (WIDTH / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        clock.tick(fps)
        pygame.display.set_caption("Game over menu")


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


def main_menu():
    menu = True
    selected = "start"

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        menu = False
                    if selected == "quit":
                        pygame.quit()
                        quit()

        screen.fill((50, 50, 120))
        title = text_format("Arkanoid", font, 90, (0, 150, 200))
        if selected == "start":
            text_start = text_format("START NEW GAME", font, 75, (255, 255, 255))
        else:
            text_start = text_format("START NEW GAME", font, 75, (0, 0, 0))
        if selected == "quit":
            text_quit = text_format("QUIT", font, 75, (255, 255, 255))
        else:
            text_quit = text_format("QUIT", font, 75, (0, 0, 0))

        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        screen.blit(title, (WIDTH / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_start, (WIDTH / 2 - (start_rect[2] / 2), 300))
        screen.blit(text_quit, (WIDTH / 2 - (quit_rect[2] / 2), 360))
        pygame.display.update()
        clock.tick(fps)
        pygame.display.set_caption("Arkanoid menu")


def collisium(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top
    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx

    return dx, dy


pygame.init()
SIZE = (WIDTH, HEIGHT) = (1200, 800)
fps = 60
font = "Font/Retro.ttf"

paddle_wight = 220
paddle_height = 35
paddle_speed = 11
paddle = pygame.Rect(WIDTH // 2 - paddle_wight // 2, HEIGHT - paddle_height - 10, paddle_wight, paddle_height)

ball_radius = 20
ball_speed = 0
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

sound_paddle = pygame.mixer.Sound('Sound/paddle.mp3')
sound_block = pygame.mixer.Sound('Sound/block.mp3')

block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(254, 255), rnd(254, 255), rnd(0, 1)) for i in range(10) for j in range(4)]

brek = 0
score = 0
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
background = pygame.image.load('images/back.png')

main_menu()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.blit(background, (0, 0))

    [pygame.draw.rect(screen, pygame.Color('orange'), block) for color, block in enumerate(block_list)]
    pygame.draw.rect(screen, pygame.Color('grey'), paddle)
    pygame.draw.circle(screen, pygame.Color('yellow'), ball.center, ball_radius)

    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
        sound_paddle.play()

    if ball.centery < ball_radius:
        dy = -dy
        sound_paddle.play()

    if ball.colliderect(paddle) and dy > 0:
        dx, dy = collisium(dx, dy, ball, paddle)
        sound_paddle.play()

    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        sound_block.play()
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = collisium(dx, dy, ball, hit_rect)
        hit_rect.inflate_ip(ball.width * 1.5, ball.height * 1.5)
        pygame.draw.rect(screen, hit_color, hit_rect)
        ball_speed += 0.2
        score += 1

    if ball.bottom > HEIGHT:
        lose_menu()
        exit()

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed


    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    if key[pygame.K_SPACE]:
        ball_speed = 5
        brek = 1

    if brek == 0:
        inf = text_format("Press <SPACE>", font, 50, (0, 200, 0))
        inf_rect = inf.get_rect()
        screen.blit(inf, (500, 580))

    if score == 40:
        win_menu()

    pygame.display.flip()
    clock.tick(fps)
