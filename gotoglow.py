import pygame, sys, random, os

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana (responsive)
WIDTH, HEIGHT = 480, 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("GoToGlow: Luxury Match")

# Colores (según Brand Book y estrategia de lujo)
COLOR_BG    = (2, 2, 2)         # Fondo sobrio y elegante
COLOR1      = (101, 211, 168)     # Energía
COLOR2      = (95, 104, 189)      # Estilo
COLOR3      = (61, 159, 227)      # Tecnología
COLOR4      = (217, 223, 226)     # Motivación
COLOR5      = (32, 65, 91)        # Exclusividad y lujo

# Variables para piezas del puzzle
candy_colors = [COLOR1, COLOR2, COLOR3, COLOR4]
LOGO_INDEX = 4  # La pieza especial mostrará el logo

# Configuración del tablero
ROWS, COLS = 8, 8
CELL_SIZE = 50

# Estados del juego: "login", "mode_selection", "game", "gameover"
game_state = "login"
selected_mode = None
score = 0
level = 1

# Variables para manejo de selección en el tablero
selected_cell = (0, 0)
first_selected = None

# Variables para la animación del logo en la pantalla de inicio
base_logo_percentage = 0.3  # El logo ocupará el 30% del ancho
logo_scale = 1.0
logo_scale_direction = 1

# Cargar el logo desde la ruta absoluta (usa comillas por los espacios)
logo_path = "/Users/juanmanuelgoenagacastro/Desktop/Logo Blanco GoToGym.png"
if os.path.exists(logo_path):
    try:
        original_logo = pygame.image.load(logo_path).convert_alpha()
    except Exception as e:
        print("Error al cargar el logo:", e)
        original_logo = None
else:
    print("No se encontró el logo en la ruta:", logo_path)
    original_logo = None

# Para usar el logo en el tablero, se escala al tamaño de celda
try:
    logo_image = pygame.transform.scale(original_logo, (CELL_SIZE-10, CELL_SIZE-10)) if original_logo else None
except Exception as e:
    logo_image = None

# Función para crear el tablero con piezas aleatorias (0-3) y ocasionalmente el logo (4)
def create_board():
    board = []
    for _ in range(ROWS):
        board.append([random.randint(0, 4) for _ in range(COLS)])
    return board

board = create_board()

# Función para dibujar el tablero de puzzle (usado en el estado "game")
def draw_board(surface, board, selected_cell=None):
    screen_width, _ = surface.get_size()
    GRID_LEFT = (screen_width - COLS * CELL_SIZE) // 2
    GRID_TOP = 120
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

# Funciones para la mecánica match-3
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

def remove_matches(board, matches):
    global score, level
    for (row, col) in matches:
        board[row][col] = None
        score += 10
    level = score // 100 + 1
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

def swap_cells(board, pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
    return board

def are_adjacent(pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    return abs(r1 - r2) + abs(c1 - c2) == 1

# Pantalla de Login: muestra logo animado y botón "Iniciar Sesión"
def draw_login_screen(surface):
    surface.fill(COLOR_BG)
    screen_width, screen_height = surface.get_size()
    
    # Animación del logo
    global logo_scale, logo_scale_direction
    logo_scale += 0.005 * logo_scale_direction
    if logo_scale > 1.2:
        logo_scale_direction = -1
    elif logo_scale < 0.8:
        logo_scale_direction = 1
    logo_size = int(screen_width * base_logo_percentage * logo_scale)
    if original_logo:
        scaled_logo = pygame.transform.scale(original_logo, (logo_size, logo_size))
        logo_rect = scaled_logo.get_rect(center=(screen_width//2, int(screen_height * 0.3)))
        surface.blit(scaled_logo, logo_rect)
    
    # Mensaje de bienvenida
    font_title = pygame.font.SysFont("Arial", int(screen_width * 0.06))
    title_text = font_title.render("Bienvenido a tu espacio de evolución", True, COLOR1)
    title_rect = title_text.get_rect(center=(screen_width//2, int(screen_height * 0.55)))
    surface.blit(title_text, title_rect)
    
    # Mensaje motivador
    font_sub = pygame.font.SysFont("Arial", int(screen_width * 0.035))
    sub_text = font_sub.render("Combina energía, desbloquea estilo y siente la tecnología premium", True, COLOR3)
    sub_rect = sub_text.get_rect(center=(screen_width//2, int(screen_height * 0.62)))
    surface.blit(sub_text, sub_rect)
    
    # Botón "Iniciar Sesión"
    button_width = int(screen_width * 0.5)
    button_height = int(screen_height * 0.1)
    button_rect = pygame.Rect((screen_width - button_width) // 2,
                                int(screen_height * 0.7),
                                button_width,
                                button_height)
    pygame.draw.rect(surface, COLOR2, button_rect, border_radius=10)
    font_button = pygame.font.SysFont("Arial", int(screen_width * 0.04))
    button_text = font_button.render("Iniciar Sesión", True, COLOR_BG)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    surface.blit(button_text, button_text_rect)
    
    return button_rect

clock = pygame.time.Clock()
running = True
game_state = "login"

# Bucle principal
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            SCREEN = pygame.display.set_mode(event.size, pygame.RESIZABLE)
    
    if game_state == "login":
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                login_button = draw_login_screen(SCREEN)
                if login_button.collidepoint(mouse_pos):
                    # Transición a la siguiente pantalla (por ejemplo, selección de modo)
                    game_state = "mode_selection"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "mode_selection"
        draw_login_screen(SCREEN)
        pygame.display.flip()
    
    # Aquí puedes agregar los estados "mode_selection", "game", "gameover" según necesites.
    
pygame.quit()
sys.exit()

