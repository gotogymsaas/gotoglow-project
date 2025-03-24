import pygame, sys, random

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 480, 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GoToGlow: Luxury Match")

# Definición de colores basados en la paleta de la marca GoToGym
COLOR_BG    = (2, 2, 2)         # Fondo elegante y sobrio
COLOR1      = (101, 211, 168)     # Energía
COLOR2      = (95, 104, 189)      # Estilo y sofisticación
COLOR3      = (61, 159, 227)      # Tecnología
COLOR4      = (217, 223, 226)     # Motivación
COLOR5      = (32, 65, 91)        # Toque de lujo

# Lista de colores para las piezas normales (índices 0 a 3)
candy_colors = [COLOR1, COLOR2, COLOR3, COLOR4]
LOGO_INDEX = 4  # Índice especial para la pieza del logo

# Configuración de la cuadrícula (8x8)
ROWS, COLS = 8, 8
CELL_SIZE = 50
GRID_TOP  = 120  # Espacio superior para el marcador y nivel
GRID_LEFT = (WIDTH - COLS * CELL_SIZE) // 2

# Variables globales del juego
score = 0
level = 1
game_state = "start"  # Estados: "start", "game", "gameover"
selected_cell = None

# Variables para la animación del logo en la pantalla de inicio
start_logo_base_size = 150
logo_scale = 1.0
logo_scale_direction = 1  # 1 para aumentar, -1 para disminuir

# Cargar imagen del logo (coloca "gotogym_logo.png" en el mismo directorio)
try:
    original_logo = pygame.image.load("gotogym_logo.png")
except Exception as e:
    print("Error al cargar el logo:", e)
    original_logo = None

# Versión escalada para la pieza especial en el juego (usada en el tablero)
try:
    logo_image = pygame.transform.scale(original_logo, (CELL_SIZE-10, CELL_SIZE-10)) if original_logo else None
except Exception as e:
    logo_image = None

# Función para crear el tablero: piezas normales (0-3) y el logo (4) con probabilidad aleatoria
def create_board():
    board = []
    for row in range(ROWS):
        board.append([random.randint(0, 4) for _ in range(COLS)])
    return board

board = create_board()

# Función para dibujar el tablero y las piezas
def draw_board(surface, board, selected_cell=None):
    for row in range(ROWS):
        for col in range(COLS):
            x = GRID_LEFT + col * CELL_SIZE
            y = GRID_TOP + row * CELL_SIZE
            pygame.draw.rect(surface, (50, 50, 50), (x, y, CELL_SIZE, CELL_SIZE))
            candy = board[row][col]
            if candy is not None:
                if candy == LOGO_INDEX and logo_image:
                    surface.blit(logo_image, (x+5, y+5))
                else:
                    color = candy_colors[candy] if candy < len(candy_colors) else COLOR5
                    center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                    radius = CELL_SIZE // 2 - 5
                    pygame.draw.circle(surface, color, center, radius)
            if selected_cell == (row, col):
                pygame.draw.rect(surface, (255, 255, 0), (x, y, CELL_SIZE, CELL_SIZE), 3)

# Función para detectar coincidencias horizontales y verticales
def find_matches(board):
    matches = set()
    # Coincidencias horizontales
    for row in range(ROWS):
        count = 1
        for col in range(1, COLS):
            if board[row][col] == board[row][col-1]:
                count += 1
            else:
                if count >= 3:
                    for c in range(col - count, col):
                        matches.add((row, c))
                count = 1
        if count >= 3:
            for c in range(COLS - count, COLS):
                matches.add((row, c))
    # Coincidencias verticales
    for col in range(COLS):
        count = 1
        for row in range(1, ROWS):
            if board[row][col] == board[row-1][col]:
                count += 1
            else:
                if count >= 3:
                    for r in range(row - count, row):
                        matches.add((r, col))
                count = 1
        if count >= 3:
            for r in range(ROWS - count, ROWS):
                matches.add((r, col))
    return matches

# Función para eliminar coincidencias y actualizar el tablero
def remove_matches(board, matches):
    global score, level
    for (row, col) in matches:
        board[row][col] = None
        score += 10
    level = score // 100 + 1  # Actualizar nivel cada 100 puntos
    for col in range(COLS):
        empty_rows = []
        for row in range(ROWS-1, -1, -1):
            if board[row][col] is None:
                empty_rows.append(row)
            elif empty_rows:
                empty_row = empty_rows.pop(0)
                board[empty_row][col] = board[row][col]
                board[row][col] = None
                empty_rows.append(row)
        for row in range(ROWS):
            if board[row][col] is None:
                board[row][col] = random.randint(0, 4)
    return board

