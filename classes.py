# import time
import pygame
import pygame_gui
import pytmx
import sys
import os
import random
import schedule
# print(2)
# print(1)

count_turn = 0
game_score = 0
COUNT_SHIP = 1
tile_w, tile_h = 40, 40
board_w, board_h = 25, 20
size = w, h = tile_w * board_w, tile_h * board_h
lvl_difficult = "easy"
MAPS_DIR = "map"
PIC_DIR = "pictures"
cell_size = 40
# print(-1)
pygame.init()
game_screen = pygame.display.set_mode((1000, 800))
# pygame.display.set_caption('A little farm')
# print(-2)

sheep_sound = pygame.mixer.Sound("sounds/sheepSound.wav")
wolf_sound = pygame.mixer.Sound("sounds/wolfSound.wav")
dog_sound = pygame.mixer.Sound("sounds/dogSound.wav")

animals = pygame.sprite.Group()
ships = pygame.sprite.Group()
wolfs = pygame.sprite.Group()
dogs = pygame.sprite.Group()
cowboys = pygame.sprite.Group()
good_gays = pygame.sprite.Group()
game_over = pygame.sprite.Group()

manager = pygame_gui.UIManager(size)
difficulty = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
    options_list=['easy', 'medium', 'hard'],
    starting_option='easy',
    relative_rect=pygame.Rect((610, 660), (70, 30)),
    manager=manager
)
rules = pygame_gui.windows.UIMessageWindow(
        rect=pygame.Rect((100, 100), (400, 400)),
        html_message="Дорогой фермер! " +
                     "Добро пожаловать, у нас очень много работы!!! " +
                     "Вам нужно будет пасти 15 овец, не допустив того, чтобы они были съедены волками или убежали в лес навсегда. " +
                     "Для этого нужно булет управлять гончими и ковбоями. " +
                     "Для этого нажмите на них, потом на соеднюю клетку. " +
                     "Количество ходов ваших героев ограничено. " +
                     "Ковобой - 3 хода, гончая - 4 хода. " +
                     "Ковбои не могут заходить в кусты (тёмно-зелёная зона травы), но могут сдвигать барашек, если походят на них. " +
                     "Проживите 20 ходов и под конец игры загоните овец обратно в сохранную зону. " +
                     "Иначе они умрут:(",
        manager=manager,
        window_title="rules")
new_game = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((400, 500), (100, 50)),
                    text="start new game", manager=manager, visible=0

                )


def new_game_start():
    global count_turn, game_score, new_game
    count_turn = 0
    game_score = 0
    for i in game_over:
        i.image = load_image("empty.png")
    for i in animals:
        i.death()
    for i in cowboys:
        i.death()
    for i in game_over:
        i.active = False
    # new_game.visible = 0
    map_new = load_level("lvl1.txt")
    with open("heroes.txt", "w", encoding="utf-8") as file:
        for i in range(len(map_new)):
            if i != len(map_new) - 1:
                file.write(map_new[i] + '\n')
            else:
                file.write(map_new[i])



    # print("start_new")


def select_lvl_difficukty(lvl, event):
    if lvl == "easy":
        schedule.every(7).seconds.do(next_turn_sheep, event)
        schedule.every(5).seconds.do(next_turn_wolfs, event)
    elif lvl == "medium":
        schedule.every(6).seconds.do(next_turn_sheep, event)
        schedule.every(4).seconds.do(next_turn_wolfs, event)
    elif lvl == "hard":
        schedule.every(5).seconds.do(next_turn_sheep, event)
        schedule.every(4).seconds.do(next_turn_wolfs, event)


def load_image(name, colorkey=None):
    fullname = os.path.join(PIC_DIR, name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, 'n'), level_map))


def find_cell(x, y):
    p_y = y // cell_size
    p_x = x // cell_size
    return (p_x, p_y)


def find_hero(x, y, animals_map):
    return animals_map[y][x]


def return_hero(x, y, group):
    for i in group:
        if i.rect.x // cell_size == x and i.rect.y // cell_size == y:
            return i
    return None


def ret_lvl_diff():
    return lvl_difficult

def spam_animals(animals_map):
    count = 0
    for i in range(len(animals_map)):
        for j in range(len(animals_map[i])):
            if find_hero(j, i, animals_map) == "s":
                Ship(j, i, count, ships)
                count += 1
                # print(x.rect.x // cell_size, x.rect.y // cell_size, x.id)
            elif find_hero(j, i, animals_map) == "d":
                Dog(j, i, dogs)
            elif find_hero(j, i, animals_map) == "c":
                Cowboy(j, i, cowboys)
    for i in range(len(animals_map)):
        for j in range(len(animals_map[i])):
            if find_hero(j, i, animals_map) == "w":
                Wolf(j, i, wolfs)

def count_score_():
    return game_score

