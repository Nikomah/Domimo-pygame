
import random
from objects import *
import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1500, 900))
screen.fill(color='aquamarine4')

dict_of_endpoints = {'end_point_nominal': {'left': 0, 'right': 0},
                     'end_point_coord': {'left': (0, 0), 'right': (0, 0)}
                     }  # End denomination values and coordinates for the next turn chip.

player_list = []  # A list of the denominations of the dice held by the player.
bar_list = []  # A list of the denominations of the dice in the bar.
robot_list = []  # A list of the denominations of the dice held by the robot.

player_group = pygame.sprite.Group()  # Sprites of the player's bones.
bar_group = pygame.sprite.Group()  # Sprites of bones in the bar.
robot_group = pygame.sprite.Group()  # Sprites of the robot bones.

empty_coord_player = [(x, 790) for x in range(520, 1320, 60)]  # Coordinates of empty player sprites.
empty_coord_robot = [(x, 10) for x in range(520, 1320, 60)]  # Coordinates of empty robot sprites.


def draw_bar_space():
    bar_space = pygame.Surface((250, 500))
    bar_space.fill(color='cyan3')
    bar_space_rect = bar_space.get_rect()
    bar_space_rect.topleft = (1250, 200)
    screen.blit(bar_space, bar_space_rect)


def draw_bar():
    bar_flag = 0
    bar_coords = [(1260, 220), (1320, 220), (1380, 220), (1440, 220),
                  (1260, 340), (1320, 340), (1380, 340), (1440, 340),
                  (1260, 460), (1320, 460), (1380, 460), (1440, 460),
                  (1260, 580), (1320, 580)]
    while len(bar_list) < 14:
        nominal = random.choice(all_bone_list)
        if nominal not in bar_list:
            bar_list.append(nominal)
            for b in bones:
                if b.nominal == nominal:
                    b.add(bar_group)
                    b.rect.topleft = bar_coords[bar_flag]
                    screen.blit(b.back_image, b.rect)
                    bar_flag += 1
    del bar_coords
    del bar_flag


def draw_player_room():
    player_flag = 0
    player_coords = [(x, 790) for x in range(100, 480, 60)]
    while len(player_list) < 7:
        nominal = random.choice(all_bone_list)
        if nominal not in bar_list and nominal not in player_list:
            player_list.append(nominal)
            for b in bones:
                if b.nominal == nominal:
                    b.add(player_group)
                    b.rect.topleft = player_coords[player_flag]
                    screen.blit(b.image, b.rect)
                    player_flag += 1
    del player_coords
    del player_flag


def draw_robot_room():
    robot_flag = 0
    robot_coords = [(x, 10) for x in range(100, 480, 60)]
    last_list = [x for x in all_bone_list if x not in bar_list and x not in player_list]
    while len(robot_list) < 7:
        for b in bones:
            if b.nominal in last_list:
                robot_list.append(b.nominal)
                b.add(robot_group)
                b.rect.topleft = robot_coords[robot_flag]
                screen.blit(b.back_image, b.rect)
                robot_flag += 1
    del robot_coords
    del last_list
    del robot_flag


def draw_start_table():
    draw_bar()
    draw_player_room()
    draw_robot_room()
    pygame.display.flip()


def player_click(x_pos, y_pos):
    for bone in player_group:
        if bone.rect.topleft[1] == 780:
            bg = Bg('t')
            bg.rect.topleft = bone.rect.topleft
            screen.blit(bg.image, bg.rect)
            bone.rect.move_ip(0, 10)
            screen.blit(bone.image, bone.rect)
            pygame.display.update([bone.rect, bg.rect])
        else:
            if bone.rect.collidepoint(x_pos, y_pos):
                if bone.nominal[0] in dict_of_endpoints['end_point_nominal'].values()\
                        or bone.nominal[1] in dict_of_endpoints['end_point_nominal'].values():
                    bg = Bg('t')
                    bg.rect.topleft = bone.rect.topleft
                    screen.blit(bg.image, bg.rect)
                    bone.rect.move_ip(0, -10)
                    screen.blit(bone.image, bone.rect)
                    pygame.display.update([bone.rect, bg.rect])


