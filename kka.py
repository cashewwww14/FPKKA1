import pygame
import math
import random
import time

# Initialize constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
VINTAGE_BLUE = (70, 130, 180)  # Muted blue
VINTAGE_BLACK = (34, 34, 34)    # Dark gray
VINTAGE_RED = (139, 0, 0)       # Dark red
VINTAGE_YELLOW = (255, 215, 0)  # Gold
WINDOW_LENGTH = 4

# Initialize Pygame
pygame.init()
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4")

def create_board():
    return [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(WINDOW_LENGTH)):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
            if all(board[r + 3 - i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    return False

def minimax(board, depth, maximizingPlayer):
    valid_locations = [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]
    if winning_move(board, VINTAGE_RED):
        return (None, -1000000)
    elif winning_move(board, VINTAGE_YELLOW):
        return (None, 1000000)
    elif depth == 0 or not valid_locations:
        return (None, 0)

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, row, col, VINTAGE_YELLOW)
            new_score = minimax(temp_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, row, col, VINTAGE_RED)
            new_score = minimax(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
        return best_col, value

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, VINTAGE_BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, VINTAGE_BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == VINTAGE_RED:
                pygame.draw.circle(screen, VINTAGE_RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int((r) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == VINTAGE_YELLOW:
                pygame.draw.circle(screen, VINTAGE_YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int((r) * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def display_message(message):
    font = pygame.font.SysFont("monospace", 75)
    label = font.render(message, 1, (255, 255, 255))
    screen.blit(label, (width // 2 - 200, height // 2 - 50))
    pygame.display.update()
    time.sleep(3)

board = create_board()
draw_board(board)
game_over = False
turn = 0

display_message("Game Start!")

while not game_over:
    if turn == 0:  # Human turn
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, VINTAGE_RED)
                    if winning_move(board, VINTAGE_RED):
                        display_message("Player wins!")
                        game_over = True
                    turn = 1
                    draw_board(board)
    else:  # AI turn
        col, _ = minimax(board, 4, True)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, VINTAGE_YELLOW)
            if winning_move(board, VINTAGE_YELLOW):
                draw_board(board)
                display_message("AI wins!")
                game_over = True
            turn = 0
            draw_board(board)
        time.sleep(0.5)

    if game_over:
        pygame.time.wait(3000)  # Wait before closing
