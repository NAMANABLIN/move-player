import os
import sys

import pygame as pg

BLACK = pg.Color('BLACK')
WHITE = pg.Color('WHITE')


def load_level(filename):
    filename = os.path.join('levels', filename)
    if not os.path.isfile(filename):
        print(f"Файл с уровнем '{filename}' не найден.\nВсе уровни должны быть в папке 'levels'.")
        sys.exit()
    else:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}'")
        sys.exit()
    image = pg.image.load(fullname)
    return image


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = mar
        self.x, self.y = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self):
        if keys[pg.K_RIGHT]:
            for x in box_group:
                if x.rect.colliderect(self.rect.move(speed, 0)):
                    return
            self.rect.x += speed

        if keys[pg.K_LEFT]:
            for x in box_group:
                if x.rect.colliderect(self.rect.move(-speed, 0)):
                    return
            self.rect.x -= speed

        if keys[pg.K_DOWN]:
            for x in box_group:
                if x.rect.colliderect(self.rect.move(0, speed)):
                    return
            self.rect.y += speed

        if keys[pg.K_UP]:
            for x in box_group:
                if x.rect.colliderect(self.rect.move(0, -speed)):
                    return
            self.rect.y -= speed


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            self.add(box_group)
        self.image = tile_images[tile_type]
        self.x, self.y = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - W // 2 + tile_width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - H // 2 + tile_height // 2)


def terminate():
    pg.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pg.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pg.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            elif event.type == pg.KEYDOWN or \
                    event.type == pg.MOUSEBUTTONDOWN:
                return
        pg.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    mar = load_image('mar.png', -1)
    fon = load_image('fon.jpg')

    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')}

    tile_width = tile_height = 50

    all_sprites = pg.sprite.Group()
    player_group = pg.sprite.Group()
    tiles_group = pg.sprite.Group()
    box_group = pg.sprite.Group()

    a = input()
    player, level_x, level_y = generate_level(load_level(a))

    pg.init()

    size = W, H = 500, 500

    camera = Camera()

    pg.display.set_caption('Перемещение героя. Камера')
    screen = pg.display.set_mode(size)

    clock = pg.time.Clock()

    speed = 50
    running = True

    start_screen()
    while True:
        screen.fill(BLACK)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                player.move()
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        player_group.draw(screen)

        pg.display.flip()
        clock.tick(50)
