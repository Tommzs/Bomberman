import pygame
import sys
import random
import time
from player import Player
from explosion import Explosion
from enemy import Enemy
from algorithm import Algorithm
from controls import Controls

TILE_WIDTH = 40
TILE_HEIGHT = 40

WINDOW_WIDTH = 13 * TILE_WIDTH
WINDOW_HEIGHT = 13 * TILE_HEIGHT

BACKGROUND = (107, 142, 35)

surf = None
show_path = True

clock = None

players = []
enemy_list = []
ene_blocks = []
bombs = []
explosions = []

player_controls = [
    Controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL),
    Controls(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LCTRL)
]


grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

grass_img = None
block_img = None
box_img = None
bomb1_img = None
bomb2_img = None
bomb3_img = None
explosion1_img = None
explosion2_img = None
explosion3_img = None


terrain_images = []
bomb_images = []
explosion_images = []

pygame.font.init()
font = pygame.font.SysFont('Bebas', 30)
TEXT_LOSE = font.render('GAME OVER', False, (0, 0, 0))
TEXT_WIN = font.render('WIN', False, (0, 0, 0))


def game_init(path, players_alg, scale):

    global TILE_WIDTH
    global TILE_HEIGHT
    TILE_WIDTH = scale
    TILE_HEIGHT = scale

    global font
    font = pygame.font.SysFont('Bebas', scale)

    global show_path
    show_path = path

    global surf
    surf = pygame.display.set_mode((13 * TILE_WIDTH, 13 * TILE_HEIGHT))
    pygame.display.set_caption('Bomberman')

    global clock
    clock = pygame.time.Clock()

    global game_speed
    game_speed = 15

    global bomb_time
    bomb_time = 3000*15/game_speed

    global enemy_list
    global ene_blocks
    global players

    enemy_list = []
    ene_blocks = []
    global explosions
    global bombs
    bombs.clear()
    explosions.clear()

    player_pos = [[1, 1], [11, 11], [1, 11], [11, 1]]

    for i, alg in enumerate(players_alg):
        if alg is Algorithm.PLAYER:
            players.append(Player(player_pos[i], player_controls[i], f"Player {i}"))
            players[-1].load_animations(scale)
            ene_blocks.append(players[-1])
        elif alg is not Algorithm.NONE:
            en1 = Enemy(player_pos[i], alg)
            en1.load_animations('1', scale)
            enemy_list.append(en1)
            ene_blocks.append(en1)

    global grass_img
    grass_img = pygame.image.load('images/terrain/grass.png')
    grass_img = pygame.transform.scale(grass_img, (TILE_WIDTH, TILE_HEIGHT))
    global block_img
    block_img = pygame.image.load('images/terrain/block.png')
    block_img = pygame.transform.scale(block_img, (TILE_WIDTH, TILE_HEIGHT))
    global box_img
    box_img = pygame.image.load('images/terrain/box.png')
    box_img = pygame.transform.scale(box_img, (TILE_WIDTH, TILE_HEIGHT))
    global bomb1_img
    bomb1_img = pygame.image.load('images/bomb/1.png')
    bomb1_img = pygame.transform.scale(bomb1_img, (TILE_WIDTH, TILE_HEIGHT))
    global bomb2_img
    bomb2_img = pygame.image.load('images/bomb/2.png')
    bomb2_img = pygame.transform.scale(bomb2_img, (TILE_WIDTH, TILE_HEIGHT))
    global bomb3_img
    bomb3_img = pygame.image.load('images/bomb/3.png')
    bomb3_img = pygame.transform.scale(bomb3_img, (TILE_WIDTH, TILE_HEIGHT))
    global explosion1_img
    explosion1_img = pygame.image.load('images/explosion/1.png')
    explosion1_img = pygame.transform.scale(explosion1_img, (TILE_WIDTH, TILE_HEIGHT))
    global explosion2_img
    explosion2_img = pygame.image.load('images/explosion/2.png')
    explosion2_img = pygame.transform.scale(explosion2_img, (TILE_WIDTH, TILE_HEIGHT))
    global explosion3_img
    explosion3_img = pygame.image.load('images/explosion/3.png')
    explosion3_img = pygame.transform.scale(explosion3_img, (TILE_WIDTH, TILE_HEIGHT))
    global terrain_images
    terrain_images = [grass_img, block_img, box_img, grass_img]
    global bomb_images
    bomb_images = [bomb1_img, bomb2_img, bomb3_img]
    global explosion_images
    explosion_images = [explosion1_img, explosion2_img, explosion3_img]

    main()


def draw():
    surf.fill(BACKGROUND)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            surf.blit(terrain_images[grid[i][j]], (i * TILE_WIDTH, j * TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH))

    for x in bombs:
        surf.blit(bomb_images[x.frame], (x.posX * TILE_WIDTH, x.posY * TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH))

    for y in explosions:
        for x in y.sectors:
            surf.blit(explosion_images[y.frame], (x[0] * TILE_WIDTH, x[1] * TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH))
    for player in players:
        if player.life:
            surf.blit(player.animation[player.direction][player.frame],
                (player.posX * (TILE_WIDTH / 4), player.posY * (TILE_HEIGHT / 4), TILE_WIDTH, TILE_HEIGHT))
    for en in enemy_list:
        if en.life:
            surf.blit(en.animation[en.direction][en.frame],
                   (en.posX * (TILE_WIDTH / 4), en.posY * (TILE_HEIGHT / 4), TILE_WIDTH, TILE_HEIGHT))
            if show_path:
                if en.algorithm == Algorithm.DFS:
                    for sek in en.path:
                        pygame.draw.rect(surf, (255, 0, 0, 240), [sek[0] * TILE_WIDTH, sek[1] * TILE_HEIGHT, TILE_WIDTH, TILE_WIDTH], 1)
                else:
                    for sek in en.path:
                        pygame.draw.rect(surf, (255, 0, 255, 240), [sek[0] * TILE_WIDTH, sek[1] * TILE_HEIGHT, TILE_WIDTH, TILE_WIDTH], 1)

    pygame.display.update()


