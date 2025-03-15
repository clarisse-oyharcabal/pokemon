import pygame
import math
from .pokemon import Pokemon
from .utils import draw_text
from .game import Game
from .save_manager import SaveManager
from .pokedex import Pokedex
from .sound_manager import SoundManager

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.pokemon_names = Pokemon.get_pokemon_names()
        self.current_index = 0

        # Inicializar el gestor de sonido
        self.sound_manager = SoundManager()
        
        self.background_main_menu = pygame.image.load('assets/images/background_pokemon.jpg')
        self.background_main_menu = pygame.transform.scale(self.background_main_menu, (800, 600))
        self.selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
        self.attack_effect = None
        self.defense_effect = None

        # Chargement des boutons
        self.button_play_image = pygame.image.load('assets/images/button_play.png')
        self.button_load_image = pygame.image.load('assets/images/button_load.png')
        self.button_quit_image = pygame.image.load('assets/images/button_quit.png')
        self.button_pokeball_image = pygame.image.load('assets/images/pokeball.png')
        self.background_pokchoice = pygame.image.load('assets/images/pokchoice_background.jpg')
        self.background_pokchoice = pygame.transform.scale(self.background_pokchoice, (800, 600))
        
        # Chargement des flèches pour le choix de Pokémon
        self.arrow_left_image = pygame.image.load('assets/images/arrow_left.png')
        self.arrow_right_image = pygame.image.load('assets/images/arrow_right.png')
        
        # Chargement du bouton choose_poke
        self.choose_poke_image = pygame.image.load('assets/images/choose_poke.png')

        # Taille originale des boutons et flèches
        self.original_size = (70, 70)
        self.button_play_image = pygame.transform.scale(self.button_play_image, self.original_size)
        self.button_load_image = pygame.transform.scale(self.button_load_image, self.original_size)
        self.button_quit_image = pygame.transform.scale(self.button_quit_image, self.original_size)
        self.button_pokeball_image = pygame.transform.scale(self.button_pokeball_image, self.original_size)
        self.arrow_left_image = pygame.transform.scale(self.arrow_left_image, (50, 50))
        self.arrow_right_image = pygame.transform.scale(self.arrow_right_image, (50, 50))
        self.choose_poke_image = pygame.transform.scale(self.choose_poke_image, (50, 50))

        # Positions des boutons du menu principal
        self.button_play_rect = self.button_play_image.get_rect(topleft=(230, 520))
        self.button_load_rect = self.button_load_image.get_rect(topleft=(370, 520))
        self.button_quit_rect = self.button_quit_image.get_rect(topleft=(500, 520))
        self.button_pokeball_rect = self.button_pokeball_image.get_rect(topleft=(20, 20))

        # Variables pour l'effet pulse
        self.pulse_speed = 0.1  # Vitesse du pulsation pour le menu principal
        self.pulse_speed1 = 0.025  # Vitesse du pulsation pour le fond de launch_game
        self.pulse_amplitude = 0.05  # Amplitude du pulsation pour le menu principal
        self.pulse_amplitude1 = 0.08  # Amplitude du pulsation pour le fond de launch_game
        self.frame = 0  # Compteur d'animation

    def run(self):
        running = True
        clock = pygame.time.Clock()
        pokedex = Pokedex()

        # Reproducir música del menú
        self.sound_manager.play_music('menu')

        while running:
            self.screen.blit(self.background_main_menu, (0, 0))

            # Calcul du facteur de mise à l'échelle pour l'effet pulse
            scale_factor = 1 + math.sin(self.frame * self.pulse_speed) * self.pulse_amplitude

            # Appliquer l'effet pulse sur chaque bouton
            play_scaled = pygame.transform.scale(self.button_play_image, 
                                             (int(self.original_size[0] * scale_factor), 
                                              int(self.original_size[1] * scale_factor)))
            load_scaled = pygame.transform.scale(self.button_load_image, 
                                             (int(self.original_size[0] * scale_factor), 
                                              int(self.original_size[1] * scale_factor)))
            quit_scaled = pygame.transform.scale(self.button_quit_image, 
                                             (int(self.original_size[0] * scale_factor), 
                                              int(self.original_size[1] * scale_factor)))
            pokeball_scaled = pygame.transform.scale(self.button_pokeball_image, 
                                             (int(self.original_size[0] * scale_factor), 
                                              int(self.original_size[1] * scale_factor)))
            

            # Recalculer les positions pour centrer les boutons après mise à l'échelle
            play_rect = play_scaled.get_rect(center=self.button_play_rect.center)
            load_rect = load_scaled.get_rect(center=self.button_load_rect.center)
            quit_rect = quit_scaled.get_rect(center=self.button_quit_rect.center)
            pokeball_rect = pokeball_scaled.get_rect(center=self.button_pokeball_rect.center)

            # Affichage des boutons avec effet pulse
            self.screen.blit(play_scaled, play_rect.topleft)
            self.screen.blit(load_scaled, load_rect.topleft)
            self.screen.blit(quit_scaled, quit_rect.topleft)
            self.screen.blit(pokeball_scaled, pokeball_rect.topleft)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.launch_game()
                    elif event.key == pygame.K_l:
                        self.load_last_battle()
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        self.current_index = (self.current_index - 1) % len(self.pokemon_names)
                    elif event.key == pygame.K_RIGHT:
                        self.current_index = (self.current_index + 1) % len(self.pokemon_names)
                    self.selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
                    self.attack_effect = None
                    self.defense_effect = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.button_play_rect.collidepoint(event.pos):
                            self.launch_game()
                        elif self.button_load_rect.collidepoint(event.pos):
                            self.load_last_battle()
                        elif self.button_quit_rect.collidepoint(event.pos):
                            running = False
                        elif self.button_pokeball_rect.collidepoint(event.pos):
                            self.open_pokedex(pokedex)  # Open Pokedex
                            self.frame = 0 # Reset animation frame

                        self.attack_effect = None
                        self.defense_effect = None

            self.frame += 1  # Incrémentation du compteur d'animation
            clock.tick(60)  # Limite à 60 FPS

    def load_last_battle(self):
        #Carga y reinicia la última batalla guardada
        player_name, opponent_name = SaveManager.load_last_battle()
        if player_name and opponent_name:
            # Crear objetos Pokemon para el jugador y el oponente
            player_pokemon = Pokemon(player_name)
            opponent_pokemon = Pokemon(opponent_name)
            # Iniciar el juego con el oponente guardado
            game = Game(self.screen, player_pokemon, opponent_pokemon)
            game.run()
        else:
            # Si no hay batalla guardada, mostrar mensaje
            draw_text(self.screen, "No hay batallas guardadas", 300, 300)
            pygame.display.flip()
            pygame.time.wait(2000)

    def launch_game(self):
        running = True
        
        # Reproducir música del menú de selección
        self.sound_manager.play_music('menu')

        while running:
            scale_factor = 1 + math.sin(self.frame * self.pulse_speed1) * self.pulse_amplitude1
            scaled_bg = pygame.transform.scale(self.background_pokchoice, (int(800 * scale_factor), int(600 * scale_factor)))
            bg_rect = scaled_bg.get_rect(center=(400, 300))
            self.screen.blit(scaled_bg, bg_rect.topleft)

            draw_text(self.screen, self.selected_pokemon.name.capitalize(), 350, 130)

            if self.selected_pokemon.front_image:  # Cambiado de image a front_image
                scaled_image = pygame.transform.scale(self.selected_pokemon.front_image, (200, 200))
                image_rect = scaled_image.get_rect(center=(400, 250))
                self.screen.blit(scaled_image, image_rect.topleft)
            else:
                image_rect = pygame.Rect(400 - 100, 250 - 100, 200, 200)

            arrow_left_rect = self.arrow_left_image.get_rect(center=(image_rect.left - 50, image_rect.centery))
            self.screen.blit(self.arrow_left_image, arrow_left_rect.topleft)
            arrow_right_rect = self.arrow_right_image.get_rect(center=(image_rect.right + 50, image_rect.centery))
            self.screen.blit(self.arrow_right_image, arrow_right_rect.topleft)

            y_offset = image_rect.bottom - 15
            for stat, value in self.selected_pokemon.stats.items():
                draw_text(self.screen, f"{stat.capitalize()}: {value}", 330, y_offset)
                y_offset += 20

            self.pulse_speed2 = 0.05  # Vitesse du pulsation du bouton
            self.pulse_amplitude2 = 0.1  # Amplitude du pulsation
            # Applique un effet pulse au bouton
            scale_factor_button = 1 + math.sin(self.frame * self.pulse_speed2) * self.pulse_amplitude2
            scaled_button = pygame.transform.scale(self.choose_poke_image, (int(self.choose_poke_image.get_width() * scale_factor_button), int(self.choose_poke_image.get_height() * scale_factor_button)))
            choose_poke_rect = scaled_button.get_rect(center=(400, y_offset + 40))

            self.screen.blit(scaled_button, choose_poke_rect.topleft)


            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_LEFT:
                        self.current_index = (self.current_index - 1) % len(self.pokemon_names)
                    elif event.key == pygame.K_RIGHT:
                        self.current_index = (self.current_index + 1) % len(self.pokemon_names)
                    elif event.key == pygame.K_c:
                        game = Game(self.screen, self.selected_pokemon)
                        game.sound_manager = self.sound_manager  # Pasar el gestor de sonido
                        game.run()
                        running = False

                    self.selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
                    self.attack_effect = None
                    self.defense_effect = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if arrow_left_rect.collidepoint(event.pos):
                            self.current_index = (self.current_index - 1) % len(self.pokemon_names)
                            self.selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
                        elif arrow_right_rect.collidepoint(event.pos):
                            self.current_index = (self.current_index + 1) % len(self.pokemon_names)
                            self.selected_pokemon = Pokemon(self.pokemon_names[self.current_index])
                        elif choose_poke_rect.collidepoint(event.pos):
                            game = Game(self.screen, self.selected_pokemon)
                            game.sound_manager = self.sound_manager  # Pasar el gestor de sonido
                            game.run()
                            running = False

                    self.attack_effect = None
                    self.defense_effect = None

            self.frame += 1

    def open_pokedex(self, pokedex):
        running = True
        
        # Reproducir música de la pokédex
        self.sound_manager.play_music('pokedex')
        page = 0
        items_per_page = 1

        # Recharger directement le Pokédex pour s'assurer que les données sont à jour
        pokedex.pokedex = pokedex._load_pokedex()  # Cette ligne recharge les données à chaque fois
        # Précharger les images et les redimensionner une seule fois
        background = pygame.transform.scale(pygame.image.load('assets/images/yellow_background.jpg'), (800, 600))  # Taille fixe pour optimisation
        history_image = pygame.transform.scale(pygame.image.load('assets/images/History_pokedex1.png'), (400, 500))

        # Police pour le nom du Pokémon (plus grande)
        name_font = pygame.font.Font(None, 35)  # Taille plus grande
        # Police pour les stats (plus petite)
        stat_font = pygame.font.Font(None, 22)

        while running:
            # Effet de pulsation (optimisé)
            scale_factor = 1 + math.sin(self.frame * self.pulse_speed1) * self.pulse_amplitude1
            scaled_bg = pygame.transform.scale(background, (int(800 * scale_factor), int(600 * scale_factor)))  # Utiliser l'image préchargée
            bg_rect = scaled_bg.get_rect(center=(400, 300))
            self.screen.blit(scaled_bg, bg_rect.topleft)

            self.screen.blit(history_image, (200, 80))  # Positionnement direct

            captured_pokemon = pokedex.pokedex
            start_index = page * items_per_page
            end_index = min((page + 1) * items_per_page, len(captured_pokemon))

            if captured_pokemon:
                for i in range(start_index, end_index):
                    pokemon_data = captured_pokemon[i]
                    try:
                        pokemon = Pokemon(pokemon_data["name"])
                        if pokemon.front_image:
                            scaled_image = pygame.transform.scale(pokemon.front_image, (150, 150))
                            image_rect = scaled_image.get_rect(center=(400, 220))
                            self.screen.blit(scaled_image, image_rect)

                            # Nom du Pokémon (plus grand, noir)
                            name_surface = name_font.render(pokemon.name.capitalize(), True, (0, 0, 0))
                            name_rect = name_surface.get_rect(topleft=(260, 425))  # Position au-dessus des stats
                            self.screen.blit(name_surface, name_rect)

                            # Stats du Pokémon (plus petites, noires)
                            y_offset = name_rect.bottom + 20  # Marge sous le nom
                            for stat, value in pokemon.stats.items():
                                stat_surface = stat_font.render(f"{stat.capitalize()}: {value}", True, (0, 0, 0))
                                stat_rect = stat_surface.get_rect(topleft=(250, y_offset))  # Centré horizontalement
                                self.screen.blit(stat_surface, stat_rect)
                                y_offset += 15  # Espacement entre les stats

                        else:
                            print(f"Error: Could not load image for {pokemon_data['name']}")
                    except Exception as e:
                        print(f"Error displaying Pokemon {pokemon_data['name']}: {e}")

            else:
                text_surface = name_font.render("No Pokémon captured yet!", True, (0, 0, 0))  # Utilisation de la police plus grande
                text_rect = text_surface.get_rect(center=(400, 230))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:  # Flèche gauche
                        page = max(0, page - 1)
                    elif event.key == pygame.K_RIGHT:  # Flèche droite
                        if end_index < len(captured_pokemon):
                            page = min(page + 1, (len(captured_pokemon) - 1) // items_per_page)

            self.frame += 1
