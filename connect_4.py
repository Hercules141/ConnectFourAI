import random
import time
import timeit

import pygame

import connect_4

pygame.init()
pygame.font.init()

running = True
playing = True
screen_size = [1000, 600]

game_size = (7, 6)
# game_size = (70, 30)
n_wins = 4
game = [[0 for i in range(game_size[1])] for j in range(game_size[0])]
active_player = 1   #0 empty, 1 player 1, 2 player 2

background_color = (20, 20, 20)
rack_color = (130, 50, 50)
player1_color = (20, 20, 110)
player2_color = (200, 200, 200)
text_color = (255, 255, 255)

rack_size_mul = 90
# rack_size_mul = 20
rack_size = (rack_size_mul*game_size[0], rack_size_mul*game_size[1])
rack_buffer_right = 0.5
hole_size = 1

hitboxes = [[[0, 0, 0, 0] for i in range(game_size[1])] for j in range(game_size[0])]   #[x,y,width,height]

surface = pygame.display.set_mode(screen_size, pygame.RESIZABLE)
pygame.display.set_caption(str(n_wins) + " Gewinnt")
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("Arial Black", 30)

ticks = 0
countGames = 0


def init_game():
    print("have fun!")

def tick():
    global ticks
    print("ticks: ", ticks)

    #draw rack then chips
    pygame.draw.rect(surface, (19, 30, 34), (100, 2, 3, 4))
    draw_game()

    #do stuff like checking stuff and stuff


    #basically updating screen with certain speed
    pygame.display.flip()
    clock.tick(500)

    ticks +=1

def reset_game():
    global game
    game = [[0 for i in range(game_size[1])] for j in range(game_size[0])]

def draw_game():
    width = surface.get_width()
    height = surface.get_height()

    rack_width = rack_size[0]
    rack_height = rack_size[1]
    rack_X = int((width-rack_size[0])/2)
    rack_Y = int((height - rack_size[1])/2)

    surface.fill(background_color)

    #draw rack and store hitboxes of slots
    pygame.draw.rect(surface, rack_color, (rack_X, rack_Y, rack_size[0], rack_size[1]))
    hole_radius = (rack_size[1]/game_size[1])/2
    hole_buffer = 0.25
    first_hole_pos = (rack_X + hole_radius, rack_Y + hole_radius)
    hitbox_size = hole_radius*2
    for column in range(len(game)):
        for row in range(len(game[1])):
            pygame.draw.circle(surface, background_color, (first_hole_pos[0] + column * hole_radius*2,
                                                           first_hole_pos[1] + row * hole_radius*2), hole_radius*(1-hole_buffer))

            hitboxes[column][row] = (int(rack_X + column * hitbox_size),     #x
                                     int(rack_Y + row * hitbox_size),        #y
                                     int(hitbox_size),                       #width
                                     int(hitbox_size))                       #height


    #draw chips
    for column in range(len(game)):
        for row in range(len(game[1])):
            if game[column][row] == 1:
                pygame.draw.circle(surface, player1_color, (first_hole_pos[0] + column * hole_radius*2,
                                                            first_hole_pos[1] + row * hole_radius*2), hole_radius*(1-hole_buffer))
            if game[column][row] == 2:
                pygame.draw.circle(surface, player2_color, (first_hole_pos[0] + column * hole_radius*2,
                                                            first_hole_pos[1] + row * hole_radius*2), hole_radius*(1-hole_buffer))
    #draw Active Player Label
    s = "Player " + str(active_player) + "'s turn"
    text_surface = myfont.render(s, False, text_color)
    surface.blit(text_surface, (20, 10))

def place_chip(col_selected):
    global active_player
    legal = False

    #calculate "gravity" for selected col
    col = game[col_selected]
    for i in range(len(col)-1, -1, -1): #reverse loop '':P (so from top to bottom)
        if col[i] == 0:
            col[i] = active_player
            legal = True
            break
    if legal:   #column not full

        if active_player == 1:
            active_player = 2
        else:
            active_player = 1

