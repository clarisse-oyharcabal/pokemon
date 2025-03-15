import pygame  # Import the pygame library to use its functionalities for game development.

def draw_text(screen, text, x, y, font_size=25, color=(255,255,255)):
    """
    Dibuja texto en la pantalla con el color especificado.
    This function draws text on the screen at a specified position with a given font size and color.
    
    :param screen: superficie de pygame donde dibujar. The pygame surface (screen) where the text will be drawn.
    :param text: texto a dibujar. The text to be drawn on the screen.
    :param x: posición x. The x-coordinate where the text will appear.
    :param y: posición y. The y-coordinate where the text will appear.
    :param font_size: tamaño de la fuente (default: 30). The size of the font. Default is 25.
    :param color: color del texto en formato RGB (default: blanco). The color of the text in RGB format. Default is white.
    """
    font = pygame.font.Font('assets/fonts/Consolab.ttf', font_size - 10)  # Load the font from a file and set the font size.
    text_surface = font.render(text, True, color)  # Render the text as a surface with the specified color.
    screen.blit(text_surface, (x, y))  # Draw the text on the screen at the specified (x, y) position.