# Función para intercambiar dos celdas
def swap_cells(board, pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
    return board

# Función para verificar si dos celdas son adyacentes
def are_adjacent(pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    return abs(r1 - r2) + abs(c1 - c2) == 1

clock = pygame.time.Clock()

# Bucle principal del juego
running = True
while running:
    clock.tick(60)
    
    # PANTALLA DE INICIO con animación del logo
    if game_state == "start":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "game"
        
        # Actualizar la escala del logo para el efecto pulsante
        logo_scale += 0.005 * logo_scale_direction
        if logo_scale > 1.2:
            logo_scale_direction = -1
        elif logo_scale < 0.8:
            logo_scale_direction = 1
        
        SCREEN.fill(COLOR_BG)
        font = pygame.font.SysFont("Arial", 32)
        title_text = font.render("GoToGlow: Luxury Match", True, COLOR1)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        font_small = pygame.font.SysFont("Arial", 20)
        description = font_small.render("Desbloquea tu mejor versión combinando energía, estilo y tecnología", True, COLOR3)
        desc_rect = description.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
        prompt = font_small.render("Presiona SPACE para comenzar", True, COLOR4)
        prompt_rect = prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        
        # Animación del logo pulsante
        if original_logo:
            current_size = int(start_logo_base_size * logo_scale)
            scaled_logo = pygame.transform.scale(original_logo, (current_size, current_size))
            logo_rect = scaled_logo.get_rect(center=(WIDTH // 2, HEIGHT // 2 - current_size))
            SCREEN.blit(scaled_logo, logo_rect)
        
        SCREEN.blit(title_text, title_rect)
        SCREEN.blit(description, desc_rect)
        SCREEN.blit(prompt, prompt_rect)
        pygame.display.flip()
    
    # PANTALLA DE JUEGO
    elif game_state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if GRID_LEFT <= mx < GRID_LEFT + COLS * CELL_SIZE and GRID_TOP <= my < GRID_TOP + ROWS * CELL_SIZE:
                    col = (mx - GRID_LEFT) // CELL_SIZE
                    row = (my - GRID_TOP) // CELL_SIZE
                    if selected_cell is None:
                        selected_cell = (row, col)
                    else:
                        if are_adjacent(selected_cell, (row, col)):
                            board = swap_cells(board, selected_cell, (row, col))
                            matches = find_matches(board)
                            if matches:
                                board = remove_matches(board, matches)
                            else:
                                board = swap_cells(board, selected_cell, (row, col))
                            selected_cell = None
                        else:
                            selected_cell = (row, col)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "gameover"
        matches = find_matches(board)
        if matches:
            pygame.time.delay(150)
            board = remove_matches(board, matches)
        SCREEN.fill(COLOR_BG)
        draw_board(SCREEN, board, selected_cell)
        font = pygame.font.SysFont("Arial", 20)
        score_text = font.render(f"Puntuación: {score}", True, COLOR4)
        SCREEN.blit(score_text, (10, 10))
        level_text = font.render(f"Nivel: {level}", True, COLOR1)
        SCREEN.blit(level_text, (WIDTH - 100, 10))
        inspire_text = font.render("Entrena cuerpo, mente y estilo", True, COLOR3)
        SCREEN.blit(inspire_text, (WIDTH//2 - inspire_text.get_width()//2, 40))
        pygame.display.flip()
    
    # PANTALLA FINAL
    elif game_state == "gameover":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = create_board()
                    score = 0
                    level = 1
                    game_state = "start"
                elif event.key == pygame.K_q:
                    running = False
        SCREEN.fill(COLOR_BG)
        font = pygame.font.SysFont("Arial", 32)
        final_text = font.render("¡Gracias por jugar!", True, COLOR2)
        final_rect = final_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
        SCREEN.blit(final_text, final_rect)
        font_small = pygame.font.SysFont("Arial", 20)
        restart_text = font_small.render("Presiona R para reiniciar o Q para salir", True, COLOR3)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
        SCREEN.blit(restart_text, restart_rect)
        pygame.display.flip()

pygame.quit()
sys.exit()