def horizont_turn_1(bone, flag):
    bone.rect.center = dict_of_endpoints['end_point_coord'][flag]
    if bone.double:
        if flag == 'left':
            bone.rect.move_ip(25, 0)
            dict_of_endpoints['end_point_coord'][flag] = (bone.rect.center[0] - 75, bone.rect.center[1])
        if flag == 'right':
            bone.rect.move_ip(-25, 0)
            dict_of_endpoints['end_point_coord'][flag] = (bone.rect.center[0] + 75, bone.rect.center[1])
        dict_of_endpoints['end_point_nominal'][flag] = bone.nominal[0]
        screen.blit(bone.image, bone.rect)
        pygame.display.update(bone.rect)
    else:
        if bone.nominal[0] == dict_of_endpoints['end_point_nominal'][flag]:
            if flag == 'left':
                new_image = pygame.transform.rotate(bone.image, -90)
            else:
                new_image = pygame.transform.rotate(bone.image, 90)
            dict_of_endpoints['end_point_nominal'][flag] = bone.nominal[1]
        else:
            if flag == 'left':
                new_image = pygame.transform.rotate(bone.image, 90)
            else:
                new_image = pygame.transform.rotate(bone.image, -90)
            dict_of_endpoints['end_point_nominal'][flag] = bone.nominal[0]
        new_rect = new_image.get_rect()
        new_rect.center = dict_of_endpoints['end_point_coord'][flag]
        if flag == 'left':
            dict_of_endpoints['end_point_coord'][flag] = (new_rect.center[0] - 100, new_rect.center[1])
        if flag == 'right':
            dict_of_endpoints['end_point_coord'][flag] = (new_rect.center[0] + 100, new_rect.center[1])
        screen.blit(new_image, new_rect)
        pygame.display.update(new_rect)


def horizont_turn_2(bone, flag):
    bone.rect.center = dict_of_endpoints['end_point_coord'][flag]
    if bone.double:
        if flag == 'right':
            bone.rect.move_ip(25, 0)
            dict_of_endpoints['end_point_coord'][flag] = (bone.rect.center[0] - 75, bone.rect.center[1])
        if flag == 'left':
            bone.rect.move_ip(-25, 0)
            dict_of_endpoints['end_point_coord'][flag] = (bone.rect.center[0] + 75, bone.rect.center[1])
        dict_of_endpoints['end_point_nominal'][flag] = bone.nominal[0]
        screen.blit(bone.image, bone.rect)
        pygame.display.update(bone.rect)
    else:
        if bone.nominal[0] == dict_of_endpoints['end_point_nominal'][flag]:
            if flag == 'right':
                new_image = pygame.transform.rotate(bone.image, -90)
            else:
                new_image = pygame.transform.rotate(bone.image, 90)
            dict_of_endpoints['end_point_nominal'][flag] = bone.nominal[1]
        else:
            if flag == 'right':
                new_image = pygame.transform.rotate(bone.image, 90)
            else:
                new_image = pygame.transform.rotate(bone.image, -90)
            dict_of_endpoints['end_point_nominal'][flag] = bone.nominal[0]
        new_rect = new_image.get_rect()
        new_rect.center = dict_of_endpoints['end_point_coord'][flag]
        if flag == 'right':
            dict_of_endpoints['end_point_coord'][flag] = (bone.rect.center[0] - 100, bone.rect.center[1])
        if flag == 'left':
            dict_of_endpoints['end_point_coord'][flag] = (bone.rect.center[0] + 100, bone.rect.center[1])
        screen.blit(new_image, new_rect)
        pygame.display.update(new_rect)


