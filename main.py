# import modules
import pygame
from pygame.locals import *
import button #only for Menu

pygame.init()

screen_height = 700
screen_width = 700
line_width = 4
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tiger Game')
win_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
win_surface.fill((0, 0, 0, 130))
# define colours in RGB
black = (0, 0, 0)
white = (255, 255, 255)
placeholder_color = (200, 200, 200)

# define font
font = pygame.font.SysFont(None, 40)

# define variables
turn = "Goats"
game_over = False
winner = ""
game_start = False
tigers_cornered = 0
goats_captured = 0
goats_outside = 20

# Load images
tiger_img = pygame.image.load('Images/tiger.png').convert_alpha()
goat_img = pygame.image.load('Images/goat.png').convert_alpha()
quit_img = pygame.image.load('Images/Quit.png').convert_alpha()
start_img = pygame.image.load('Images/Start.png').convert_alpha()
tiger_win_img = pygame.image.load('Images/Tiger_win.png').convert_alpha()
goat_win_img = pygame.image.load('Images/Goat_win.png').convert_alpha()
play_again_img = pygame.image.load('Images/Play_Again.png').convert_alpha()
forest_img = pygame.image.load('Images/forest.png').convert_alpha()
wood_img = pygame.image.load('Images/wood.png').convert_alpha()

# Scale images to fit the board
tiger_img = pygame.transform.scale(tiger_img, (50, 50))
goat_img = pygame.transform.scale(goat_img, (60, 60))
bg_image = pygame.transform.scale(forest_img, (screen_width, screen_height))
bg_image_game = pygame.transform.scale(wood_img, (screen_width, screen_height))

# buttons
start_button = button.Button(200, 200, start_img, 0.5)
quit_button = button.Button(200, 400, quit_img, 0.5)
tiger_win_button = button.Button(100, 200, tiger_win_img, 0.5)
goat_win_button = button.Button(100, 200, goat_win_img, 0.5)
play_again_button = button.Button(100, 300, play_again_img, 0.5)

tiger_pos = [(0, 0), (0, 4), (4, 0), (4, 4)]
goats = [] #lists the position of goats

