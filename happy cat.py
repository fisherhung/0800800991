import pygame# Initialize Pygame
pygame.init()

# Set window size
win_size = (400, 400)
win = pygame.display.set_mode(win_size)
pygame.display.set_caption("Sudoku Solver")

# Define sudoku board
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Define font
font = pygame.font.SysFont(None, 40)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw game screen
    win.fill(WHITE)  # White background
    for i in range(9):
        for j in range(9):
            if sudoku_board[i][j] != 0:
                text = font.render(str(sudoku_board[i][j]), True, BLACK)
                win.blit(text, (j * 40 + 10, i * 40 + 10))
            pygame.draw.rect(win, GRAY, (j * 40, i * 40, 40, 40), 1)  # Draw grid lines
    pygame.display.flip()

# Quit Pygame
pygame.quit()
import sys
import pygame

# 初始化 Pygame
pygame.init()

# 設置視窗大小
win_size = (400, 400)
win = pygame.display.set_mode(win_size)
pygame.display.set_caption("Sudoku Solver")

# 定義數獨盤面
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# 定義顏色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# 定義字體
font = pygame.font.SysFont(None, 40)

# 遊戲循環
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 繪製遊戲畫面
    win.fill(WHITE)  # 白色背景
    for i in range(9):
        for j in range(9):
            if sudoku_board[i][j] != 0:
                text = font.render(str(sudoku_board[i][j]), True, BLACK)
                win.blit(text, (j * 40 + 10, i * 40 + 10))
            pygame.draw.rect(win, GRAY, (j * 40, i * 40, 40, 40), 1)  # 繪製格線

    pygame.display.flip()

# 退出 Pygame
pygame.quit()
sys.exit()
