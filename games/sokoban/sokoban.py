import pygame
import os
import profile
import sys
sys.path.insert(0 , 'J:\menu')

def save(score_display):
    username = os.getlogin() #get username
    user_profile = profile.User_Profile(username)
    user_profile.update_score(score_display)
    user_profile.add_game_record('Sokoban')

def get_score(time,level):
    level = level - 1
    score = (level * 10000)/time
    save(score)
    
tile_characters = {
    "─": "images/wall-width.png",
    "│": "images/wall-height.png",
    "┬": "images/wall-all.png",
    "╵": "images/wall-top.png",
    "┌": "images/wall-righttopbot.png",
    "┐": "images/wall-lefttopbot.png",
    "└": "images/wall-righttop.png",
    "┘": "images/wall-lefttop.png",

    ".": "images/empty.png",
    "■": "images/block.png",
    "□": "images/snake.png",
    "▣": "images/activeBlock.png"

}


class Map():
    """Creates and renders map."""

    def __init__(self, file_name):
        """Load map and images."""

        self.load_map(file_name)
        self.load_tiles()

    def load_map(self, file_name):
        """Makes the map into a list"""

        # List for lines of map
        self.map = []

        # Opens map files
        with open(file_name, "r", encoding='utf8') as f_obj:
            for each_line in f_obj:
                # Adds lines from file to map list
                self.map.append(list(each_line.strip("\n")))

    def load_tiles(self):
        """Load tiles."""

        # Dictionary for tiles of map
        self.tiles = {}

        # Go through the dictionary 'tile_characters' and name 'tile_symbol'
        # every element of the dictionary which offers the possibility to do
        # something with each iteration of the loop 'for'
        for tile_symbol in tile_characters:
            # Retrieves the path to the image stored in the dictionary
            # 'tile_characters' and stores it in the 'tile_path' variable
            tile_path = tile_characters[tile_symbol]
            # Adds tiles to a key character and loaded image
            self.tiles[tile_symbol] = pygame.image.load(
                tile_path).convert_alpha()

    def render(self):
        """Renders map onto screen."""

        # Sees all x and y coordinates in the map
        for x in range(width):
            for y in range(height):
                # Gets the character associated with the x, y
                # coordinate
                character = self.map[y][x]
                # Gets image associated with the character (from self.tiles)
                tile_image = self.tiles[character]
                # Displays image
                gameDisplay.blit(tile_image, (x * tile_size, y * tile_size))

    def walkable(self, x, y):
        """Sees if tile is walkable."""

        # Look at line (y) then character (x) to see if tile is walkable.
        if self.map[y][x] == "." or self.map[y][x] == "□":
            return True

    def pushable(self, x, y, dx, dy):
        """Sees if tile is pushable."""

        # Find value of the tile we need to push from map
        next_tile = self.map[y + dy][x + dx]
        # Finds value of the tile behind the one we want to push
        after_next_tile = self.map[y + dy*2][x + dx*2]

        # Moving tile
        if next_tile == "■":
            if after_next_tile == ".":
                self.map[y + dy][x + dx] = "."
                self.map[y + dy*2][x + dx*2] = "■"
                return True
            elif after_next_tile == "□":
                self.map[y + dy][x + dx] = "."
                self.map[y + dy*2][x + dx*2] = "▣"
                return True
        elif next_tile == "▣":
            if after_next_tile == ".":
                self.map[y + dy][x + dx] = "□"
                self.map[y + dy*2][x + dx*2] = "■"
                return True
            elif after_next_tile == "□":
                self.map[y + dy][x + dx] = "□"
                self.map[y + dy*2][x + dx*2] = "▣"
                return True

    def victory_condition(self, player, all_maps):
        """Checks if the victory condition is met."""

        global current_map
        global map_spawns

        # Look at map
        for y in self.map:
            for x in y:
                # If a base isn't covered, continue game
                if x == "□":
                    return False

        # Else they won
        if current_map < 8:
            current_map += 1
            player.replace_player(map_spawns[current_map])

        self.load_map('maps/' + all_maps[current_map])

        if current_map == 8:
            button('Restart', (gameDisplay_rect.centerx/2),
                   (gameDisplay_rect.centery/0.75636363636),
                   100, 50, green, bright_green, game_intro)
            button('Quit', (gameDisplay_rect.centerx*1.25),
                   (gameDisplay_rect.centery/0.75636363636),
                   100, 50, red, bright_red, quitgame)