# only valid moves for each position
moves = {
    (0, 0): [(0, 1), (1, 0), (1, 1)], 
    (0, 1): [(0, 0), (1, 1), (0, 2)], 
    (0, 2): [(0, 1), (1, 1), (1, 2), (1, 3), (0, 3)],
    (0, 3): [(0, 2), (1, 3), (0, 4)], 
    (0, 4): [(0, 3), (1, 3), (1, 4)], 
    (1, 0): [(0, 0), (1, 1), (2, 0)],
    (1, 1): [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
    (1, 2): [(0, 2), (1, 1), (1, 3), (2, 2)],
    (1, 3): [(0, 2), (0, 3), (0, 4), (1, 2), (1, 4), (2, 2), (2, 3), (2, 4)],
    (1, 4): [(0, 4), (1, 3), (2, 4)],
    (2, 0): [(1, 0), (1, 1), (2, 1), (3, 0), (3, 1)],
    (2, 1): [(2, 0), (1, 1), (2, 2), (3, 1)],
    (2, 2): [(1, 1), (1, 2), (1, 3), (2, 1), (3, 1), (3, 2), (2, 3), (3, 3)],
    (2, 3): [(2, 2), (1, 3), (2, 4), (3, 3)],
    (2, 4): [(1, 3), (2, 3), (1, 4), (3, 3), (3, 4)],
    (3, 0): [(2, 0), (3, 1), (4, 0)],
    (3, 1): [(2, 0), (3, 0), (2, 1), (2, 2), (3, 2), (4, 0), (4, 1), (4, 2)],
    (3, 2): [(2, 2), (3, 1), (4, 2), (3, 3)],
    (3, 3): [(2, 2), (3, 2), (2, 3), (2, 4), (3, 4), (4, 2), (4, 3), (4, 4)],
    (3, 4): [(3, 3), (2, 4), (4, 4)],
    (4, 0): [(3, 0), (3, 1), (4, 1)],
    (4, 1): [(4, 0), (3, 1), (4, 2)],
    (4, 2): [(4, 1), (3, 1), (3, 2), (3, 3), (4, 3)],
    (4, 3): [(4, 2), (4, 4), (3, 3)],
    (4, 4): [(4, 3), (3, 3), (3, 4)]
}
# only valid jumps for each position
jumps = {
    (0, 0): [(0, 2), (2, 0), (2, 2)],
    (0, 1): [(0, 3), (2, 1)],
    (0, 2): [(0, 0), (0, 4), (2, 0), (2, 2), (2, 4)],
    (0, 3): [(0, 1), (2, 3)],
    (0, 4): [(0, 2), (2, 2), (2, 4)],
    (1, 0): [(3, 0), (1, 2)],
    (1, 1): [(3, 1), (1, 3),(3, 3)],
    (1, 2): [(1, 0), (1, 4),(3, 2)],
    (1, 3): [(1, 1), (3, 1), (3, 3)],
    (1, 4): [(1, 2), (3, 4)],
    (2, 0): [(0, 0), (0, 2), (2, 2), (4, 0), (4, 2)],
    (2, 1): [(0, 1), (4, 1), (2, 3)],
    (2, 2): [(0, 0), (0, 2), (0, 4), (2, 0), (2, 4), (4, 0), (4, 2), (4, 4)],
    (2, 3): [(0, 3), (2, 1), (4, 3)],
    (2, 4): [(0, 2), (0, 4), (4, 2), (2, 2), (4, 4)],
    (3, 0): [(1, 0), (3, 2)],
    (3, 1): [(1, 1), (1, 3), (3, 3)],
    (3, 2): [(1, 2), (3, 0), (3, 4)],
    (3, 3): [(1, 1), (3, 1), (1, 3)],
    (3, 4): [(3, 2), (1, 4)],
    (4, 0): [(2, 0), (2, 2), (4, 2)],
    (4, 1): [(2, 1), (4, 3)],
    (4, 2): [(2, 0), (2, 2), (2, 4), (4, 0), (4, 4)],
    (4, 3): [(4, 1), (2, 3)],
    (4, 4): [(2, 2), (2, 4), (4, 2)]
}
# Initial board setup
board = [['' for _ in range(5)] for _ in range(5)]
for pos in tiger_pos:
    board[pos[0]][pos[1]] = 'T'

placeholders = []  # Store the positions of the placeholders

def draw_board():
    color = (50, 50, 50)
    spacing = 120
    screen.blit(bg_image_game, (0, 0)) # bg = 'burlywood4'  # screen.fill(bg)
    for x in range(1, 6):
        # rows and columns
        pygame.draw.line(screen, color, (spacing, spacing * x),
                         (screen_width-100, spacing * x), line_width)
        pygame.draw.line(screen, color, (spacing * x, spacing),
                         (spacing * x, screen_height-100), line_width)
    # diagonal lines
    pygame.draw.line(screen, color, (spacing, spacing),
                     (screen_height-100, spacing * 5), line_width)
    pygame.draw.line(screen, color, (spacing, spacing*5),
                     (screen_width-100, spacing), line_width)

    # secondary diagonal lines
    pygame.draw.line(screen, color, (spacing, spacing * 3),
                     (spacing * 3, spacing), line_width)
    pygame.draw.line(screen, color, (spacing * 3, screen_height - 100),
                     (screen_width - 100, spacing * 3), line_width)
    pygame.draw.line(screen, color, (spacing * 3, spacing),
                     (screen_height - 100, spacing * 3), line_width)
    pygame.draw.line(screen, color, (spacing, spacing * 3),
                     (spacing * 3, screen_height - 100), line_width)

    # Draw the placeholders and store their positions
    placeholders.clear()
    for row in range(5):
        for col in range(5):
            center_x = spacing * col + spacing
            center_y = spacing * row + spacing
            pygame.draw.circle(screen, placeholder_color,
                               (center_x, center_y), 15)
            placeholders.append((center_x, center_y, row, col))

    # Draw the tigers and goats on the board
    for row in range(5):
        for col in range(5):
            if board[row][col] == 'T':
                screen.blit(tiger_img, (spacing * col + spacing -
                            23, spacing * row + spacing - 24))
            elif board[row][col] == 'G':
                screen.blit(goat_img, (spacing * col + spacing -
                            30, spacing * row + spacing - 28))

    # Draw the turn text
    turn_text = font.render(f'{turn} Turn!', True, black)
    screen.blit(turn_text, (300, 50))


def draw_stats(tigers_cornered, goats_captured, goats_outside):
    font = pygame.font.SysFont(None, 25)
    # Render the text
    tigers_text = font.render(
        f'TIGERS CORNERED: {tigers_cornered}/4', True, black)
    goats_text = font.render(
        f'GOATS CAPTURED: {goats_captured}/20', True, black)
    outside_text = font.render(
        f'GOATS OUTSIDE: {goats_outside}/20', True, black)

    # Display the text on the screen
    screen.blit(tigers_text, (250, screen_height - 80))
    screen.blit(goats_text, (250, screen_height - 50))
    screen.blit(outside_text, (250, screen_height - 20))


def is_valid_move(start, end):
    x1, y1 = start
    x2, y2 = end
    if not (0 <= x2 < 5 and 0 <= y2 < 5):
        return False  # Out of bounds
    if board[x2][y2] != '':
        return False  # Not an empty spot
    if (x2, y2) in moves[(x1, y1)]:
        return True  # Adjacent move
    return False


def is_valid_jump(start, end):
    x1, y1 = start
    x2, y2 = end
    if not (0 <= x2 < 5 and 0 <= y2 < 5):
        return False  # Out of bounds
    if board[x2][y2] != '':
        return False  # Not an empty spot
    mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
    if board[mid_x][mid_y] != 'G':
        return False  # No goat to jump over
    # if (abs(x1 - x2) == 2 and abs(y1 - y2) == 2) or (abs(x1 - x2) == 2 and abs(y1 - y2) == 0) or (abs(x1 - x2) == 0 and abs(y1 - y2) == 2):
    if (x2, y2) in jumps[(x1, y1)]:
        return True  # Valid jump
    return False


def move_tiger(start, end):
    global goats_captured, game_over, winner
    ismove = is_valid_move(start, end)
    isjump = is_valid_jump(start, end)
    if ismove or isjump:
        x1, y1 = start
        x2, y2 = end
        board[x1][y1] = ''
        board[x2][y2] = 'T'
        tiger_pos.remove((x1, y1))
        tiger_pos.append((x2, y2))
        if not ismove:
            if isjump:
                mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                board[mid_x][mid_y] = ''  # Remove jumped goat
                goats.remove((mid_x, mid_y))
                goats_captured += 1
                if goats_captured == 6:
                    game_over = True
                    winner = 'Tigers'
        return True
    return False


def move_goat(start, end):
    if is_valid_move(start, end):
        x1, y1 = start
        x2, y2 = end
        board[x1][y1] = ''
        board[x2][y2] = 'G'
        goats.append((x2, y2))
        goats.remove((x1, y1))
        return True
    return False


def place_goat(position):
    global goats_outside
    x, y = position
    if board[x][y] == '':
        board[x][y] = 'G'
        goats.append((x, y))
        goats_outside -= 1
        return True
    return False


def is_trap_tiger():
    global tigers_cornered, game_over, winner
    tigers_cornered = 0
    for pos in tiger_pos:
        for move in moves[pos] + jumps[pos]:
            if board[move[0]][move[1]] == '':
                break
        else: # if all moves are blocked(if break is not executed)
            tigers_cornered += 1
    if tigers_cornered == 4:
        game_over = True
        winner = 'Goats'
        return True
    return False    
    
# main loop
run = True
click_pos = []

while run:
    # Draw board

    if not game_start:
        # screen.fill((255, 255, 255))
        screen.blit(bg_image, (0, 0))
        start_button.draw(screen)
        quit_button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if start_button.draw(screen):
                game_start = True
            if quit_button.draw(screen):
                run = False
        pygame.display.update()
        continue
    draw_board()

    draw_stats(tigers_cornered, goats_captured, goats_outside)
    if game_over:
        if winner == 'Tigers':
            tiger_win_button.draw(win_surface)
            screen.blit(win_surface, (0, 0))
        elif winner == 'Goats':
            goat_win_button.draw(win_surface)
            screen.blit(win_surface, (0, 0))
            
        play_again_button.draw(win_surface)
        quit_button.draw(win_surface)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if quit_button.draw(screen):
                run = False
            if play_again_button.draw(screen):
                game_over = False
                winner = 0
                game_start = True
                tigers_cornered = 0
                goats_captured = 0
                goats_outside = 20
                turn = "Goats"
                tiger_pos = [(0, 0), (0, 4), (4, 0), (4, 4)]
                goats = []
                board = [['' for _ in range(5)] for _ in range(5)]
                for pos in tiger_pos:
                    board[pos[0]][pos[1]] = 'T'
        pygame.display.update()
        continue
    # Handle events
    for event in pygame.event.get():
        # Handle game exit
        if event.type == pygame.QUIT:
            run = False
        if not game_over:
            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for center_x, center_y, row, col in placeholders:
                    if (mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2 <= 15 ** 2:
                        # Clicked inside a placeholder circle
                        if turn == 'Goats':
                            if board[row][col] == '' and goats_outside > 0:
                                if place_goat((row, col)):
                                    turn = 'Tigers'
                            elif goats_outside == 0:
                                if len(click_pos) == 0 and board[row][col] == 'G':
                                    click_pos.append((row, col))
                                elif len(click_pos) == 1 and board[row][col] == '':
                                    click_pos.append((row, col))
                                    if move_goat(*click_pos):
                                        click_pos.clear()
                                        turn = 'Tigers'
                                    else:
                                        click_pos.pop()
                                elif len(click_pos) == 1 and board[row][col] == 'G':
                                    click_pos.clear()
                                    click_pos.append((row, col))
                                else:
                                    click_pos.clear()
                            is_trap_tiger()


                        elif turn == 'Tigers':
                            if len(click_pos) == 0 and board[row][col] == 'T':
                                click_pos.append((row, col))
                            elif len(click_pos) == 1 and board[row][col] == '':
                                click_pos.append((row, col))
                                if move_tiger(*click_pos):
                                    click_pos.clear()
                                    turn = 'Goats'
                                else:
                                    click_pos.pop()
                            elif len(click_pos) == 1 and board[row][col] == 'T':
                                click_pos.clear()
                                click_pos.append((row, col))
                            else:
                                click_pos.clear()

    pygame.display.update()

pygame.quit()
