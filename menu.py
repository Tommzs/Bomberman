import pygame
import pygame_menu
import cfg
from game import Game
from algorithm import Algorithm
from controls import Controls

class Menu:
    def __init__(self):
        self.clock = None
        self.show_path = False
        self.game = Game()
        self.surface = pygame.display.set_mode(cfg.WINDOW_SIZE)
        self.players_alg = [Algorithm.PLAYER, Algorithm.PLAYER, Algorithm.DIJKSTRA, Algorithm.DFS]

        # Controllers initialization
        self.control_list_select1 = [("Key1", 0)]
        self.control_list_select2 = [("Key2", 1)]
        pygame.joystick.init()
        num_of_gamepads = pygame.joystick.get_count()

        self.controllers = [
            Controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL),
            Controls(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LCTRL)
            ]

        for i in range(num_of_gamepads):
            gamepad = pygame.joystick.Joystick(i)
            gamepad.init()
            self.controllers.append(gamepad)
            if i%2 == 0:
                self.control_list_select1.append((f"Joy{i+1}", i+2))
            else:
                self.control_list_select2.append((f"Joy{i+1}", i+2))

        self.player_controls = [
            self.controllers[0],
            self.controllers[1]
        ]

    def change_controls_player(self, value, control_num, player_num):
        self.player_controls[player_num] = self.controllers[control_num]

    def change_controls_player1(self, value, control_num):
        self.change_controls_player(value, control_num, 0)

    def change_controls_player2(self, value, control_num):
        self.change_controls_player(value, control_num, 1)

    def change_path(self, value, c):
        self.show_path = c

    def change_player(self, value, c, player_num):
        self.players_alg[player_num] = c

    def run_game(self):
        self.game.game_init(self.show_path, self.players_alg, cfg.TILE_SIZE, self.player_controls)


    def main_background(self):
        self.surface.fill(cfg.COLOR_BACKGROUND)


    def menu_loop(self):
        pygame.init()

        pygame.display.set_caption('Bomberman')
        clock = pygame.time.Clock()

        menu_theme = pygame_menu.themes.Theme(
            selection_color=cfg.COLOR_WHITE,
            widget_font=pygame_menu.font.FONT_BEBAS,
            title_font_size=int(cfg.TILE_SIZE*0.8),
            widget_font_color=cfg.COLOR_BLACK,
            widget_font_size=int(cfg.TILE_SIZE*0.7),
            background_color=cfg.MENU_BACKGROUND_COLOR,
            title_background_color=cfg.MENU_TITLE_COLOR,
            widget_shadow=False
        )

        play_menu = pygame_menu.Menu(
            theme=menu_theme,
            height=int(cfg.WINDOW_SIZE[1] * 0.7),
            width=int(cfg.WINDOW_SIZE[0] * 0.7),
            onclose=pygame_menu.events.DISABLE_CLOSE,
            title='Play menu'
        )

        play_options = pygame_menu.Menu(theme=menu_theme,
            height=int(cfg.WINDOW_SIZE[1] * 0.7),
            width=int(cfg.WINDOW_SIZE[0] * 0.7),
            title='Options'
        )
        player_options = pygame_menu.Menu(theme=menu_theme,
            height=int(cfg.WINDOW_SIZE[1] * 0.7),
            width=int(cfg.WINDOW_SIZE[0] * 0.7),
            title='Player options'
        )
        control_options = pygame_menu.Menu(theme=menu_theme,
            height=int(cfg.WINDOW_SIZE[1] * 0.7),
            width=int(cfg.WINDOW_SIZE[0] * 0.7),
            title='Controls'
        )
        play_options.add_button('Characters', player_options)
        play_options.add_button('Controls', control_options)
        play_options.add_button('Back', pygame_menu.events.BACK)

        player_options.add_selector("Character 1", [("Player 1", Algorithm.PLAYER, 0), ("DFS", Algorithm.DFS, 0),
                                                ("DIJKSTRA", Algorithm.DIJKSTRA, 0), ("None", Algorithm.NONE, 0)], onchange=self.change_player)
        player_options.add_selector("Character 2", [("Player 2", Algorithm.PLAYER, 1), ("DFS", Algorithm.DFS, 1),
                                                ("DIJKSTRA", Algorithm.DIJKSTRA, 1), ("None", Algorithm.NONE, 1)], onchange=self.change_player)
        player_options.add_selector("Character 3", [("DFS", Algorithm.DIJKSTRA, 2),
                                                ("DIJKSTRA", Algorithm.DFS, 2), ("None", Algorithm.NONE, 2)], onchange=self.change_player)
        player_options.add_selector("Character 3", [("DFS", Algorithm.DFS, 3),
                                                ("DIJKSTRA", Algorithm.DIJKSTRA, 3), ("None", Algorithm.NONE, 3)], onchange=self.change_player)
        player_options.add_selector("Show AI path", [("No", False), ("Yes", True)], onchange=self.change_path)
        player_options.add_button('Back', pygame_menu.events.BACK)

        control_options.add_selector("Player 1", self.control_list_select1, onchange=self.change_controls_player1)
        control_options.add_selector("Player 2", self.control_list_select2, onchange=self.change_controls_player2)
        control_options.add_button('Back', pygame_menu.events.BACK)

        play_menu.add_button('Start',
                            self.run_game)

        play_menu.add_button('Options', play_options)
        play_menu.add_button('Return  to  main  menu', pygame_menu.events.BACK)

        about_menu_theme = pygame_menu.themes.Theme(
            selection_color=cfg.COLOR_WHITE,
            widget_font=pygame_menu.font.FONT_BEBAS,
            title_font_size=cfg.TILE_SIZE,
            widget_font_color=cfg.COLOR_BLACK,
            widget_font_size=int(cfg.TILE_SIZE*0.4),
            background_color=cfg.MENU_BACKGROUND_COLOR,
            title_background_color=cfg.MENU_TITLE_COLOR,
            widget_shadow=False
        )

        about_menu = pygame_menu.Menu(theme=about_menu_theme,
            height=int(cfg.WINDOW_SIZE[1] * 0.7),
            width=int(cfg.WINDOW_SIZE[0] * 0.7),
            onclose=pygame_menu.events.DISABLE_CLOSE,
            title='About'
        )
        about_menu.add_label("Player_controls: ")
        about_menu.add_label("Movement:_Arrows")
        about_menu.add_label("Plant bomb:_Space")
        about_menu.add_label("Author:_Michal_Sliwa")
        about_menu.add_label("Sprite: ")

        about_menu.add_label("https://opengameart.org/content")
        about_menu.add_label("/bomb-party-the-complete-set")

        main_menu = pygame_menu.Menu(
            theme=menu_theme,
            height=int(cfg.WINDOW_SIZE[1] * 0.6),
            width=int(cfg.WINDOW_SIZE[0] * 0.6),
            onclose=pygame_menu.events.DISABLE_CLOSE,
            title='Main menu'
        )

        main_menu.add_button('Play', play_menu)
        main_menu.add_button('About', about_menu)
        main_menu.add_button('Quit', pygame_menu.events.EXIT)
        while True:

            clock.tick(cfg.MENU_FPS)

            self.main_background()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()

            main_menu.mainloop(self.surface, self.main_background, disable_loop=False, fps_limit=0)
            main_menu.update(events)
            main_menu.draw(self.surface)

            pygame.display.flip()

    def run(self):
        self.menu_loop()