def vertical_turn(bone, flag):
    bone.rect.center = dict_of_endpoints['end_point_coord'][flag]
    if bone.double:
        new_image = pygame.transform.rotate(bone.image, 90)
        new_rect = new_image.get_rect()
        if flag == 'left':
            new_rect.center = dict_of_endpoints['end_point_coord']['left']
            new_rect.move_ip(0, 25)
            dict_of_endpoints['end_point_coord'][flag] = 50, new_rect.center[1] - 75
        if flag == 'right':
            new_rect.center = dict_of_endpoints['end_point_coord']['right']
            new_rect.move_ip(0, -25)
            dict_of_endpoints['end_point_coord'][flag] = 1200, new_rect.center[1] + 75
        dict_of_endpoints['end_point_nominal'][flag] = bone.nominal[0]
        screen.blit(new_image, new_rect)
        pygame.display.update(new_rect)

    else:
        if bone.nominal[0] == dict_of_endpoints['end_point_nominal'][flag]:
            if flag == 'left':
                new_image = pygame.transform.rotate(bone.image, 180)
                new_rect = new_image.get_rect()
                new_rect.center = dict_of_endpoints['end_point_coord']['left']
                dict_of_endpoints['end_point_coord'][flag] = 50, bone.rect.center[1] - 100
                screen.blit(new_image, new_rect)
                pygame.display.update(new_rect)
            if flag == 'right':
                dict_of_endpoints['end_point_coord'][flag] = 1200, bone.rect.center[1] + 100
                screen.blit(bone.image, bone.rect)
                pygame.display.update(bone.rect)
            dict_of_endpoints['end_point_nominal'][flag] = bone.nominal[1]
        else:
            if flag == 'left':
                dict_of_endpoints['end_point_coord'][flag] = 50, bone.rect.center[1] - 100
                screen.blit(bone.image, bone.rect)
                pygame.display.update(bone.rect)
            if flag == 'right':
                new_image = pygame.transform.rotate(bone.image, 180)
                new_rect = new_image.get_rect()
                new_rect.center = dict_of_endpoints['end_point_coord']['right']
                dict_of_endpoints['end_point_coord'][flag] = 1200, bone.rect.center[1] + 100
                screen.blit(new_image, new_rect)
                pygame.display.update(new_rect)
            dict_of_endpoints['end_point_nominal'][flag] = bone.nominal[0]


def calc_to_vertical(flag):
    if flag == 'left':
        for bone in bones:
            if bone.rect.center[0] <= 100 and bone.rect.center[1] == 450:
                if bone.double:
                    dict_of_endpoints['end_point_coord'][flag] = 50, 350
                else:
                    dict_of_endpoints['end_point_coord'][flag] = 50, 375
                bone.remove(bones)
                break
    if flag == 'right':
        for bone in bones:
            if bone.rect.center[0] >= 1150 and bone.rect.center[1] == 450:
                if bone.double:
                    dict_of_endpoints['end_point_coord'][flag] = 1200, 550
                else:
                    dict_of_endpoints['end_point_coord'][flag] = 1200, 525
                bone.remove(bones)
                break


def calc_to_horizont(flag):
    if flag == 'left':
        for bone in bones:
            if bone.rect.center[1] <= 250 and bone.rect.center[0] == 50:
                if bone.double:
                    dict_of_endpoints['end_point_coord']['left'] = 150, 170
                else:
                    dict_of_endpoints['end_point_coord']['left'] = 125, 170
                bone.remove(bones)
                break

    if flag == 'right':
        for bone in bones:
            if bone.rect.center[1] >= 650 and bone.rect.center[0] == 1200:
                if bone.double:
                    dict_of_endpoints['end_point_coord']['right'] = 1100, 730
                else:
                    dict_of_endpoints['end_point_coord']['right'] = 1125, 730
                bone.remove(bones)
                break


def left_side(bone):
    if dict_of_endpoints['end_point_coord']['left'][0] >= 50 \
            and dict_of_endpoints['end_point_coord']['left'][1] == 450:
        horizont_turn_1(bone, 'left')
    else:
        calc_to_vertical('left')
    if dict_of_endpoints['end_point_coord']['left'][0] == 50 \
            and 450 > dict_of_endpoints['end_point_coord']['left'][1] >= 170:
        vertical_turn(bone, 'left')
    else:
        calc_to_horizont('left')
    if dict_of_endpoints['end_point_coord']['left'][1] == 170:
        horizont_turn_2(bone, 'left')


def right_side(bone):
    if dict_of_endpoints['end_point_coord']['right'][0] <= 1200 \
            and dict_of_endpoints['end_point_coord']['right'][1] == 450:
        horizont_turn_1(bone, 'right')
    else:
        calc_to_vertical('right')
    if dict_of_endpoints['end_point_coord']['right'][0] == 1200 \
            and 450 < dict_of_endpoints['end_point_coord']['right'][1] <= 730:
        vertical_turn(bone, 'right')
    else:
        calc_to_horizont('right')
    if dict_of_endpoints['end_point_coord']['right'][1] == 730:
        horizont_turn_2(bone, 'right')