def count_turn_():
    return count_turn

def next_turn_sheep(event):
    global game_score, count_turn
    count = 0
    for i in ships:
        if i.alive:
            count += 1
    if count > 0:
        sheep_sound.play()
        # print(count_turn)
        count_turn += 1
        count = count_turn
        ships.update(event)
        for i in cowboys:
            i.count = 3
        for i in dogs:
            i.count = 4
        if count % 10 == 0:
            if lvl_difficult == "easy":
                iter = 3
            elif lvl_difficult == "medium":
                iter = 4
            else:
                iter = 5
            for i in range(iter):
                f = load_level("heroes.txt")
                coor = [0, 0]
                line = random.randint(1, 3)
                if line == 1 or line == 3:
                    if line == 1:
                        coor[0] = 1
                    else:
                        coor[0] = board_w - 2
                    coor[1] = random.randint(2, 9)
                    while f[coor[1]][coor[0]] != "n":
                        coor[1] = random.randint(2, 9)
                elif line == 2:
                    coor[1] = 2
                    coor[0] = random.randint(1, 23)
                    while f[coor[1]][coor[0]] != "n":
                        coor[0] = random.randint(1, 24)
                Wolf(coor[0], coor[1], wolfs)
        for i in ships:
            if i.alive:
                game_score += 1
        # print(game_score)
    else:
        count = 0
        for i in game_over:
            if i.active:
                count += 1
        if count == 0:
            GameOver(game_over)



def render_score(screen, count):
    font = pygame.font.Font(None, 24)
    text = font.render(f"очки: {count}", 1, (20, 20, 20))
    screen.blit(text, (710, 740))


def next_turn_wolfs(event):
    count = 0
    for i in ships:
        if i.alive:
            count += 1
    if count > 0:
        wolfs.update(event)
        count1 = 0
        for i in wolfs:
            if i.alive:
                count1 += 1
        if count1 > 0:
            # print("sound_wolf")
            wolf_sound.play(maxtime=1000)
    else:
        count = 0
        for i in game_over:
            if i.active:
                count += 1
        if count == 0:
            GameOver(game_over)


def check_for_heroes(x, y, f):
    needed = ["s", "c", "d"]
    if (f[y][x-1] in needed or f[y][x+1] in needed) or (f[y+1][x-1] in needed or f[y+1][x] in needed or f[y+1][x+1] in needed) or\
            (f[y-1][x] in needed or f[y-1][x+1] in needed or f[y-1][x-1] in needed):
        return True


def death_around(x, y, f):
    h = []
    h.append(return_hero(x, y-1, f))
    h.append(return_hero(x, y+1, f))
    h.append(return_hero(x+1, y-1, f))
    h.append(return_hero(x+1, y, f))
    h.append(return_hero(x+1, y+1, f))
    h.append(return_hero(x-1, y-1, f))
    h.append(return_hero(x-1, y, f))
    h.append(return_hero(x-1, y+1, f))
    for i in h:
        if i != None:
            if i.type != "w":
                i.death()

def delete(x, y, lvl):
    # print(x, y)
    # f[y_ch] = f[y_ch][:x_ch] + "n" + f[y_ch][x_ch + 1:]
    lvl[y] = lvl[y][:x] + "n" + lvl[y][x+1:]
    with open("heroes.txt", 'w', encoding="utf-8") as file:
        for i in range(len(lvl)):
            # print(lvl[i])
            if i != len(lvl) - 1:
                file.write(lvl[i] + '\n')
            else:
                file.write(lvl[i])

def appear(x, y, smt, lvl):
    lvl[y] = lvl[y][:x] + smt + lvl[y][x + 1:]
    with open("heroes.txt", 'w', encoding="utf-8") as file:
        for i in range(len(lvl)):
            # print(lvl[i])
            if i != len(lvl) - 1:
                file.write(lvl[i] + '\n')
            else:
                file.write(lvl[i])


class GameOver(pygame.sprite.Sprite):
    image = load_image("gameover.png", -1)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = GameOver.image
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect[2]
        self.rect.y = 0
        self.count = 0
        self.active = True

    def update(self, game_screen, *args):
        if self.rect[0] + self.rect[2] <= cell_size*board_w:
            self.rect = self.rect.move(10, 0)
        else:
            if self.count == 0:
                # pygame.time.wait(1000)
                # self.rect = self.rect.move(-10, 0)
                font = pygame.font.Font(None, 100)
                text = font.render(f"{game_score}", 1, (255, 20, 20))
                game_screen.blit(text, (450, 470))
                new_game.visible = 1



class Fild:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(f"{MAPS_DIR}/{filename}")
        self.h = self.map.height
        self.w = self.map.width
        self.tile_size = self.map.tilewidth

    def render(self, screen):
        ti = self.map.get_tile_image_by_gid
        for layer in self.map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        screen.blit(tile, (x*self.tile_size, y*self.tile_size))