# Sprites
sprites_dict = {
    "up": "images/player_up.png",
    "down": "images/player_down.png",
    "left": "images/player_left.png",
    "right": "images/player_right.png"
}


class Person():
    """Creates and renders the player."""

    def __init__(self, initial_position):
        """Load all images and put character in initial position."""

        self.load_sprites()
        self.replace_player(initial_position)

    def load_sprites(self):
        """Load sprites in a dict."""

        self.sprites = {}

        for sprite in sprites_dict:
            # Stores the path to the image in the 'sprite_path' variable
            sprite_path = sprites_dict[sprite]
            # Adds key direction and image to sprite
            self.sprites[sprite] = pygame.image.load(sprite_path)

    def look(self, direction):
        """Manages direction of character."""

        self.current_direction = direction

    def move(self, dx, dy):
        """Determines movement of character."""

        # Sees if next tile is walkable / pushable.
        next_tile_is_walkable = game_map.walkable(self.x + dx, self.y + dy)
        next_tile_is_pushable = game_map.pushable(self.x, self.y, dx, dy)

        # If above are true, move player.
        if next_tile_is_walkable or next_tile_is_pushable:
            self.x += dx
            self.y += dy

    def replace_player(self, initial_position):
        """Set initial position of player."""

        self.current_direction = "down"
        (self.x, self.y) = initial_position

    def render(self):
        """Renders player to gameDisplay."""

        # Get sprite depending on direction
        current_sprite = self.sprites[self.current_direction]

        # Displays sprite
        gameDisplay.blit(current_sprite, (self.x * tile_size,
                                          (self.y - 0.5) * tile_size))


