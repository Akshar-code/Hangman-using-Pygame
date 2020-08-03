import pygame
import math
import random
from pygame import mixer

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hangman')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
# Setting up a Font
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
title = TITLE_FONT.render('HANGMAN', 1, BLACK)
# Background images
background_image = pygame.image.load('background.jpg')
# laod images
images = []
for i in range(7):
    image = pygame.image.load('hangman' + str(i) + '.png')
    images.append(image)

# button Variables
RADIUS = 20
GAP = 15
letters = []
start_x = round((WIDTH - (GAP + RADIUS * 2) * 13) / 2)
start_y = 400
A = 65
for i in range(26):
    x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((GAP + (RADIUS * 2)) * (i // 13))
    letters.append([x, y, chr(A + i), True])

# game variables
hangman_status = 0
guessed = []
words = ['FORD', 'HYUNDAI', 'MARUTI', 'MAHINDRA', 'TATA', 'TOYOTA', 'CHEVROLET']
word = random.choice(words)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw():
    window.blit(background_image, (0, 0))
    window.blit(title, (WIDTH / 2 - title.get_width() / 2, 20))
    # drawing buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            window.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
    # Drawing words
    display_word = ''
    for letter in word:
        if letter in guessed:
            display_word += letter + ' '
        else:
            display_word += '_ '
        text = WORD_FONT.render(display_word, 1, BLACK)
        window.blit(text, (400, 200))
    window.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    window.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def display_intro(message):
    window.fill(WHITE)
    title = TITLE_FONT.render(message, 1, BLACK)
    window.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 2 - title.get_height() / 2))
    ah_shit = mixer.Sound('ah_shit.mp3')
    ah_shit.play()
    pygame.display.update()


def main():
    # Setup Game loop
    global hangman_status
    FPS = 60
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            pygame.display.update()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        distance = math.sqrt((x - mouse_x) ** 2 + (y - mouse_y) ** 2)
                        if distance < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
                                oof = mixer.Sound('oof.mp3')
                                oof.play()
                            else:
                                wow = mixer.Sound('wow.mp3')
                                wow.play()
        draw()
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            epic_sax = mixer.Sound('epic_sax.mp3')
            epic_sax.play()
            display_message('You WON')
            pygame.time.delay(8000)
            display_intro('Do you want to play?')
            break

        if hangman_status == 6:
            display_message('You LOST')
            not_fine = mixer.Sound('not_really_fine.mp3')
            not_fine.play()
            pygame.time.delay(8000)
            display_intro('Do you want to play?')
            break


run_game = True
while run_game:
    display_intro('Do you want to play?')
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            main()
            # game variables
            hangman_status = 0
            guessed = []
            words = ['FORD', 'HYUNDAI', 'MARUTI', 'MAHINDRA', 'TATA', 'TOYOTA', 'CHEVROLET']
            word = random.choice(words)
            for letter in letters:
                letter[3] = True
        elif event.type == pygame.QUIT:
            run_game = False

pygame.quit()