class It(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name, *group,  hp=1, count=1):
        super().__init__(*group)
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.rect.x = x*cell_size
        self.rect.y = y*cell_size
        self.hp = hp
        self.alive = True
        self.count = count

    def update(self, event, move=cell_size):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.rect = self.rect.move(-move, 0)
            elif event.key == pygame.K_RIGHT:
                self.rect = self.rect.move(move, 0)
            elif event.key == pygame.K_UP:
                self.rect = self.rect.move(0, -move)
            elif event.key == pygame.K_DOWN:
                self.rect = self.rect.move(0, move)

    def death(self):
        self.image = load_image("empty.png")
        self.alive = False
        x_ch, y_ch = self.rect.x // cell_size, self.rect.y//cell_size
        delete(x_ch, y_ch, load_level('heroes.txt'))


class Ship(It):
    def __init__(self, x, y, id, *group, image_name="ship.png"):
        super().__init__(x, y, image_name, *group)
        self.vector_left = 0
        self.vector_right = 0
        self.vector_up = 3
        self.vector_down = 0
        self.alive = True
        self.type = "s"
        self.id = id
        self.add(animals)
        self.add(good_gays)


    def update(self, event, move=cell_size):
        if self.alive:
            x_ch, y_ch = self.rect.x // cell_size, self.rect.y // cell_size
            x = random.randint(self.vector_left-1, self.vector_right+1)
            y = random.randint(self.vector_down-1, self.vector_up+1)
            move = [0, 0]
            if x > 0:
                move[0] = 1
            elif x < 0:
                move[0] = -1
            if y > 0:
                move[1] = -1
            elif y < 0:
                move[1] = 1
            f_s = load_level("saved_map.txt")
            f = load_level("heroes.txt")
            try:
                if f[y_ch + move[1]][x_ch + move[0]] == "t":
                    raise IndexError
                # print((f_s[y_ch+move[1]][x_ch+move[0]] == "n" or f_s[y_ch+move[1]][x_ch+move[0]] == "s") and f[y_ch+move[1]][x_ch+move[0]] == "n")
                if (f_s[y_ch+move[1]][x_ch+move[0]] == "f" or f_s[y_ch+move[1]][x_ch+move[0]] == "h" or f_s[y_ch+move[1]][x_ch+move[0]] == "s") and\
                        f[y_ch+move[1]][x_ch+move[0]] == "n":
                    self.rect = self.rect.move(move[0]*cell_size, move[1]*cell_size)
                    delete(x_ch, y_ch, f)
                    appear(x_ch+move[0], y_ch+move[1], "s", f)
                if f_s[y_ch+move[1]][x_ch+move[0]] == "f":
                    self.image = load_image("ship.png")
                elif f_s[y_ch+move[1]][x_ch+move[0]] == "h":
                    self.image = load_image("sheep_hide.png")

            except IndexError:
                self.alive = False
                delete(x_ch, y_ch, f)
                self.image = load_image("empty.png")


    def moveee(self, move):
        # print('move', move)
        f_s = load_level("saved_map.txt")
        f = load_level("heroes.txt")
        x_ch, y_ch = self.rect.x // cell_size, self.rect.y // cell_size
        try:
            if f[y_ch + move[1]][x_ch + move[0]] == "t":
                raise IndexError
            # print((f_s[y_ch + move[1]][x_ch + move[0]] == "n" or f_s[y_ch + move[1]][x_ch + move[0]] == "s") and
            #       f[y_ch + move[1]][x_ch + move[0]] == "n")
            if (f_s[y_ch+move[1]][x_ch+move[0]] == "f" or f_s[y_ch+move[1]][x_ch+move[0]] == "h" or f_s[y_ch + move[1]][x_ch + move[0]] == "s") and \
                    f[y_ch + move[1]][x_ch + move[0]] == "n":
                self.rect = self.rect.move(move[0] * cell_size, move[1] * cell_size)
                delete(x_ch, y_ch, f)
                appear(x_ch + move[0], y_ch + move[1], "s", f)
            if f_s[y_ch + move[1]][x_ch + move[0]] == "f":
                self.image = load_image("ship.png")
            elif f_s[y_ch + move[1]][x_ch + move[0]] == "h":
                self.image = load_image("sheep_hide.png")

        except IndexError:
            # print('1!!!!!')
            delete(x_ch, y_ch, f)
            self.image = load_image("empty.png")
            self.alive = False

    def death(self):
        super().death()