def check_keyboard_events():
    """Checks keyboard events."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            get_score(timer,current_map)
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            respond_keyboard_events(event.key)


def respond_keyboard_events(key):
    """Responds to keyboard events."""
    global current_map

    if key == pygame.K_r:
        game_map.load_map('maps/' + all_maps[current_map])
        player.replace_player(map_spawns[current_map])
    if key == pygame.K_p:
        pause()

    if key == pygame.K_LEFT:
        player.look("left")
        player.move(-1, 0)
    if key == pygame.K_RIGHT:
        player.look("right")
        player.move(1, 0)
    if key == pygame.K_UP:
        player.look("up")
        player.move(0, -1)
    if key == pygame.K_DOWN:
        player.look("down")
        player.move(0, 1)


def message_display(text, screen_rect, size, area):
    largeText = pygame.font.Font('freesansbold.ttf', size)
    textSurface = largeText.render(text, True, white)
    TextRect = textSurface.get_rect()

    TextRect.centerx = screen_rect.centerx

    if area == 'top_center':
        TextRect.top = 10
    if area == 'midtop_center':
        TextRect.top = 200
    if area == 'center':
        TextRect.centery = screen_rect.centery

    return textSurface, TextRect


pygame.init()

clock = pygame.time.Clock()

# px of tiles
tile_size = 64

# map in tiles
width = 22
height = 13

gameDisplay = pygame.display.set_mode((width * tile_size, height * tile_size))
gameDisplay_rect = gameDisplay.get_rect()
pygame.display.set_caption("Sokoban")

title_screen = pygame.image.load(
    'images/sokoban_title_screen.jpg').convert()
controls_screen = pygame.image.load(
    'images/controls_screen_2_final.jpg').convert()
game_icon = pygame.image.load('images/game_icon.png')

pygame.display.set_icon(game_icon)

white = (255, 255, 255)
black = (0, 0, 0)
dark_grey = (10, 10, 10)

grey = (140, 140, 140)
light_grey = (173, 173, 173)
red = (180, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 255, 0)

small_text = pygame.font.Font("freesansbold.ttf", 20)

current_map = 0
all_maps = ['start.txt', 'first_map.txt', 'second_map.txt', 'third_map.txt',
            'fourth_map.txt', 'fifth_map.txt', 'sixth_map.txt',
            'straightOuttaSokoban.txt', 'win.txt']
map_spawns = [(11, 7), (10, 7), (9, 4), (8, 4), (9, 4), (8, 6), (12, 4),
              (9, 4), (11, 7)]
game_map = Map('maps/' + all_maps[current_map])
player = Person(map_spawns[current_map])

timer = 0


def quitgame():
    pygame.quit()
    quit()


def text_objects(text, font):
    """Creates text objects."""
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def button(msg, x, y, w, h, inactive_colour, active_colour, action=None,
           delay=None):
    """Creates and displays button to be used on main menu."""

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, active_colour, (x, y, w, h))
        if click[0] == 1 and action is not None:
            if delay:
                pygame.time.delay(90)
                action()
            else:
                action()
    else:
        pygame.draw.rect(gameDisplay, inactive_colour, (x, y, w, h))

    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(text_surf, text_rect)


def pause():
    """Creates and displays pause menu."""
    global paused
    paused = True

    pause_msg, pause_rect = message_display(
        "Paused", gameDisplay_rect, 30, 'center')
    gameDisplay.blit(pause_msg, pause_rect)

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        button('Continue', (gameDisplay_rect.centerx/2),
               (gameDisplay_rect.centery/1.06666666667),
               100, 50, green, bright_green,
               unpause)
        button('Quit', (gameDisplay_rect.centerx*1.34),
               (gameDisplay_rect.centery/1.06666666667),
               100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def unpause():
    global paused
    paused = False


def controls():
    """Displays controls menu screen."""
    gameDisplay.fill(dark_grey)

    gameDisplay.blit(controls_screen, (60, 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        button('Back', (gameDisplay_rect.centerx/1.085),
               (gameDisplay_rect.bottom/1.4), 100,
               50, grey, light_grey, game_intro)

        pygame.display.update()
        clock.tick(15)


def game_intro():
    """Creates and displays main menu for game."""

    gameDisplay.fill(dark_grey)
    gameDisplay.blit(title_screen, (60, 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        button('GO!', (gameDisplay_rect.centerx/2),
               (gameDisplay_rect.centery/0.832),
               100, 50, green, bright_green, game_loop)
        button('Controls', (gameDisplay_rect.centerx/1.085),
               (gameDisplay_rect.centery/0.832),
               100, 50, grey, light_grey, controls)
        button('Quit', (gameDisplay_rect.centerx*1.34),
               (gameDisplay_rect.centery/0.832),
               100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


def game_loop():
    global timer
    global current_map

    current_map = 0
    timer = 0

    while True:

        gameDisplay.fill((10, 10, 10))

        game_map.victory_condition(player, all_maps)
        check_keyboard_events()
        game_map.render()
        player.render()

        # timer
        if current_map > 0 and current_map < 8:
            seconds = clock.get_time() / 1000
            timer += seconds

            msg, msg_rect = message_display('Timer ' + str(round(timer)),
                                            gameDisplay_rect, 20, 'top_center')
            gameDisplay.blit(msg, msg_rect)

        # end score
        if current_map == 8:
            msg, msg_rect = message_display('You took ' + str(round(timer)) +
                                            ' seconds', gameDisplay_rect, 30,
                                            'midtop_center')
            gameDisplay.blit(msg, msg_rect)

        pygame.display.update()
        clock.tick(30)


game_intro()
