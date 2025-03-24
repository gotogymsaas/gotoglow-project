import pygame, sys, random, os

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana (responsive)
WIDTH, HEIGHT = 480, 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("GoToGlow: Luxury Match")

# Colores (según Brand Book)
COLOR_BG    = (2, 2, 2)         # Fondo sobrio
COLOR1      = (101, 211, 168)     # Energía
COLOR2      = (95, 104, 189)      # Estilo
COLOR3      = (61, 159, 227)      # Tecnología
COLOR4      = (217, 223, 226)     # Motivación
COLOR5      = (32, 65, 91)        # Lujo

# Variables para logo
base_logo_percentage = 0.3  # El logo ocupará el 30% del ancho
logo_scale = 1.0
logo_scale_direction = 1

# Ruta absoluta al logo (manejo de espacios con comillas)
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

# Función para dibujar la pantalla de inicio (Login)
def draw_login_screen(surface):
    surface.fill(COLOR_BG)
    screen_width, screen_height = surface.get_size()
    
    # Animación del logo: actualización de escala
    global logo_scale, logo_scale_direction
    logo_scale += 0.005 * logo_scale_direction
    if logo_scale > 1.2:
        logo_scale_direction = -1
    elif logo_scale < 0.8:
        logo_scale_direction = 1
    logo_size = int(screen_width * base_logo_percentage * logo_scale)
    
    # Dibujar el logo en la parte superior, centrado
    if original_logo:
        scaled_logo = pygame.transform.scale(original_logo, (logo_size, logo_size))
        logo_rect = scaled_logo.get_rect(center=(screen_width//2, int(screen_height * 0.3)))
        surface.blit(scaled_logo, logo_rect)
    
    # Título: mensaje de bienvenida
    font_title = pygame.font.SysFont("Arial", int(screen_width * 0.06))
    title_text = font_title.render("Bienvenido a tu espacio de evolución", True, COLOR1)
    title_rect = title_text.get_rect(center=(screen_width//2, int(screen_height * 0.55)))
    surface.blit(title_text, title_rect)
    
    # Subtítulo: mensaje motivador
    font_sub = pygame.font.SysFont("Arial", int(screen_width * 0.035))
    sub_text = font_sub.render("Combina energía, desbloquea estilo y siente la tecnología premium", True, COLOR3)
    sub_rect = sub_text.get_rect(center=(screen_width//2, int(screen_height * 0.62)))
    surface.blit(sub_text, sub_rect)
    
    # Botón "Iniciar Sesión" con efecto de borde redondeado y color de acento
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
game_state = "login"  # Estado inicial

# Bucle principal
running = True
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
                    game_state = "mode_selection"  # Transición a selección de modo
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "mode_selection"
        draw_login_screen(SCREEN)
        pygame.display.flip()
    
    # Se pueden agregar más estados (mode_selection, game, gameover) aquí...
    
pygame.quit()
sys.exit()

