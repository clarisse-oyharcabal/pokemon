import pygame  # Import the pygame library to use its functionalities for game development.
import os  # Import the os module to handle file paths and directories.

class SoundManager:
    def __init__(self):
        """
        Initializes the SoundManager class, ensuring pygame.mixer is set up correctly
        and preparing paths for the music files.
        """
        # Asegurarse de que pygame.mixer esté inicializado correctamente
        try:
            pygame.mixer.init(44100, -16, 2, 2048)  # Initialize the pygame mixer with the specified settings.
        except pygame.error:
            print("No se pudo inicializar el sistema de audio")  # Error message if the audio system fails to initialize.
        
        self.current_music = None  # Track the current music being played.
        
        # Definir la ruta base para los archivos de música
        self.sound_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sounds")  # Define the base path for the sound files.
        
        # Rutas de los archivos de música
        self.music_files = {
            'menu': os.path.join(self.sound_dir, 'menu.mp3'),  # Path for the 'menu' music file.
            'pokedex': os.path.join(self.sound_dir, 'pokedex.mp3'),  # Path for the 'pokedex' music file.
            'combat': os.path.join(self.sound_dir, 'combat.mp3')  # Path for the 'combat' music file.
        }
        
    def play_music(self, music_type):
        """
        Reproduce la música especificada en loop.
        Plays the specified music in a loop. 
        music_type puede ser: 'menu', 'pokedex', 'combat'
        music_type can be one of: 'menu', 'pokedex', 'combat'.
        """
        if self.current_music != music_type:  # Check if the requested music is different from the currently playing music.
            try:
                pygame.mixer.music.stop()  # Stop the currently playing music.
                music_file = self.music_files.get(music_type)  # Get the file path for the requested music type.
                
                if music_file and os.path.exists(music_file):  # Check if the music file exists.
                    pygame.mixer.music.load(music_file)  # Load the music file.
                    pygame.mixer.music.play(-1)  # Play the music in a loop (-1 means infinite loop).
                    self.current_music = music_type  # Update the current music.
                else:
                    print(f"Archivo de música no encontrado: {music_file}")  # Error message if the file does not exist.
                    
            except pygame.error as e:
                print(f"Error al reproducir la música: {e}")  # Error message if there's an issue with pygame's music system.
                # Intentar cargar un formato alternativo
                try:
                    alt_file = music_file.replace('.mp3', '.wav')  # Attempt to use a .wav version if the .mp3 fails.
                    if os.path.exists(alt_file):  # Check if the alternate file exists.
                        pygame.mixer.music.load(alt_file)  # Load the .wav file.
                        pygame.mixer.music.play(-1)  # Play the .wav file in a loop.
                        self.current_music = music_type  # Update the current music.
                except:
                    print("No se pudo cargar el formato alternativo")  # Error message if the alternate format fails to load.