class Wolf(It):
    def __init__(self, x, y, *group, image_name="wolf.png"):
        # print('spam wolf')
        super().__init__(x, y, image_name, *group)
        self.type = "w"
        self.the_ship = None
        self.add(animals)
        self.add(good_gays)

        f = load_level("heroes.txt")
        f[y] = f[y][:x] + "w" + f[y][x+1:]
        with open("heroes.txt", 'w', encoding="utf-8") as file:
            for i in range(len(f)):
                if i != len(f) - 1:
                    file.write(f[i] + '\n')
                else:
                    file.write(f[i])
        count = 0
        count1 = 0
        for i in ships:
            count1+=1
            if i.alive:
                count += 1
        # print(count, "count", count1, 'count1')
        if count != 0:
            sheep_need_id = random.randint(0, count-1)
            count = 0
            for i in ships:
                if i.alive:
                    if count == sheep_need_id:
                        self.the_ship = i
                        # print(sheep_need_id, count, i.type, i.id, 'id')
                        # print("end spam", count, self.the_ship == None, i.rect.x//cell_size, i.rect.y//cell_size)

                        break
                    count += 1
        else:
            self.the_ship = None

    def update(self, event, move=cell_size):
        if self.alive:
            if not self.the_ship.alive:
                # ищем новую овцу
                count = 0
                for i in ships:
                    if i.alive:
                        count += 1
                # print(count, "count")
                if count != 0:
                    sheep_need_id = random.randint(0, count - 1)
                    count = 0
                    for i in ships:
                        if i.alive:
                            if count == sheep_need_id:
                                self.the_ship = i
                                break
                            count += 1
                else:
                    self.the_ship = None

            if self.the_ship != None:
                # если овца есть
                # print("wolf move")
                x_sheep = self.the_ship.rect.x // cell_size
                y_sheep = self.the_ship.rect.y // cell_size
                move = [0, 0]
                x_ch, y_ch = self.rect.x//cell_size, self.rect.y//cell_size
                x, y = x_sheep - x_ch, y_sheep - y_ch
                if x > 0:
                    move[0] = 1
                elif x < 0:
                    move[0] = -1
                if y > 0:
                    move[1] = 1
                elif y < 0:
                    move[1] = -1
                # print('move:', move)
                f_s = load_level("saved_map.txt")
                f = load_level("heroes.txt")
                try:
                    if check_for_heroes(x_ch, y_ch, f):
                        # если есть кого убить, убиваем
                        death_around(x_ch, y_ch, good_gays)
                    elif (f_s[y_ch + move[1]][x_ch + move[0]] == "f" or f_s[y_ch + move[1]][x_ch + move[0]] == "h") and f[y_ch + move[1]][x_ch + move[0]] == "n":
                        # ходим если можем
                        self.rect = self.rect.move(move[0] * cell_size, move[1] * cell_size)
                        delete(x_ch, y_ch, f)
                        appear(x_ch+move[0], y_ch+move[1], "w", f)
                        if f_s[y_ch + move[1]][x_ch + move[0]] == "f":
                            self.image = load_image("wolf.png")
                        elif f_s[y_ch + move[1]][x_ch + move[0]] == "h":
                            self.image = load_image("wolf_hide.png")
                except IndexError:
                    print('error wolf')
                # self.alive = False
                # print('1!')
                # f[y_ch] = f[y_ch][:x_ch] + "n" + f[y_ch][x_ch + 1:]
                # print(f)
                # with open("heroes.txt", 'w', encoding="utf-8") as file:
                #     for i in f:
                #         file.write(i + '\n')
                # self.image = load_image("empty.png")



class Dog(It):
    def __init__(self, x, y, *group, image_name="dog.png"):
        super().__init__(x, y, image_name, *group, count=4)
        self.type = "d"
        self.add(good_gays)
        self.add(animals)

    def move(self, x, y, x_ch, y_ch):
        if self.count > 0:
            f = load_level("saved_map.txt")
            f_h = load_level("heroes.txt")
            if self.count > 0 and (f[y][x] == "f" or f[y][x] == "h") and f_h[y][x] == "n":
                appear(x, y, "d", f_h)
                delete(x_ch, y_ch, f_h)
                self.rect.x = x * cell_size
                self.rect.y = y * cell_size
                self.count -= 1
            if f[y][x] == "f":
                self.image = load_image("dog.png")
            elif f[y][x] == "h":
                self.image = load_image("dog_hide.png")


class Cowboy(It):
    def __init__(self, x, y, *group, image_name="cowboy.png"):
        super().__init__(x, y, image_name, *group, count=3)
        self.type = "c"
        self.add(good_gays)

    def move(self, x, y, x_ch, y_ch):
        print("cowboy move!!")
        f = load_level("saved_map.txt")
        if self.count > 0 and f[y][x] == "f":
            f = load_level("heroes.txt")
            appear(x, y, "c", f)
            delete(x_ch, y_ch, f)
            self.rect.x = x * cell_size
            self.rect.y = y * cell_size
            self.count -= 1


# print(111)