import pygame
import sys
import numpy as np
import pickle

# Constants
BOARD_SIZE = 3  # Change this for larger boards (e.g., 4, 5, etc.)
CELL_SIZE = 150
WIDTH, HEIGHT = BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE
LINE_WIDTH = 10
CIRCLE_RADIUS = 40
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = 55
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CIRCLE_COLOR = (0, 0, 255)
CROSS_COLOR = (255, 0, 0)

# Minimax Scoring
AI_PLAYER = "O"
HUMAN_PLAYER = "X"

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe AI")
screen.fill(WHITE)

# Draw Grid
def draw_grid():
    for row in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (row * CELL_SIZE, 0), (row * CELL_SIZE, HEIGHT), LINE_WIDTH)

# Draw Symbols (X and O)
def draw_symbol(row, col, player):
    center_x = col * CELL_SIZE + CELL_SIZE // 2
    center_y = row * CELL_SIZE + CELL_SIZE // 2
    if player == "O":
        pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)
    elif player == "X":
        pygame.draw.line(screen, CROSS_COLOR, 
                         (center_x - SPACE, center_y - SPACE), 
                         (center_x + SPACE, center_y + SPACE), CROSS_WIDTH)
        pygame.draw.line(screen, CROSS_COLOR, 
                         (center_x + SPACE, center_y - SPACE), 
                         (center_x - SPACE, center_y + SPACE), CROSS_WIDTH)

# Check Winner
def check_winner(board):
    for row in range(BOARD_SIZE):
        if all(board[row][0] == board[row][col] != " " for col in range(BOARD_SIZE)):
            return board[row][0]

    for col in range(BOARD_SIZE):
        if all(board[0][col] == board[row][col] != " " for row in range(BOARD_SIZE)):
            return board[0][col]

    if all(board[i][i] == board[0][0] != " " for i in range(BOARD_SIZE)):
        return board[0][0]

    if all(board[i][BOARD_SIZE - i - 1] == board[0][BOARD_SIZE - 1] != " " for i in range(BOARD_SIZE)):
        return board[0][BOARD_SIZE - 1]

    if any(" " in row for row in board):
        return None  # Game still ongoing

    return "Draw"  # No moves left

# Minimax Algorithm with Alpha-Beta Pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == AI_PLAYER:
        return 10 - depth
    elif winner == HUMAN_PLAYER:
        return depth - 10
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == " ":
                    board[row][col] = AI_PLAYER
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[row][col] = " "
                    best_score = max(best_score, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float("inf")
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == " ":
                    board[row][col] = HUMAN_PLAYER
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[row][col] = " "
                    best_score = min(best_score, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return best_score

# Get Best AI Move
def get_best_move(board):
    best_move = None
    best_score = -float("inf")

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == " ":
                board[row][col] = AI_PLAYER
                score = minimax(board, 0, False, -float("inf"), float("inf"))
                board[row][col] = " "
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move

# Save Model
def save_minimax():
    model = {"get_best_move": get_best_move}
    with open(f"minimax_ttt_{BOARD_SIZE}x{BOARD_SIZE}.pkl", "wb") as file:
        pickle.dump(model, file)
    print(f"Minimax model for {BOARD_SIZE}x{BOARD_SIZE} saved!")

# Load Model
def load_minimax():
    with open(f"minimax_ttt_{BOARD_SIZE}x{BOARD_SIZE}.pkl", "rb") as file:
        model = pickle.load(file)
    return model["get_best_move"]

# Main Game Loop
def play_game():
    board = [[" " for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = "X"
    running = True

    draw_grid()
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and current_player == HUMAN_PLAYER:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE
                
                if board[row][col] == " ":
                    board[row][col] = HUMAN_PLAYER
                    draw_symbol(row, col, HUMAN_PLAYER)
                    pygame.display.flip()

                    winner = check_winner(board)
                    if winner:
                        print(f"Winner: {winner}")
                        running = False
                        break

                    ai_move = get_best_move(board)
                    if ai_move:
                        board[ai_move[0]][ai_move[1]] = AI_PLAYER
                        draw_symbol(ai_move[0], ai_move[1], AI_PLAYER)
                        pygame.display.flip()

                    winner = check_winner(board)
                    if winner:
                        print(f"Winner: {winner}")
                        running = False

# Start Game
if __name__ == "__main__":
    save_minimax()
    play_game()
