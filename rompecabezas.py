import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (70, 130, 180)
YELLOW = (255, 223, 0)

# Tamaño de la pantalla y de las piezas
WIDTH, HEIGHT = 400, 400
TILE_SIZE = WIDTH // 3

# Crear la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rompecabezas Deslizante")

# Fuentes
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 30)

# Función para crear el rompecabezas
def create_puzzle():
    puzzle = list(range(1, 9)) + [None]
    random.shuffle(puzzle)
    return puzzle

# Función para dibujar el rompecabezas
def draw_puzzle(puzzle):
    screen.fill(LIGHT_BLUE)
    
    for i in range(3):
        for j in range(3):
            tile = puzzle[i * 3 + j]
            x, y = j * TILE_SIZE, i * TILE_SIZE
            if tile is not None:
                pygame.draw.rect(screen, DARK_BLUE, (x, y, TILE_SIZE, TILE_SIZE), border_radius=10)
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 5, border_radius=10)
                text = font.render(str(tile), True, WHITE)
                text_rect = text.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, GRAY, (x, y, TILE_SIZE, TILE_SIZE), border_radius=10)
                pygame.draw.rect(screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 5, border_radius=10)
    
    # Dibujar el título
    title_text = font.render("Rompecabezas", True, YELLOW)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 40))
    screen.blit(title_text, title_rect)

# Función para mover una pieza
def move_piece(puzzle, direction):
    empty_idx = puzzle.index(None)
    row, col = divmod(empty_idx, 3)

    if direction == 'UP' and row > 0:
        swap_idx = (row - 1) * 3 + col
    elif direction == 'DOWN' and row < 2:
        swap_idx = (row + 1) * 3 + col
    elif direction == 'LEFT' and col > 0:
        swap_idx = row * 3 + (col - 1)
    elif direction == 'RIGHT' and col < 2:
        swap_idx = row * 3 + (col + 1)
    else:
        return puzzle

    puzzle[empty_idx], puzzle[swap_idx] = puzzle[swap_idx], puzzle[empty_idx]
    return puzzle

# Función para verificar si el rompecabezas está resuelto
def check_win(puzzle):
    return puzzle == list(range(1, 9)) + [None]

# Función para dibujar el botón de reinicio
def draw_reset_button():
    button_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 60, 160, 40)
    pygame.draw.rect(screen, YELLOW, button_rect, border_radius=20)
    pygame.draw.rect(screen, BLACK, button_rect, 3, border_radius=20)
    reset_text = small_font.render("Reiniciar", True, BLACK)
    text_rect = reset_text.get_rect(center=button_rect.center)
    screen.blit(reset_text, text_rect)
    return button_rect

# Función principal del juego
def main():
    puzzle = create_puzzle()
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(LIGHT_BLUE)
        draw_puzzle(puzzle)
        
        # Dibujar el botón de reinicio
        reset_button = draw_reset_button()

        # Verificar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    puzzle = move_piece(puzzle, 'UP')
                elif event.key == pygame.K_DOWN:
                    puzzle = move_piece(puzzle, 'DOWN')
                elif event.key == pygame.K_LEFT:
                    puzzle = move_piece(puzzle, 'LEFT')
                elif event.key == pygame.K_RIGHT:
                    puzzle = move_piece(puzzle, 'RIGHT')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if reset_button.collidepoint(event.pos):
                    puzzle = create_puzzle()  # Reiniciar el rompecabezas

        # Verificar si el jugador ha ganado
        if check_win(puzzle):
            win_text = font.render("¡Ganaste!", True, YELLOW)
            win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(win_text, win_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
