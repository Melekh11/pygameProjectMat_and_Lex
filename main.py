from classes import *


def main():
    pygame.init()
    game_screen = pygame.display.set_mode(size)
    pygame.display.set_caption('A little farm')

    # начинается main
    hero_chosen = None
    x_chosen = None
    y_chosen = None

    fild = Fild("final_fild.tmx")
    clock = pygame.time.Clock()
    running = True
    fps = 30
    animals_map_start = load_level("heroes.txt")
    spam_animals(animals_map_start)
    event = None

    schedule.every(5).seconds.do(next_turn_sheep, None)
    schedule.every(4).seconds.do(next_turn_wolfs, None)
    while running:
        # count_turns = count_turn_()
        schedule.run_pending()
        for event in pygame.event.get():
            manager.process_events(event)

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    lvl = event.text
                    # schedule.cancel_job(schedule.every(7).seconds.do(next_turn_sheep, None))
                    schedule.clear()

                    if lvl == "easy":
                        # print(1)
                        schedule.every(5).seconds.do(next_turn_sheep, None)
                        schedule.every(4).seconds.do(next_turn_wolfs, None)
                    elif lvl == "medium":
                        # print(2)
                        schedule.every(4).seconds.do(next_turn_sheep, None)
                        schedule.every(3).seconds.do(next_turn_wolfs, None)
                    else:
                        schedule.every(3).seconds.do(next_turn_sheep, None)
                        schedule.every(2).seconds.do(next_turn_wolfs, None)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if new_game != None:
                        if event.ui_element == new_game:
                            schedule.clear()
                            new_game_start()
                            new_game.visible = 0
                            game_screen = None
                            pygame.quit()
                            main()


            if event.type == pygame.MOUSEBUTTONDOWN:
                print("tab!!!")
                animals_map = load_level("heroes.txt")
                lvl = load_level('saved_map.txt')
                x, y = find_cell(event.pos[0], event.pos[1])
                if hero_chosen == None or find_hero(x, y, animals_map) == "c" or find_hero(x, y, animals_map) == "d":
                    if find_hero(x, y, animals_map) == "c":
                        hero_chosen = return_hero(x, y, cowboys)
                        is_chosen = True
                        x_chosen = x
                        y_chosen = y
                        print(1, find_hero(x, y, animals_map) == "c")
                        print(hero_chosen.type)
                    elif find_hero(x, y, animals_map) == "d":
                        hero_chosen = return_hero(x, y, dogs)
                        is_chosen = True
                        x_chosen = x
                        y_chosen = y
                        # print(1)
                        # print(hero_chosen.type)
                else:
                    if x_chosen != None:
                        if abs(x - x_chosen) >= 2 or abs(y - y_chosen) >= 2:
                            print(10)
                            is_chosen = False
                            x_chosen = None
                            y_chosen = None
                        else:
                            if return_hero(x, y, animals) == None:
                                print(5)
                                hero_chosen.move(x, y, x_chosen, y_chosen)
                                if hero_chosen.type == "d":
                                    dog_sound.play(maxtime=800)
                                if hero_chosen.count <= 0:
                                    is_chosen = False
                                    x_chosen = None
                                    y_chosen = None
                                    hero_chosen = None
                                    print(13)
                                else:
                                    f = load_level("saved_map.txt")
                                    if x == hero_chosen.rect.x // cell_size and y == hero_chosen.rect.y//cell_size:
                                        x_chosen = x
                                        y_chosen = y
                                    # if f[y][x] == "f" and hero_chosen.type == "c":
                                    #     delete(x_chosen, y_chosen, load_level('heroes.txt'))
                                    #     x_chosen = x
                                    #     y_chosen = y
                                    #     hero_chosen.rect.x, hero_chosen.rect.y = x_chosen*cell_size, y*cell_size
                                    #     appear(x_chosen, y_chosen, 'c', load_level('heroes.txt'))
                                    #
                                    # elif (f[y][x] == "f" or f[y][x] == "h") and hero_chosen.type == "d":
                                    #     delete(x_chosen, y_chosen, load_level('heroes.txt'))
                                    #     x_chosen = x
                                    #     y_chosen = y
                                    #     hero_chosen.rect.x, hero_chosen.rect.y = x_chosen * cell_size, y * cell_size
                                    #     appear(x_chosen, y_chosen, 'd', load_level('heroes.txt'))

                            elif return_hero(x, y, animals).type == "s" and hero_chosen.type == "c" and lvl[y][x] == 'f':
                                print(123)
                                ship_punched = return_hero(x, y, ships)
                                # print(ship_punched.rect.x//cell_size, x_chosen, "xxx")
                                # print(ship_punched.rect.y//cell_size, y_chosen, "yyy")
                                ship_punched.moveee([ship_punched.rect.x//cell_size - x_chosen, ship_punched.rect.y//cell_size-y_chosen])
                                hero_chosen.count -= 1
                            elif return_hero(x, y, animals).type == "w" and hero_chosen.type == "c" and lvl[y][x] == 'f':
                                wolf_dead = return_hero(x, y, wolfs)
                                wolf_dead.death()
                                hero_chosen.count -= 1

                            elif return_hero(x, y, animals).type == "w" and hero_chosen.type == "d":
                                dog_sound.play(maxtime=800)
                                wolf_dead = return_hero(x, y, wolfs)
                                wolf_dead.death()
                                delete(hero_chosen.rect.x//cell_size, hero_chosen.rect.y//cell_size, load_level("heroes.txt"))
                                appear(x, y, "d", load_level("heroes.txt"))
                                hero_chosen.rect.x, hero_chosen.rect.y = x * cell_size, y * cell_size
                                f = load_level("saved_map.txt")
                                if f[y][x] == "f":
                                    hero_chosen.image = load_image("dog.png")
                                elif f[y][x] == "h":
                                    hero_chosen.image = load_image("dog_hide.png")
                                hero_chosen.count -= 1

        manager.update(clock.tick(fps) / 1000.0)
        fild.render(game_screen)
        animals.draw(game_screen)
        cowboys.draw(game_screen)
        render_score(game_screen, count_score_())
        # print("game_score1 ", game_score)
        manager.draw_ui(game_screen)
        game_over.draw(game_screen)
        for i in game_over:
            if i.active:
                # i.draw(game_screen)
                i.update(game_screen, event)

        # game_over.update(game_screen, event)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()

    with open("heroes.txt", "w", encoding="utf-8") as file:
        for i in range(len(animals_map_start)):
            if i != len(animals_map_start)-1:
                file.write(animals_map_start[i]+'\n')
            else:
                file.write(animals_map_start[i])


if __name__ == "__main__":
    # print(12345)
    main()