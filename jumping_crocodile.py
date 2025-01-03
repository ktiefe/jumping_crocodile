import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join

current_file_directory = os.path.dirname(os.path.abspath(__file__))

pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

text_font = pygame.font.SysFont("Arial", 30)

def draw_text(window, x, y, text,):
    color = [0,0,0]
    img = text_font.render(text, True, color)
    window.blit(img, (x, y))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def game_restart():
    main(window)


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def load_sprites(path: str, w, h):

    abs_path = f"{current_file_directory}/{path}"
    assert os.path.isfile(abs_path), "File doesn't exists,"

    sprite_sheet = pygame.image.load(abs_path).convert_alpha()
    sprites = []
    for i in range(sprite_sheet.get_width() // w):
        surface = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        rect = pygame.Rect(i * w, 0, w, h)
        surface.blit(sprite_sheet, (0, 0), rect)
        sprites.append(pygame.transform.scale2x(surface))

    return sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)


    COLOR = (255, 0, 0)
class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.life_level = 5

    def restart(self):
        pass

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def add_life(self):
        self.life_level +=1

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0
            self.life_level = self.life_level - 1

        if self.life_level == 0:
            game_restart()

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
        draw_text(win, 120, 120, f"Life: {self.life_level}")


class Text():
    def __init__(self, x, y, pre_text: str, size: int):
        self.pre_text: str = pre_text
        self.size: int = size
        self.x = x
        self.y = y
        self.text_font = pygame.font.SysFont("Arial", size)

    def set_text(self, text: str) -> None:
        self.text = text

    def draw(self, win) -> None:
        color = [0, 0, 0]
        img = self.text_font.render(self.pre_text + self.text, True, color)
        win.blit(img, (self.x, self.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


class Fruit(Object):
    ANIMATION_DELAY = 3
    def __init__(self, x, y):
        self.width = 32
        self.height = 32
        self.x = x
        self.y = y
        super().__init__(x, y, width=self.width, height=self.height, name="fruit")
        self._set_image("assets/Items/Fruits/Melon.png", self.width, self.height)

    def _set_image(self, path_name: str, width, height):
        self.fruits = load_sprites(path_name, width, height)

        self.image = self.fruits[0]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]

        self.animation_count = 0
        self.num_sprites = len(self.fruits)
        pass

    def eat(self):
        self._set_image("assets/Items/Fruits/Collected.png", self.width, self.height)

    def loop(self):
        if self.animation_count >= self.num_sprites:
            self.animation_count = 0

        self.image = self.fruits[math.floor(self.animation_count)]
        self.animation_count += (1/self.ANIMATION_DELAY)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        # init image, name off, start form the 0 frame
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image) 

        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, texts, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    for text in texts:
        text.draw(window)

    player.draw(window, offset_x)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

        if obj and obj.name == "fruit":
            obj.eat()
            player.add_life()


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Green.png")

    block_size = 96

    player = Player(100, 100, 50, 50)
    fires = [Fire(block_size * 2 + 32, HEIGHT - block_size * 4 -64, 16, 32),
             Fire(block_size*-2 + 32, HEIGHT - block_size * 4 -64, 16, 32),
             Fire(block_size * 5 + 32, HEIGHT - block_size * 5 -64, 16, 32)]
    
    fruits = [Fruit(x=719, y=190), Fruit(x=240, y=303), Fruit(x=528, y=195)]

    for fire in fires:  
        fire.on()

    debug_text = [Text(813, 8, f"Mouse coordinates: ", size=12)]

    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 2, HEIGHT - block_size * 4, block_size),
               Block(block_size * 5, HEIGHT - block_size * 5, block_size),
               Block(block_size * 7, HEIGHT - block_size * 6, block_size),

               Block(block_size*-2, HEIGHT - block_size * 4, block_size),
               Block(block_size*-4, HEIGHT - block_size * 5, block_size),
               Block(block_size*-6, HEIGHT - block_size * 6, block_size),
               ] + fires + fruits

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():   

            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

                if event.key == pygame.K_r:
                    player.restart()
                    print(f"Game restart!!!!")
                    game_restart()

                if event.key == pygame.K_q:
                    run = False
                    
                break 


        player.loop(FPS)

        for fire in fires:
            fire.loop()


        for fruit in fruits:
            fruit.loop()
        
        handle_move(player, objects)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        debug_text[0].set_text(f"{mouse_x, mouse_y}")
        
        draw(window, background, bg_image, player, objects, debug_text, offset_x)
      
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