def generate_map():

    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] != 0:
                continue
            elif (i < 3 or i > len(grid) - 4) and (j < 3 or j > len(grid[i]) - 4):
                continue
            if random.randint(0, 9) < 7:
                grid[i][j] = 2

    return


def game_end_check():
    num_alive = 0
    for player in players:
        if player.life:
            num_alive += 1

    if num_alive == 0:
        global game_speed
        global bomb_time
        game_speed = 60
        bomb_time = 3000*15/game_speed
    
    for enemy in enemy_list:
        if enemy.life:
            num_alive += 1
    
    if num_alive > 1:
        return False
    return True


def main():
    generate_map()
    end_game = False
    while not game_end_check() and not end_game:
        dt = clock.tick(game_speed)
        for en in enemy_list:
            en.make_move(grid, bombs, explosions, ene_blocks, bomb_time)

        keys = pygame.key.get_pressed()
        new_directions = [player.direction for player in players]
        movements = [False for player in players]

        for new_direction, movement, player in zip(new_directions, movements, players):
            if not player.life:
                continue
            if keys[player.controls.down]:
                new_direction = 0
                player.move(0, 1, grid, ene_blocks)
                movement = True
            elif keys[player.controls.right]:
                new_direction = 1
                player.move(1, 0, grid, ene_blocks)
                movement = True
            elif keys[player.controls.up]:
                new_direction = 2
                player.move(0, -1, grid, ene_blocks)
                movement = True
            elif keys[player.controls.left]:
                new_direction = 3
                player.move(-1, 0, grid, ene_blocks)
                movement = True
            if new_direction != player.direction:
                player.frame = 0
                player.direction = new_direction
            if movement:
                if player.frame == 2:
                    player.frame = 0
                else:
                    player.frame += 1

        draw()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    end_game = pause()
                for player in players:
                    if not player.life:
                        continue
                    if e.key == player.controls.bomb:
                        if player.bomb_limit == 0:
                            continue
                        temp_bomb = player.plant_bomb(grid, bomb_time)
                        bombs.append(temp_bomb)
                        grid[temp_bomb.posX][temp_bomb.posY] = 3
                        player.bomb_limit -= 1

        update_bombs(dt)
    game_over()


def update_bombs(dt):
    for b in bombs:
        b.update(dt)
        if b.time < 1:
            b.bomber.bomb_limit += 1
            grid[b.posX][b.posY] = 0
            exp_temp = Explosion(b.posX, b.posY, b.range)
            exp_temp.explode(grid, bombs, b)
            exp_temp.clear_sectors(grid)
            explosions.append(exp_temp)
    for player in players:
        if player not in enemy_list:
            player.check_death(explosions)
    for en in enemy_list:
        en.check_death(explosions)
    for e in explosions:
        e.update(dt)
        if e.time < 1:
            explosions.remove(e)


def game_over():

    while True:
        dt = clock.tick(15)
        update_bombs(dt)
        count = 0
        winner = ""
        for en in enemy_list:
            en.make_move(grid, bombs, explosions, ene_blocks, bomb_time)
            if en.life:
                count += 1
                winner = en.algorithm.name
        for player in players:
            if player.life:
                count += 1
                winner = player.name
        if count > 1:
            draw()
            textsurface = font.render("Game ended prematurely", False, (0, 0, 0))
            font_w = textsurface.get_width()
            font_h = textsurface.get_height()
            surf.blit(textsurface, (surf.get_width() // 2 - font_w//2,  surf.get_height() // 2 - font_h//2))
            pygame.display.update()
            time.sleep(2)
            break
        if count == 1:
            draw()
            textsurface = font.render(winner + " wins", False, (0, 0, 0))
            font_w = textsurface.get_width()
            font_h = textsurface.get_height()
            surf.blit(textsurface, (surf.get_width() // 2 - font_w//2,  surf.get_height() // 2 - font_h//2))
            pygame.display.update()
            time.sleep(2)
            break
        if count == 0:
            draw()
            textsurface = font.render("Draw", False, (0, 0, 0))
            font_w = textsurface.get_width()
            font_h = textsurface.get_height()
            surf.blit(textsurface, (surf.get_width() // 2 - font_w//2, surf.get_height() // 2 - font_h//2))
            pygame.display.update()
            time.sleep(2)
            break
        draw()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
    explosions.clear()
    enemy_list.clear()
    ene_blocks.clear()
    players.clear()
    bombs.clear()


def pause():
    stay_pause = True
    end_game = False
    
    textsurface = font.render("Pause", False, (0, 0, 0))
    font_w = textsurface.get_width()
    font_h = textsurface.get_height()
    surf.blit(textsurface, (surf.get_width() // 2 - font_w//2, surf.get_height() // 2 - font_h//2))
    pygame.display.update()
    

    while stay_pause:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    stay_pause = False
                if e.key == pygame.K_RETURN:
                    end_game = True
                    stay_pause = False
    draw()
    return end_game
