import pygame  # Import the pygame library to use its functionalities for game development.
from src.menu import MainMenu  # Import the MainMenu class from the src.menu module to handle the main menu of the game.

def main():
    """
    This is the main function that initializes the game, creates the game window, and starts the main menu.
    """
    pygame.init()  # Initialize all pygame modules required for the game.

    # Set up the game window with a resolution of 800x600 pixels.
    screen = pygame.display.set_mode((800, 600))

    # Set the caption (title) of the game window.
    pygame.display.set_caption("Pokémon Game")

    # Create an instance of the MainMenu class and pass the screen object to it to render the menu.
    main_menu = MainMenu(screen)

    # Run the main menu loop, where the user interacts with the menu options.
    main_menu.run()

# Check if the script is run directly (not imported as a module).
if __name__ == "__main__":
    main()  # Call the main function to start the game.
