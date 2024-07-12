import pygame
import os
from player import Player
from enemy import Enemy
from field import Field
from wall import Wall
from food import Food

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

sound_death = pygame.mixer.Sound('death.mp3')
sound_coin = pygame.mixer.Sound('coin.mp3')
sound_next = pygame.mixer.Sound('next.mp3')
sound_risa = pygame.mixer.Sound('risa.mp3')
sound_theme = pygame.mixer.Sound('theme.mp3')
sound_trompeta = pygame.mixer.Sound('trompeta.mp3')
sound_victory = pygame.mixer.Sound('victory.mp3')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

isRunning = True

font = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font('freesansbold.ttf', 24)
current_level = 1
difficulty_multiplier = 1.0
total_levels = 3
mode = 'classic'

background_gif = pygame.image.load('background.gif')
background_gif = pygame.transform.scale(background_gif, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def main_menu():
    click = False
    while True:
        screen.blit(background_gif, (0, 0))
        draw_text('Main Menu', font, (255, 255, 255), screen, SCREEN_WIDTH // 2, 50)
        
        mx, my = pygame.mouse.get_pos()

        button_classic = pygame.Rect((SCREEN_WIDTH // 2) - 100, 200, 200, 50)
        button_individual = pygame.Rect((SCREEN_WIDTH // 2) - 100, 300, 200, 50)
        button_instructions = pygame.Rect((SCREEN_WIDTH // 2) - 150, 400, 300, 50)

        if button_classic.collidepoint((mx, my)):
            if click:
                difficulty_menu('classic')
        if button_individual.collidepoint((mx, my)):
            if click:
                difficulty_menu('individual')
        if button_instructions.collidepoint((mx, my)):
            if click:
                instructions_menu()

        pygame.draw.rect(screen, (255, 0, 0), button_classic)
        pygame.draw.rect(screen, (255, 0, 0), button_individual)
        pygame.draw.rect(screen, (255, 0, 0), button_instructions)
        draw_text('Classic', font, (255, 255, 255), screen, button_classic.centerx, button_classic.centery)
        draw_text('Individual', font, (255, 255, 255), screen, button_individual.centerx, button_individual.centery)
        draw_text('Instrucciones', font, (255, 255, 255), screen, button_instructions.centerx, button_instructions.centery)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def difficulty_menu(selected_mode):
    global mode
    click = False
    mode = selected_mode
    while True:
        screen.blit(background_gif, (0, 0))
        draw_text('Select Difficulty', font, (255, 255, 255), screen, SCREEN_WIDTH // 2, 50)
        
        mx, my = pygame.mouse.get_pos()

        button_easy = pygame.Rect((SCREEN_WIDTH // 2) - 100, 200, 200, 50)
        button_medium = pygame.Rect((SCREEN_WIDTH // 2) - 100, 300, 200, 50)
        button_hard = pygame.Rect((SCREEN_WIDTH // 2) - 100, 400, 200, 50)

        if button_easy.collidepoint((mx, my)):
            if click:
                global difficulty_multiplier
                difficulty_multiplier = 0.8
                start_game()
        if button_medium.collidepoint((mx, my)):
            if click:
                difficulty_multiplier = 1.0
                start_game()
        if button_hard.collidepoint((mx, my)):
            if click:
                difficulty_multiplier = 1.2
                start_game()

        pygame.draw.rect(screen, (255, 0, 0), button_easy)
        pygame.draw.rect(screen, (255, 0, 0), button_medium)
        pygame.draw.rect(screen, (255, 0, 0), button_hard)
        draw_text('Easy', font, (255, 255, 255), screen, button_easy.centerx, button_easy.centery)
        draw_text('Medium', font, (255, 255, 255), screen, button_medium.centerx, button_medium.centery)
        draw_text('Hard', font, (255, 255, 255), screen, button_hard.centerx, button_hard.centery)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def load_level(file_path):
    walls = []
    foods = []
    enemies = []
    checkpoints = []
    field_start = None
    field_finish = None
    player_start = (0, 0)
    player_respawn = (0, 0)

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            if parts[0] == 'PlayerStart':
                player_start = (int(parts[1]), int(parts[2]))
                player_respawn = (int(parts[3]), int(parts[4]))
            elif parts[0] == 'Enemy':
                x, y, width, height = map(int, parts[1:5])
                vel = float(parts[5])
                vel = float(vel * difficulty_multiplier)
                movement_type = parts[6]
                kwargs = {}
                if movement_type == 'linearx' or movement_type == 'lineary':
                    kwargs['b1'] = int(parts[7])
                    kwargs['b2'] = int(parts[8])
                elif movement_type == 'circle':
                    kwargs['radius'] = int(parts[7])
                    kwargs['angle_vel'] = float(parts[8])
                    kwargs['angle'] = int(parts[9])
                elif movement_type == 'pattern':
                    pattern = []
                    for i in range(7, len(parts), 2):
                        pattern.append((int(parts[i]), int(parts[i+1])))
                    kwargs['pattern'] = pattern
                enemies.append(Enemy(x, y, width, height, vel, movement_type=movement_type, **kwargs))
            elif parts[0] == 'FieldStart':
                field_start = Field(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
            elif parts[0] == 'FieldFinish':
                field_finish = Field(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]))
            elif parts[0] == 'Wall':
                walls.append(Wall(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5])))
            elif parts[0] == 'Food':
                foods.append(Food(int(parts[1]), int(parts[2]), int(parts[3])))
            elif parts[0] == 'Checkpoint':
                checkpoints.append(Field(int(parts[1]), int(parts[2]), int(parts[3]), int(parts[4]), color=(0, 255, 255)))

    return player_start, player_respawn, checkpoints, enemies, field_start, field_finish, walls, foods

def load_next_level():
    global current_level, player, checkpoints, enemies, field_start, field_finish, walls, foods
    current_level += 1
    if current_level > total_levels:
        sound_theme.stop()
        sound_victory.play()
        win_screen()
    else:
        level_file = f'level{current_level}.txt'
        if os.path.exists(level_file):
            player_start, player_respawn, checkpoints, enemies, field_start, field_finish, walls, foods = load_level(level_file)
            player = Player(player_start[0], player_start[1], 16, 16, checkpoints=checkpoints)
        else:
            win_screen()

def start_game():
    global current_level
    if mode == 'classic':
        current_level = 0
        load_next_level()
        game_loop()
    elif mode == 'individual':
        level_menu()

def level_menu():
    click = False
    while True:
        screen.blit(background_gif, (0, 0))
        draw_text('Select Level', font, (255, 255, 255), screen, SCREEN_WIDTH // 2, 50)
        
        mx, my = pygame.mouse.get_pos()
        
        button_height = 50
        button_width = 200
        button_spacing = 20
        start_y = 150 

        buttons = []
        for i in range(total_levels):
            y_pos = start_y + (i * (button_height + button_spacing))
            button = pygame.Rect((SCREEN_WIDTH // 2) - (button_width // 2), y_pos, button_width, button_height)
            buttons.append(button)

            if button.collidepoint((mx, my)):
                if click:
                    load_individual_level(i + 1)

            pygame.draw.rect(screen, (255, 0, 0), button)
            draw_text(f'Level {i + 1}', font, (255, 255, 255), screen, button.centerx, button.centery)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def instructions_menu():
    click = False
    while True:
        screen.fill((0, 0, 0))
        draw_text('Instrucciones', font, (255, 255, 255), screen, SCREEN_WIDTH // 2, 50)

        instructions = [
            "1. Usa las teclas de flecha para mover al jugador.",
            "2. Evita los enemigos para no morir.",
            "3. Recoge toda la comida para avanzar.",
            "4. Llega al campo de meta para completar el nivel.",
        ]

        for i, instruction in enumerate(instructions):
            draw_text(instruction, small_font, (255, 255, 255), screen, SCREEN_WIDTH // 2, 150 + i * 40)

        mx, my = pygame.mouse.get_pos()
        button_back = pygame.Rect((SCREEN_WIDTH // 2) - 100, SCREEN_HEIGHT - 100, 300, 50)

        if button_back.collidepoint((mx, my)):
            if click:
                main_menu()

        pygame.draw.rect(screen, (255, 0, 0), button_back)
        draw_text('Regresar al Menu', font, (255, 255, 255), screen, button_back.centerx, button_back.centery)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def load_individual_level(level):
    global current_level, player, checkpoints, enemies, field_start, field_finish, walls, foods
    current_level = level
    level_file = f'level{current_level}.txt'
    if os.path.exists(level_file):
        player_start, player_respawn, checkpoints, enemies, field_start, field_finish, walls, foods = load_level(level_file)
        player = Player(player_start[0], player_start[1], 16, 16, checkpoints=checkpoints)
        game_loop(individual=True)
    else:
        print("Level not found!")

def update(individual=False):
    keys = pygame.key.get_pressed()
    player.move(keys, walls)
    for enemy in enemies:
        if enemy.movement_type == 'linearx' or enemy.movement_type == 'lineary':
            enemy.move(enemy.b1, enemy.b2)
        else:
            enemy.move()

    player_rect = player.draw(screen)
    for enemy in enemies:
        if player_rect.colliderect(enemy.draw(screen)):
            foods[:] = player.reset(foods)
            sound_death.play()
            player.deaths += 1
            break

    for food in foods[:]:
        if player_rect.colliderect(food.draw(screen)):
            foods.remove(food)
            sound_coin.play()
            player.food_collected += 1

    if player.update_checkpoint(checkpoints, foods):
        player.food_collected = len(foods)

    if player_rect.colliderect(field_finish.draw(screen)) and not foods:
        if individual:
            current_level = 1
            sound_theme.stop()
            main_menu()
        else:
            sound_next.play()
            load_next_level()

def draw():
    screen.fill((183, 175, 250))
    for checkpoint in checkpoints:
        checkpoint.draw(screen)
    if field_start:
        field_start.draw(screen)
    if field_finish:
        field_finish.draw(screen)
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for wall in walls:
        wall.draw(screen)
    for food in foods:
        food.draw(screen)

    deathCounter = font.render("Deaths: " + str(player.deaths), True, (255, 255, 255))
    screen.blit(deathCounter, (300, 50))
    
    levelCounter = font.render("Level: " + str(current_level), True, (255, 255, 255))
    screen.blit(levelCounter, (300, 10))

    surrender_button = pygame.Rect(50, SCREEN_HEIGHT - 100, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), surrender_button)
    draw_text('Me Rindo', font, (255, 255, 255), screen, surrender_button.centerx, surrender_button.centery)

    mx, my = pygame.mouse.get_pos()
    if surrender_button.collidepoint((mx, my)):
        if pygame.mouse.get_pressed()[0]:
            sound_theme.stop()
            sound_trompeta.play()
            surrender_screen()

    pygame.display.update()

def game_loop(individual=False):
    sound_theme.play(loops=-1)
    global isRunning
    while isRunning:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
        
        update(individual=individual)
        draw()
        pygame.display.update()

def win_screen():
    click = False
    while True:
        screen.fill((0, 0, 0))
        win_image = pygame.image.load('victory1.png')
        win_image = pygame.transform.scale(win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(win_image, (0, 0))

        mx, my = pygame.mouse.get_pos()

        button_back = pygame.Rect((SCREEN_WIDTH // 2) - 100, 200, 300, 50)

        if button_back.collidepoint((mx, my)):
            if click:
                sound_victory.stop()
                main_menu()

        pygame.draw.rect(screen, (255, 0, 0), button_back)
        draw_text('Back to Menu', font, (255, 255, 255), screen, button_back.centerx, button_back.centery)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

def surrender_screen():
    click = False
    while True:
        screen.fill((0, 0, 0))
        surrender_image = pygame.image.load('surrender.png')
        surrender_image = pygame.transform.scale(surrender_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(surrender_image, (0, 0))

        mx, my = pygame.mouse.get_pos()

        button_back = pygame.Rect((SCREEN_WIDTH // 2) - 100, 200, 300, 50)

        if button_back.collidepoint((mx, my)):
            if click:
                sound_trompeta.stop()
                main_menu()

        pygame.draw.rect(screen, (255, 0, 0), button_back)
        draw_text('Back to Menu', font, (255, 255, 255), screen, button_back.centerx, button_back.centery)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

main_menu()
pygame.quit()
