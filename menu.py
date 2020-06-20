import pygame
import pygame_menu
import game
from algorithm import Algorithm
from controls import Controls

COLOR_BACKGROUND = (153, 153, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (102, 102, 153)
MENU_TITLE_COLOR = (51, 51, 255)

pygame.display.init()
INFO = pygame.display.Info()
TILE_SIZE = int(INFO.current_h * 0.035)
WINDOW_SIZE = (13 * TILE_SIZE, 13 * TILE_SIZE)

clock = None
players_alg = [Algorithm.PLAYER, Algorithm.PLAYER, Algorithm.DIJKSTRA, Algorithm.DFS]
show_path = False
surface = pygame.display.set_mode(WINDOW_SIZE)

control_list_select1 = [("Key1", 0)]
control_list_select2 = [("Key2", 1)]
pygame.joystick.init()
num_of_gamepads = pygame.joystick.get_count()

controllers = [
    Controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RCTRL),
    Controls(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_LCTRL)
    ]

for i in range(num_of_gamepads):
    gamepad = pygame.joystick.Joystick(i)
    gamepad.init()
    controllers.append(gamepad)
    if i%2 == 0:
        control_list_select1.append((f"Joy{i+1}", i+2))
    else:
        control_list_select2.append((f"Joy{i+1}", i+2))

player_controls = [
    controllers[0],
    controllers[1]
]

def change_controls_player(value, control_num, player_num):
    player_controls[player_num] = controllers[control_num]

def change_controls_player1(value, control_num):
    change_controls_player(value, control_num, 0)

def change_controls_player2(value, control_num):
    change_controls_player(value, control_num, 1)

def change_path(value, c):
    global show_path
    show_path = c


def change_player(value, c, player_num):
    global players_alg
    players_alg[player_num] = c

def run_game():
    game.game_init(show_path, players_alg, TILE_SIZE, player_controls)


def main_background():
    global surface
    surface.fill(COLOR_BACKGROUND)


def menu_loop():
    pygame.init()

    pygame.display.set_caption('Bomberman')
    clock = pygame.time.Clock()

    menu_theme = pygame_menu.themes.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame_menu.font.FONT_BEBAS,
        title_font_size=int(TILE_SIZE*0.8),
        widget_font_color=COLOR_BLACK,
        widget_font_size=int(TILE_SIZE*0.7),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,
        widget_shadow=False
    )

    play_menu = pygame_menu.Menu(
        theme=menu_theme,
        height=int(WINDOW_SIZE[1] * 0.7),
        width=int(WINDOW_SIZE[0] * 0.7),
        onclose=pygame_menu.events.DISABLE_CLOSE,
        title='Play menu'
    )

    play_options = pygame_menu.Menu(theme=menu_theme,
        height=int(WINDOW_SIZE[1] * 0.7),
        width=int(WINDOW_SIZE[0] * 0.7),
        title='Options'
    )
    player_options = pygame_menu.Menu(theme=menu_theme,
        height=int(WINDOW_SIZE[1] * 0.7),
        width=int(WINDOW_SIZE[0] * 0.7),
        title='Options'
    )
    control_options = pygame_menu.Menu(theme=menu_theme,
        height=int(WINDOW_SIZE[1] * 0.7),
        width=int(WINDOW_SIZE[0] * 0.7),
        title='Options'
    )
    play_options.add_button('Characters', player_options)
    play_options.add_button('Controls', control_options)
    play_options.add_button('Back', pygame_menu.events.BACK)

    player_options.add_selector("Character 1", [("Player 1", Algorithm.PLAYER, 0), ("DFS", Algorithm.DFS, 0),
                                              ("DIJKSTRA", Algorithm.DIJKSTRA, 0), ("None", Algorithm.NONE, 0)], onchange=change_player)
    player_options.add_selector("Character 2", [("Player 2", Algorithm.PLAYER, 1), ("DFS", Algorithm.DFS, 1),
                                              ("DIJKSTRA", Algorithm.DIJKSTRA, 1), ("None", Algorithm.NONE, 1)], onchange=change_player)
    player_options.add_selector("Character 3", [("DFS", Algorithm.DIJKSTRA, 2),
                                              ("DIJKSTRA", Algorithm.DFS, 2), ("None", Algorithm.NONE, 2)], onchange=change_player)
    player_options.add_selector("Character 3", [("DFS", Algorithm.DFS, 3),
                                              ("DIJKSTRA", Algorithm.DIJKSTRA, 3), ("None", Algorithm.NONE, 3)], onchange=change_player)
    player_options.add_selector("Show path", [("Yes", True), ("No", False)], onchange=change_path)
    player_options.add_button('Back', pygame_menu.events.BACK)

    control_options.add_selector("Player 1", control_list_select1, onchange=change_controls_player1)
    control_options.add_selector("Player 2", control_list_select2, onchange=change_controls_player2)
    control_options.add_button('Back', pygame_menu.events.BACK)

    play_menu.add_button('Start',
                         run_game)

    play_menu.add_button('Options', play_options)
    play_menu.add_button('Return  to  main  menu', pygame_menu.events.BACK)

    about_menu_theme = pygame_menu.themes.Theme(
        selection_color=COLOR_WHITE,
        widget_font=pygame_menu.font.FONT_BEBAS,
        title_font_size=TILE_SIZE,
        widget_font_color=COLOR_BLACK,
        widget_font_size=int(TILE_SIZE*0.4),
        background_color=MENU_BACKGROUND_COLOR,
        title_background_color=MENU_TITLE_COLOR,
        widget_shadow=False
    )

    about_menu = pygame_menu.Menu(theme=about_menu_theme,
        height=int(WINDOW_SIZE[1] * 0.7),
        width=int(WINDOW_SIZE[0] * 0.7),
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
        height=int(WINDOW_SIZE[1] * 0.6),
        width=int(WINDOW_SIZE[0] * 0.6),
        onclose=pygame_menu.events.DISABLE_CLOSE,
        title='Main menu'
    )

    main_menu.add_button('Play', play_menu)
    main_menu.add_button('About', about_menu)
    main_menu.add_button('Quit', pygame_menu.events.EXIT)
    while True:

        clock.tick(FPS)

        main_background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

        main_menu.mainloop(surface, main_background, disable_loop=False, fps_limit=0)
        main_menu.update(events)
        main_menu.draw(surface)

        pygame.display.flip()


menu_loop()