def player_move(x_pos):
    for bone in player_group:
        if bone.rect.topleft[1] == 780:
            empty_coord_player.insert(0, (bone.rect.topleft[0], bone.rect.topleft[1] + 10))
            bg = Bg('t')
            bg.rect.topleft = bone.rect.topleft
            bone.remove(player_group)
            player_list.remove(bone.nominal)

            if x_pos < 625:
                if bone.nominal[0] == dict_of_endpoints['end_point_nominal']['left'] or\
                        bone.nominal[1] == dict_of_endpoints['end_point_nominal']['left']:
                    left_side(bone)
                else:
                    right_side(bone)
            if x_pos > 625:
                if bone.nominal[0] == dict_of_endpoints['end_point_nominal']['right'] or\
                        bone.nominal[1] == dict_of_endpoints['end_point_nominal']['right']:
                    right_side(bone)
                else:
                    left_side(bone)
            screen.blit(bg.image, bg.rect)
            pygame.display.update([bone.rect, bg.rect])
            break
    pygame.time.delay(1000)
    robot_find_to_move()


def first_move():
    space = True
    while space:
        if dict_of_endpoints['end_point_coord']['left'] != (0, 0):
            space = False
        else:
            player_double_list = []
            robot_double_list = []
            for bone in player_group:
                if bone.double and bone.nominal[0] != 0:
                    player_double_list.append(bone.nominal[0])
            for bone in robot_group:
                if bone.double and bone.nominal[0] != 0:
                    robot_double_list.append(bone.nominal[0])
            try:
                p = min(player_double_list)
            except ValueError:
                p = 7
            try:
                r = min(robot_double_list)
            except ValueError:
                r = 7
            if p < r:
                for bone in player_group:
                    if bone.nominal == (p, p):
                        bone.remove(player_group)
                        player_list.remove(bone.nominal)
                        empty_coord_player.insert(0, bone.rect.topleft)
                        bg = Bg('t')
                        bg.rect.topleft = bone.rect.topleft
                        dict_of_endpoints['end_point_nominal']['left'] = bone.nominal[0]
                        dict_of_endpoints['end_point_nominal']['right'] = bone.nominal[1]
                        dict_of_endpoints['end_point_coord']['left'] = (625 - 75), 450
                        dict_of_endpoints['end_point_coord']['right'] = (625 + 75), 450
                        bone.rect.center = (625, 450)
                        screen.blit(bone.image, bone.rect)
                        screen.blit(bg.image, bg.rect)
                        pygame.display.update([bone.rect, bg.rect])
                        break
                pygame.time.delay(1000)
                robot_find_to_move()
            elif p == r:
                print_text('NO DOUBLES', 550, 450)
                pygame.time.delay(1000)
                new_table()
            else:
                for bone in robot_group:
                    if bone.nominal == (r, r):
                        bone.remove(robot_group)
                        robot_list.remove(bone.nominal)
                        empty_coord_robot.insert(0, bone.rect.topleft)
                        bg = Bg('t')
                        bg.rect.topleft = bone.rect.topleft
                        dict_of_endpoints['end_point_nominal']['left'] = bone.nominal[0]
                        dict_of_endpoints['end_point_nominal']['right'] = bone.nominal[1]
                        dict_of_endpoints['end_point_coord']['left'] = (625 - 75), 450
                        dict_of_endpoints['end_point_coord']['right'] = (625 + 75), 450
                        bone.rect.center = (625, 450)
                        screen.blit(bone.image, bone.rect)
                        screen.blit(bg.image, bg.rect)
                        pygame.display.update([bone.rect, bg.rect])
                        break


def movie_from_bar(x_pos, y_pos):
    for bone in bar_group:
        if bone.rect.collidepoint(x_pos, y_pos):
            bone.remove(bar_group)
            bar_list.remove(bone.nominal)
            bg = Bg('b')
            bg.rect.topleft = bone.rect.topleft
            coord = empty_coord_player[0]
            empty_coord_player.pop(0)
            bone.rect.topleft = coord
            bone.add(player_group)
            player_list.append(bone.nominal)
            screen.blit(bone.image, bone.rect)
            screen.blit(bg.image, bg.rect)
            pygame.display.update([bone.rect, bg.rect])
            break


