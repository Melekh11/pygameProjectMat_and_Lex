from classes import *


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


def spam_animals(animals_map):
    for i in range(len(animals_map)):
        for j in range(len(animals_map[i])):
            if find_hero(j, i, animals_map) == "s":
                Ship(j, i, ships)
            elif find_hero(j, i, animals_map) == "w":
                Wolf(j, i, wolfs)
            elif find_hero(j, i, animals_map) == "d":
                Dog(j, i, dogs)
            elif find_hero(j, i, animals_map) == "c":
                Cowboy(j, i, cowboys)


def main():
    hero_chosen = None
    is_chosen = False
    x_chosen = None
    y_chosen = None

    fild = Fild("final_fild.tmx")
    clock = pygame.time.Clock()
    running = True
    fps = 30
    animals_map_start = load_level("heroes.txt")
    spam_animals(animals_map_start)
    while running:
        animals_map = animals_map_start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = find_cell(event.pos[0], event.pos[1])
                if hero_chosen == None or find_hero(x, y, animals_map) == "c" or find_hero(x, y, animals_map) == "d":
                    if find_hero(x, y, animals_map) == "c":
                        hero_chosen = return_hero(x, y, cowboys)
                        is_chosen = True
                        x_chosen = x
                        y_chosen = y
                        print(1)
                        print(hero_chosen.type)
                    elif find_hero(x, y, animals_map) == "d":
                        hero_chosen = return_hero(x, y, dogs)
                        is_chosen = True
                        x_chosen = x
                        y_chosen = y
                        print(1)
                        print(hero_chosen.type)
                else:
                    if abs(x - x_chosen) >= 2 or abs(y - y_chosen) >= 2:
                        print(10)
                        is_chosen = False
                        x_chosen = None
                        y_chosen = None
                    else:
                        if return_hero(x, y, animals) == None:
                            print(5)
                            hero_chosen.move(x, y, x_chosen, y_chosen)
                            if hero_chosen.count <= 0:
                                is_chosen = False
                                x_chosen = None
                                y_chosen = None
                                hero_chosen = None
                            else:
                                with open("saved_map.txt", "r", encoding="utf-8") as file:
                                    f = file.readlines()
                                if f[y][x] == "f":
                                    x_chosen = x
                                    y_chosen = y
                        else:
                            print("!!")
                print(is_chosen)
                print('')

        fild.render(game_screen)
        animals.draw(game_screen)
        cowboys.draw(game_screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()