def check_win():

    #check for 4 in row, diagonal and vertical
    counter = 0
    color_being_tested = -1 #first of 4 being checked (if other three match -> win)
    winner = -1

    #Part checking vertical matches (omiting part of bottom)
    for col in range(len(game)):
        for row in range(len(game[col])-(n_wins-1)):
            color_being_tested = game[col][row]
            if color_being_tested != 0: #Empty can't win xp
                #start counting consecutive color to 4 downward from this row to see if 4 wins (bottom 3 skipped cause already included)
                for i in range(n_wins):
                    if game[col][row+i] == color_being_tested:
                        counter += 1

                if counter == n_wins:
                    winner = color_being_tested
                    print("vertical win")
                else:
                    counter = 0

    #part checking horizontal matches (omiting part of right)
    for col in range(len(game)-(n_wins-1)):
        for row in range(len(game[col])):
            color_being_tested = game[col][row]
            if color_being_tested != 0: #Empty can't win xp
                #start counting consecutive color to 4 to the right from this row to see if 4 wins (rightmost 3 skipped cause already included)
                for i in range(n_wins):
                    if game[col+i][row] == color_being_tested:
                        counter += 1

                if counter == n_wins:
                    winner = color_being_tested
                    print("horizontal win")
                else:
                    counter = 0


    #part checking diagonal matches descending
    for col in range(len(game) - (n_wins - 1)):
        for row in range(len(game[col]) - (n_wins - 1)):
            color_being_tested = game[col][row]
            if color_being_tested != 0:  # Empty can't win xp
                # start counting consecutive color to 4 to the right and down from this row (slot) to see if 4 wins (rightmost and bottom 3 skipped cause already included)
                for i in range(n_wins):
                    if game[col + i][row + i] == color_being_tested:
                        counter += 1

                if counter == n_wins:
                    winner = color_being_tested
                    print("diagonal descending win")
                else:
                    counter = 0


    # part checking diagonal matches ascending (omiting 3 on top and to the right)
    for col in range(len(game) - (n_wins - 1)):
        for row in range((n_wins-1), len(game[col])): #start is 3 down here ("box" in corner bottom left)
            color_being_tested = game[col][row]
            if color_being_tested != 0:  # Empty can't win xp
                # start counting consecutive color to 4 to the right and up from this row (slot) to see if 4 wins (rightmost and top 3 skipped cause already included)
                for i in range(n_wins):
                    if game[col + i][row - i] == color_being_tested:    # row - i means checking upwards (and to the right) instead of downwards
                        counter += 1

                if counter == n_wins:
                    winner = color_being_tested
                    print("diagonal ascending win")
                else:
                    counter = 0

    # check for draw (if no winner yet, assume draw, disprove by finding empty slot allowing for a win to happen yet)
    if winner == -1: #nobody won?
        winner = 0  #assume draw and try to disprove by finding empty slot
        for col in game:
            for row in col:
                if row == 0:
                    winner = -1    #finding empty slot means: can't be draw yet
    return winner

def left_click():
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]

    col_result = -1
    row_result = -1



    #scan which slot was clicked (and store to result)
    for i in range(len(hitboxes)):
        for j in range(len(hitboxes[i])):
            if x in range(hitboxes[i][j][0], hitboxes[i][j][0]+hitboxes[i][j][2]):
                col_result = i

    for i in range(len(hitboxes)):
        for j in range(len(hitboxes[i])):
            if y in range(hitboxes[i][j][1], hitboxes[i][j][1]+hitboxes[i][j][3]):
                row_result = j

    #place chip at registered spot (if both click x and y / click are on rack)
    if col_result != -1 and row_result != -1:
        place_chip(col_result)
        col_result, row_result = (-1, -1)

    place_chip(random.randrange(game_size[0]))

def stop():
   global running
   running = False


def start():
    while running:

        #check for Events like Keystrokes and Mouse input
        for event in pygame.event.get():
            # Check if window closed
            if event.type == pygame.QUIT:
                stop()
            # Check Key Strokes
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop()

                if event.key == pygame.K_r:
                    reset_game()
                    print("r pressed")
            # Check Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN:
                left_click()

        #
        tick()



