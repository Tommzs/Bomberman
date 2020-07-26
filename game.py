import pygame
import sys
import random
import time
import cfg
import copy
from player import Player
from explosion import Explosion
from enemy import Enemy
from algorithm import Algorithm
from joystick_state import JoystickState


class Game:
    def __init__(self):

        self.surf = None
        self.show_path = True

        self.clock = None

        self.player_controls = []
        self.players = []
        self.enemy_list = []
        self.ene_blocks = []
        self.bombs = []
        self.explosions = []
        self.bonuses = []
        self.grid = copy.deepcopy(cfg.GRID)
        self.grass_img = None
        self.block_img = None
        self.box_img = None
        self.bomb1_img = None
        self.bomb2_img = None
        self.bomb3_img = None
        self.explosion1_img = None
        self.explosion2_img = None
        self.explosion3_img = None
        self.terrain_images = []
        self.bomb_images = []
        self.explosion_images = []
        self.bonus_images = []
        self.joysticks = []

        pygame.font.init()
        self.font = pygame.font.SysFont(cfg.FONT_TYPE, cfg.FONT_SIZE)
        self.text_lose = self.font.render(cfg.TEXT_LOSE, False, (0, 0, 0))
        self.text_win = self.font.render(cfg.TEXT_WIN, False, (0, 0, 0))

    def game_init(self, path, players_alg, scale, controls):
        self.player_controls = controls

        self.joysticks = [JoystickState() for i in range(pygame.joystick.get_count())]

        self.grid = copy.deepcopy(cfg.GRID)
        cfg.TILE_SIZE = scale
        cfg.TILE_SIZE = scale

        self.font = pygame.font.SysFont('Bebas', scale)
        self.show_path = path
        self.surf = pygame.display.set_mode((13 * cfg.TILE_SIZE, 13 * cfg.TILE_SIZE))
        pygame.display.set_caption('Bomberman')
        self.clock = pygame.time.Clock()
        self.game_speed = cfg.GAME_SPEED
        self.bomb_time = cfg.BOMB_TIME*cfg.GAME_SPEED/self.game_speed

        self.enemy_list = []
        self.ene_blocks = []
        self.bombs.clear()
        self.explosions.clear()
        self.bonuses.clear()

        player_pos = [[1, 1], [11, 11], [1, 11], [11, 1]]

        for i, alg in enumerate(players_alg):
            if alg is Algorithm.PLAYER:
                self.players.append(Player(player_pos[i], self.player_controls[i], f"Player {i+1}"))
                self.players[-1].load_animations(scale, (len(self.players) > 0))
                self.ene_blocks.append(self.players[-1])
            elif alg is not Algorithm.NONE:
                en1 = Enemy(player_pos[i], alg)
                en1.load_animations(i, scale)
                self.enemy_list.append(en1)
                self.ene_blocks.append(en1)

        self.grass_img = pygame.image.load('images/terrain/grass.png')
        self.grass_img = pygame.transform.scale(self.grass_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.block_img = pygame.image.load('images/terrain/block.png')
        self.block_img = pygame.transform.scale(self.block_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.box_img = pygame.image.load('images/terrain/box.png')
        self.box_img = pygame.transform.scale(self.box_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.bonus_fire_img = pygame.image.load('images/bonuses/fire.png')
        self.bonus_fire_img = pygame.transform.scale(self.bonus_fire_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.bonus_bomb_img = pygame.image.load('images/bonuses/bomb.png')
        self.bonus_bomb_img = pygame.transform.scale(self.bonus_bomb_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.bomb1_img = pygame.image.load('images/bomb/1.png')
        self.bomb1_img = pygame.transform.scale(self.bomb1_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.bomb2_img = pygame.image.load('images/bomb/2.png')
        self.bomb2_img = pygame.transform.scale(self.bomb2_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.bomb3_img = pygame.image.load('images/bomb/3.png')
        self.bomb3_img = pygame.transform.scale(self.bomb3_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.explosion1_img = pygame.image.load('images/explosion/1.png')
        self.explosion1_img = pygame.transform.scale(self.explosion1_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.explosion2_img = pygame.image.load('images/explosion/2.png')
        self.explosion2_img = pygame.transform.scale(self.explosion2_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.explosion3_img = pygame.image.load('images/explosion/3.png')
        self.explosion3_img = pygame.transform.scale(self.explosion3_img, (cfg.TILE_SIZE, cfg.TILE_SIZE))
        self.terrain_images = [self.grass_img, self.block_img, self.box_img, self.grass_img]
        self.bomb_images = [self.bomb1_img, self.bomb2_img, self.bomb3_img]
        self.explosion_images = [self.explosion1_img, self.explosion2_img, self.explosion3_img]
        self.bonus_images = [self.bonus_fire_img, self.bonus_bomb_img]

        self.main()


    def draw(self):
        self.surf.fill(cfg.GAME_BACKGROUND)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.surf.blit(self.terrain_images[self.grid[i][j]], (i * cfg.TILE_SIZE, j * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE))

        for x in self.bombs:
            self.surf.blit(self.bomb_images[x.frame], (x.posX * cfg.TILE_SIZE, x.posY * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE))

        for y in self.explosions:
            for x in y.sectors:
                self.surf.blit(self.explosion_images[y.frame], (x[0] * cfg.TILE_SIZE, x[1] * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE))
        
        for bonus in self.bonuses:
            self.surf.blit(self.bonus_images[bonus.type - 1], (bonus.x * cfg.TILE_SIZE, bonus.y * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE))

        for player in self.players:
            if player.life:
                self.surf.blit(player.animation[player.direction][player.frame],
                    (player.posX * (cfg.TILE_SIZE / 4), player.posY * (cfg.TILE_SIZE / 4), cfg.TILE_SIZE, cfg.TILE_SIZE))
        for en in self.enemy_list:
            if en.life:
                self.surf.blit(en.animation[en.direction][en.frame],
                    (en.posX * (cfg.TILE_SIZE / 4), en.posY * (cfg.TILE_SIZE / 4), cfg.TILE_SIZE, cfg.TILE_SIZE))
                if self.show_path:
                    if en.algorithm == Algorithm.DFS:
                        for sek in en.path:
                            pygame.draw.rect(self.surf, (255, 0, 0, 240), [sek[0] * cfg.TILE_SIZE, sek[1] * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE], 1)
                    else:
                        for sek in en.path:
                            pygame.draw.rect(self.surf, (255, 0, 255, 240), [sek[0] * cfg.TILE_SIZE, sek[1] * cfg.TILE_SIZE, cfg.TILE_SIZE, cfg.TILE_SIZE], 1)

        pygame.display.update()


    def generate_map(self):

        for i in range(1, len(self.grid) - 1):
            for j in range(1, len(self.grid[i]) - 1):
                if self.grid[i][j] != 0:
                    continue
                elif (i < 3 or i > len(self.grid) - 4) and (j < 3 or j > len(self.grid[i]) - 4):
                    continue
                if random.randint(0, 9) < 7:
                    self.grid[i][j] = 2


    def game_end_check(self):
        num_alive = 0
        for player in self.players:
            if player.life:
                num_alive += 1

        if num_alive == 0:
            self.game_speed = cfg.GAME_SPEED_AI_ONLY
            self.bomb_time = cfg.BOMB_TIME*cfg.GAME_SPEED/self.game_speed
        
        for enemy in self.enemy_list:
            if enemy.life:
                num_alive += 1
        
        if num_alive > 1:
            return False
        return True


    def updateJoystickStates(self, events):
        for e in events:
            event_type = e.type
            if event_type in [pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP]:
                joy_id = e.joy
                if event_type == pygame.JOYAXISMOTION:
                    self.joysticks[joy_id].axes[e.axis] = e.value
                elif event_type == pygame.JOYBUTTONDOWN:
                    self.joysticks[joy_id].buttons[e.button] = True
                elif event_type == pygame.JOYBUTTONUP:
                    self.joysticks[joy_id].buttons[e.button] = False

    
    def changeDirIfDifferent(self, direction, player):
        if direction != player.direction:
            player.change_direction(direction)


    def main(self):
        self.generate_map()
        end_game = False
        while not self.game_end_check() and not end_game:
            dt = self.clock.tick(self.game_speed)
            for en in self.enemy_list:
                en.make_move(self.grid, self.bombs, self.explosions, self.ene_blocks, self.bomb_time, self.bonuses)

            keys = pygame.key.get_pressed()
            events = pygame.event.get()
            self.updateJoystickStates(events)

            for player in self.players:
                if not player.life:
                    continue
                if not isinstance(player.controls, pygame.joystick.JoystickType):
                    if keys[player.controls.down]: #moving down
                        player.step(0, self.grid, self.ene_blocks)
                    elif keys[player.controls.right]:#moving right
                        player.step(1, self.grid, self.ene_blocks)
                    elif keys[player.controls.up]: #moving up
                        player.step(2, self.grid, self.ene_blocks)
                    elif keys[player.controls.left]: #moving left
                        player.step(3, self.grid, self.ene_blocks)
                    if keys[player.controls.bomb]: #planting bomb
                        player.plant_bomb(self.grid, self.bomb_time, self.bombs, self.bonuses)
                else:
                    joy_id = player.controls.get_id()
                    joystick_state = self.joysticks[joy_id]

                    axis0 = joystick_state.axes[0]
                    axis1 = joystick_state.axes[1]
                    
                    if axis0 < 0:
                        player.step(3, self.grid, self.ene_blocks)
                    elif axis0 > 0:
                        player.step(1, self.grid, self.ene_blocks)
                    elif axis1 < 0:
                        player.step(2, self.grid, self.ene_blocks)
                    elif axis1 > 0:
                        player.step(0, self.grid, self.ene_blocks)
                            
                    if joystick_state.buttons[2]:
                        player.plant_bomb(self.grid, self.bomb_time, self.bombs, self.bonuses)

            self.draw()
            for e in events:
                if e.type == pygame.QUIT:
                    sys.exit(0)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        end_game = self.pause()
                            
            self.update_bombs(dt)
        self.game_over()


    def update_bombs(self, dt):
        for b in self.bombs:
            b.update(dt)
            if b.time < 1:
                b.bomber.bomb_limit += 1
                self.grid[b.posX][b.posY] = 0
                exp_temp = Explosion(b.posX, b.posY, self.bonuses)
                exp_temp.explode(self.grid, self.bombs, b)
                exp_temp.clear_sectors(self.grid, self.bonuses)
                self.explosions.append(exp_temp)
        for player in self.players:
            if player not in self.enemy_list:
                player.check_death(self.explosions)
                player.check_bonus(self.bonuses)
        for en in self.enemy_list:
            en.check_death(self.explosions)
            en.check_bonus(self.bonuses)
        for e in self.explosions:
            e.update(dt)
            if e.time < 1:
                self.explosions.remove(e)


    def game_over(self):

        while True:
            dt = self.clock.tick(15)
            self.update_bombs(dt)
            count = 0
            winner = ""
            for en in self.enemy_list:
                en.make_move(self.grid, self.bombs, self.explosions, self.ene_blocks, self.bomb_time, self.bonuses)
                if en.life:
                    count += 1
                    winner = en.algorithm.name
            for player in self.players:
                if player.life:
                    count += 1
                    winner = player.name
            if count > 1:
                self.draw()
                textsurface = self.font.render("Game ended prematurely", False, (0, 0, 0))
                font_w = textsurface.get_width()
                font_h = textsurface.get_height()
                self.surf.blit(textsurface, (self.surf.get_width() // 2 - font_w//2,  self.surf.get_height() // 2 - font_h//2))
                pygame.display.update()
                time.sleep(2)
                break
            if count == 1:
                self.draw()
                textsurface = self.font.render(winner + " wins", False, (0, 0, 0))
                font_w = textsurface.get_width()
                font_h = textsurface.get_height()
                self.surf.blit(textsurface, (self.surf.get_width() // 2 - font_w//2,  self.surf.get_height() // 2 - font_h//2))
                pygame.display.update()
                time.sleep(2)
                break
            if count == 0:
                self.draw()
                textsurface = self.font.render("Draw", False, (0, 0, 0))
                font_w = textsurface.get_width()
                font_h = textsurface.get_height()
                self.surf.blit(textsurface, (self.surf.get_width() // 2 - font_w//2, self.surf.get_height() // 2 - font_h//2))
                pygame.display.update()
                time.sleep(2)
                break
            self.draw()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)
        self.explosions.clear()
        self.enemy_list.clear()
        self.ene_blocks.clear()
        self.players.clear()
        self.bombs.clear()


    def pause(self):
        stay_pause = True
        end_game = False
        
        textsurface = self.font.render("Pause", False, (0, 0, 0))
        font_w = textsurface.get_width()
        font_h = textsurface.get_height()
        self.surf.blit(textsurface, (self.surf.get_width() // 2 - font_w//2, self.surf.get_height() // 2 - font_h//2))
        pygame.display.update()
        

        while stay_pause:
            self.clock.tick(self.game_speed)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit(0)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        stay_pause = False
                    if e.key == pygame.K_RETURN:
                        end_game = True
                        stay_pause = False
        self.draw()
        return end_game