def robot_move(robot_bone, flag):
    empty_coord_robot.insert(0, (robot_bone.rect.topleft[0], robot_bone.rect.topleft[1]))
    bg = Bg('t')
    bg.rect.topleft = robot_bone.rect.topleft
    robot_bone.remove(robot_group)
    robot_list.remove(robot_bone.nominal)
    if flag == 'left':
        left_side(robot_bone)
    if flag == 'right':
        right_side(robot_bone)
    screen.blit(bg.image, bg.rect)
    pygame.display.update(bg.rect)

    player_count_list = [x[0] for x in player_list] + [x[1] for x in player_list]
    if len(bar_list) == 0 \
            and dict_of_endpoints['end_point_nominal']['left'] not in player_count_list\
            and (dict_of_endpoints['end_point_nominal']['right'] not in player_count_list):
        pygame.time.delay(1000)
        robot_find_to_move()


def robot_from_bar():
    try:
        nom_bar = random.choice(bar_list)
    except IndexError:
        nom_bar = None
    if nom_bar:
        bar_list.remove(nom_bar)
        robot_list.append(nom_bar)
    for bone in bar_group:
        if bone.nominal == nom_bar:
            coord = empty_coord_robot[0]
            del empty_coord_robot[0]
            bg = Bg('b')
            bg.rect.topleft = bone.rect.topleft
            bone.rect.topleft = coord
            bone.add(robot_group)
            bone.remove(bar_group)
            screen.blit(bone.back_image, bone.rect)
            screen.blit(bg.image, bg.rect)
            pygame.display.update([bone.rect, bg.rect])
            break


def robot_find_to_move():
    if len(player_list) != 0:
        ready_to_move = []
        for nom in robot_list:
            if dict_of_endpoints['end_point_nominal']['left'] in nom \
                    or dict_of_endpoints['end_point_nominal']['right'] in nom:
                ready_to_move.append(nom)
        if len(ready_to_move) > 0:
            try:
                nom_to_move = random.choice(ready_to_move)
            except IndexError:
                nom_to_move = None
            for bone in robot_group:
                if bone.nominal == nom_to_move:
                    if dict_of_endpoints['end_point_nominal']['left'] in bone.nominal:
                        robot_move(bone, 'left')
                    else:
                        robot_move(bone, 'right')
                    break
        elif len(bar_list) == 0:
            print_text('PASS', 620, 300)
            pass_ = pygame.Surface((100, 50))
            pass_rect = pass_.get_rect()
            pass_rect.topleft = 620, 300
            pass_.fill(color='aquamarine4')
            pygame.time.delay(1000)
            screen.blit(pass_, pass_rect)
            pygame.display.update(pass_rect)
        else:
            robot_from_bar()
            pygame.display.update()
            pygame.time.delay(1000)
            robot_find_to_move()
    else:
        pass


def print_text(message, x, y, font_color=(0, 0, 0), font_type='arial', font_size=30, long=250):
    font_type = pygame.font.SysFont(font_type, font_size)
    text = font_type.render(message, True, font_color)
    text_rect = text.get_rect()
    text_rect.topleft = x, y
    text_area = pygame.Surface((long, font_size))
    text_area.fill(color='aquamarine4')
    text_area_rect = text_area.get_rect()
    text_area_rect.topleft = x, y
    screen.blit(text_area, text_area_rect)
    screen.blit(text, (x, y))
    pygame.display.update([text_area_rect, text_rect])


def fish(p_count, r_count, player_count_list, robot_count_list, score):
    if dict_of_endpoints['end_point_nominal']['left'] not in robot_count_list\
            and dict_of_endpoints['end_point_nominal']['left'] not in player_count_list\
            and dict_of_endpoints['end_point_nominal']['right'] not in robot_count_list\
            and dict_of_endpoints['end_point_nominal']['right'] not in player_count_list\
            and len(bar_list) == 0\
            and len(robot_list) != 0\
            and len(player_list) != 0:
        p_count_ = sum(player_count_list)
        r_count_ = sum(robot_count_list)
        if r_count_ > p_count_:
            r_count += r_count_ + p_count_
            print_text(f'robot count: {r_count}', 1300, 60)
            print_text(f'player count: {p_count}', 1300, 800)
        else:
            p_count += p_count_ + r_count_
            print_text(f'robot count: {r_count}', 1300, 60)
            print_text(f'player count: {p_count}', 1300, 800)
        print_text('FISH!', 620, 300, long=80)
        pygame.time.delay(2000)
        if r_count > 101:
            print_text('YOU WIN', 700, 300, long=150)
            score = False
        if p_count > 101:
            print_text('YOU LOST', 700, 300, long=150)
            score = False
        return False, score, p_count, r_count
    else:
        return True, score, p_count, r_count


