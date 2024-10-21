import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors (RGB)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 125, 0)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jeu du morpion imbattable')

# Fonts
font = pygame.font.SysFont(None, 100)
small_font = pygame.font.SysFont(None, 120)

# Board
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]  # 0: empty, 1: player1, 2: player2 or AI

# Game variables
player = 1
game_over = False
game_mode = None  # None initially, 1 for vs AI, 2 for 2 players
winner = None  # Track the winner, 1: player1, 2: player2/AI, 0: draw

def draw_lines():
    screen.fill(BG_COLOR)
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

def check_win(player, AI=False):
    # Check verticals
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            if not AI:
                draw_vertical_winning_line(col, player)
            return True

    # Check horizontals
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            if not AI:
                draw_horizontal_winning_line(row, player)
            return True

    # Check descending diagonal
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        if not AI:
            draw_desc_diagonal(player)
        return True

    # Check ascending diagonal
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        if not AI:
            draw_asc_diagonal(player)
        return True

    return False

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), LINE_WIDTH)

def draw_asc_diagonal(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), LINE_WIDTH)

def draw_desc_diagonal(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), LINE_WIDTH)

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

# AI (Minimax algorithm)
def minimax(board, depth, is_maximizing):
    if check_win(2, True):
        return 1
    elif check_win(1, True):
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 2
                    score = minimax(board, depth + 1, False)
                    board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax(board, depth + 1, True)
                    board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -math.inf
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        mark_square(best_move[0], best_move[1], 2)

def display_menu():
    screen.fill(BG_COLOR)
    text_vs_ai = small_font.render("Joueur vs IA", True, TEXT_COLOR)
    text_two_player = small_font.render("Joueur vs Joueur", True, TEXT_COLOR)
    screen.blit(text_vs_ai, (WIDTH//2 - text_vs_ai.get_width()//2, HEIGHT//3))
    screen.blit(text_two_player, (WIDTH//2 - text_two_player.get_width()//2, HEIGHT//2))
    pygame.display.update()

def display_winner(winner):
    if winner == 1:
        text = font.render("Le joueur 1 a gagné !" if game_mode == 2 else "T'as triché !", True, TEXT_COLOR)
    elif winner == 2:
        text = font.render("Le joueur 2 a gagné !" if game_mode == 2 else "L'IA a gagné !", True, TEXT_COLOR)
    else:
        text = font.render("Égalité !", True, TEXT_COLOR)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, (HEIGHT - text.get_height())//2))
    pygame.display.update()

# Main game loop
menu_active = True
draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if menu_active:
            display_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if HEIGHT//3 <= mouseY <= HEIGHT//3 + 80:
                    game_mode = 1  # Player vs AI
                    menu_active = False
                    restart()
                elif HEIGHT//2 <= mouseY <= HEIGHT//2 + 80:
                    game_mode = 2  # Two Players
                    menu_active = False
                    restart()

        elif not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        game_over = True
                        winner = player
                    elif is_board_full():
                        game_over = True
                        winner = 0

                    player = 2 if player == 1 else 1

            if game_mode == 1 and player == 2 and not game_over:
                ai_move()
                if check_win(2):
                    game_over = True
                    winner = 2
                elif is_board_full():
                    game_over = True
                    winner = 0
                player = 1

        if game_over:
            draw_figures()
            display_winner(winner)

    if not menu_active and not game_over:
        draw_figures()
    pygame.display.update()