def count(p_count, r_count, player_count_list, robot_count_list, no_fish):
    if no_fish is True:
        p_count += sum(player_count_list)
        r_count += sum(robot_count_list)
    print_text(f'robot count: {r_count}', 1300, 60)
    print_text(f'player count: {p_count}', 1300, 800)
    if p_count >= 101 or r_count >= 101:
        return False, p_count, r_count
    else:
        return True, p_count, r_count


def new_table():
    dict_of_endpoints['end_point_coord']['left'] = 0, 0
    dict_of_endpoints['end_point_coord']['right'] = 0, 0
    dict_of_endpoints['end_point_nominal']['left'] = 0
    dict_of_endpoints['end_point_nominal']['right'] = 0
    player_list.clear()
    bar_list.clear()
    robot_list.clear()
    empty_coord_player.clear()
    empty_coord_robot.clear()
    all_bone_list.clear()
    for bone in bones:
        bone.kill()
    for bg in bgs:
        bg.kill()
    for x in range(520, 1320, 60):
        empty_coord_player.append((x, 790))
        empty_coord_robot.append((x, 10))
    set_bones()
    draw_bar_space()
    pygame.display.update()
    pygame.time.delay(1000)
    draw_start_table()


def run():
    draw_bar_space()
    draw_start_table()
    player_count = 0
    robot_count = 0
    game = True
    no_fish = True
    score = True
    running = True
    print_text('PRESS SPACE TO MAKE THE FIRST MOVE', 500, 450)
    while running:
        player_count_list = [x[0] for x in player_list] + [x[1] for x in player_list]
        robot_count_list = [x[0] for x in robot_list] + [x[1] for x in robot_list]

        if no_fish:
            no_fish, score, player_count, robot_count = fish(player_count, robot_count,
                                                             player_count_list, robot_count_list, score)

        if len(bar_list) == 0 \
                and dict_of_endpoints['end_point_nominal']['left'] not in player_count_list \
                and (dict_of_endpoints['end_point_nominal']['right'] not in player_count_list) \
                and len(robot_list) > 0 \
                and no_fish is True:
            pygame.time.delay(1000)
            robot_find_to_move()

        if score:
            if len(player_list) == 0 or len(robot_list) == 0 or no_fish is False:
                screen.fill(color='aquamarine4')
                score, player_count, robot_count = count(player_count, robot_count,
                                                         player_count_list, robot_count_list, no_fish)
                if score:
                    pygame.time.delay(1000)
                    new_table()
                    no_fish = True
                else:
                    if robot_count >= 101:
                        print_text('YOU WIN', 600, 300, long=150)
                    else:
                        print_text('YOU LOST', 600, 300, long=150)
                    print_text('PRESS ENTER TO A NEW GAME', 475, 550)
                    game = False
                    score = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEOEXPOSE:  # Window minimization/open
                pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press Enter
                    text_area = pygame.Surface((500, 30))
                    text_area.fill(color='aquamarine4')
                    text_rect = text_area.get_rect()
                    text_rect.topleft = 500, 450
                    screen.blit(text_area, text_rect)
                    pygame.display.update(text_rect)
                    first_move()
                if event.key == pygame.K_RETURN and game is False:
                    player_count = 0
                    robot_count = 0
                    score = True
                    no_fish = True
                    screen.fill(color='aquamarine4')
                    new_table()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                if y > 780:  # Player's room
                    player_click(x, y)
                elif x > 1250 and 110 < y < 790:  # Bar's room
                    movie_from_bar(x, y)
                elif 0 < x < 1250 and 110 < y < 790\
                        and (dict_of_endpoints['end_point_nominal']['left'] in player_count_list or
                             dict_of_endpoints['end_point_nominal']['right'] in player_count_list):  # Main table
                    player_move(x)

        clock.tick(15)


if __name__ == '__main__':
    run()
