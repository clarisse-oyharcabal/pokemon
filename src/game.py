import pygame
import random
import math
import requests
from .pokemon import Pokemon
from .utils import draw_text
from .combat import Combat
from .combat import Attack
from .save_manager import SaveManager
from .pokedex import Pokedex
from pygame.locals import *

class Game:
    def __init__(self, screen, player_pokemon, opponent_pokemon=None):
        self.screen = screen
        self.player_pokemon = player_pokemon
        # Si se proporciona un oponente específico, usarlo, sino elegir uno aleatorio
        self.opponent_pokemon = opponent_pokemon if opponent_pokemon else self.get_random_pokemon(player_pokemon.name)
        self.background = pygame.image.load("assets/images/battle_pokemon.jpg")
        self.sound_manager = None  # Será establecido por el menú principal
        self.background = pygame.transform.scale(self.background, (800, 600))

        # Agrandissement des sprites
        self.scale_factor = 2

        # Escalar la imagen frontal y trasera del Pokémon del jugador
        if self.player_pokemon.front_image:
           self.player_pokemon.front_image = pygame.transform.scale(
                self.player_pokemon.front_image,
                (self.player_pokemon.front_image.get_width() * self.scale_factor,
                 self.player_pokemon.front_image.get_height() * self.scale_factor))
        if self.player_pokemon.back_image:
            self.player_pokemon.back_image = pygame.transform.scale(
                self.player_pokemon.back_image,
                (self.player_pokemon.back_image.get_width() * self.scale_factor,
                 self.player_pokemon.back_image.get_height() * self.scale_factor))

        # Escalar la imagen del oponente (solo necesitamos la frontal)
        if self.opponent_pokemon.front_image:
            self.opponent_pokemon.front_image = pygame.transform.scale(
                self.opponent_pokemon.front_image,
                (self.opponent_pokemon.front_image.get_width() * self.scale_factor,
                self.opponent_pokemon.front_image.get_height() * self.scale_factor))

        self.time = 0
        self.amplitude = 10
        self.speed = 0.05
        self.combat = Combat(self.player_pokemon, self.opponent_pokemon)
        self.turn = self.player_pokemon if self.player_pokemon.stats["speed"] > self.opponent_pokemon.stats["speed"] else self.opponent_pokemon
        self.game_over = False
        
        # Inicializar el log de mensajes
        self.message_log = []
        self.max_messages = 5

        # Ajout des attaques possibles
        self.player_moves = [
            Attack("Charge", "normal", 40, 35),
            Attack("Ember", "fire", 40, 25),
            Attack("Water Gun", "water", 40, 25),
            Attack("Scratch", "normal", 50, 30)
        ]

        # Guardar la batalla actual
        SaveManager.save_battle(self.player_pokemon, self.opponent_pokemon)

    def get_random_pokemon(self, excluded_pokemon_name):
        """Récupère un Pokémon aléatoire parmi les 150 premiers de la PokéAPI, en excluant le Pokémon choisi."""
        
        api_url = "https://pokeapi.co/api/v2/pokemon?limit=150"
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Vérifie que la requête s'est bien passée
            data = response.json()
            
            # Liste des noms de Pokémon
            pokemon_list = [p["name"] for p in data["results"]]
            
            # Exclure le Pokémon choisi par le joueur
            pokemon_list = [p for p in pokemon_list if p.lower() != excluded_pokemon_name.lower()]
            
            # Sélection aléatoire d'un Pokémon
            if pokemon_list:
                random_pokemon_name = random.choice(pokemon_list)
                return Pokemon(random_pokemon_name)
            
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des Pokémon : {e}")
                
    # Si une erreur se produit, ou si la liste est vide, on choisit un Pokémon par défaut
        return Pokemon("pikachu")

    def add_message(self, message):
        """Añade un mensaje al log"""
        self.message_log.append(message)
        if len(self.message_log) > self.max_messages:
            self.message_log.pop(0)

    def display_message_log(self):
        """Muestra los mensajes del log"""
        y_start = 40
        total_messages = len(self.message_log)
        
        for i, message in enumerate(self.message_log):
            # Determinar el color basado en el contenido del mensaje
            if self.player_pokemon.name.lower() in message.lower():
                color = (20, 20, 254)  # Verde para mensajes del jugador
            elif self.opponent_pokemon.name.lower() in message.lower():
                color = (254, 20, 20)  # Rojo para mensajes del oponente
            else:
                # Para mensajes genéricos como "Critical hit!" o "It's super effective!"
                # Usar el color del último pokémon que atacó
                last_attacker = self.player_pokemon.name if self.turn == self.opponent_pokemon else self.opponent_pokemon.name
                color = (0, 255, 0) if last_attacker == self.player_pokemon.name else (255, 0, 0)

            draw_text(self.screen, message, 42, y_start + (i * 30), color=color)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        # Reproducir música de combate
        if self.sound_manager:
            self.sound_manager.play_music('combat')

        while running:
            self.screen.blit(self.background, (0, 0))

            self.time += self.speed
            oscillation = math.sin(self.time) * self.amplitude

            player_x, player_y = 60 + oscillation, 340 - oscillation
            opponent_x, opponent_y = 535 - oscillation, 100 + oscillation

            # Actualizar las posiciones de los Pokémon para los efectos
            self.player_pokemon.position = [player_x, player_y]
            self.opponent_pokemon.position = [opponent_x, opponent_y]

            # Actualizar los efectos visuales
            self.combat.update_effects()

            # Dessiner les Pokémon avec leurs effets visuels
            self.player_pokemon.draw(self.screen, player_x, player_y, is_player=True)
            self.opponent_pokemon.draw(self.screen, opponent_x, opponent_y, is_player=False)

            # Dibujar los efectos visuales
            self.combat.draw_effects(self.screen)

            draw_text(self.screen, f"Your Pokémon: {self.player_pokemon.name.capitalize()}", 60, 540, 30)
            draw_text(self.screen, f"HP: {self.player_pokemon.stats['hp']}", 85, 565, 30)     # Affichage des points de vie

            draw_text(self.screen, f"Opponent: {self.opponent_pokemon.name.capitalize()}", 545, 300, 30)
            draw_text(self.screen, f"HP: {self.opponent_pokemon.stats['hp']}", 570, 325, 30)    # Affichage des points de vie



            if not self.game_over:
                if self.turn == self.player_pokemon:
                    self.display_attack_options()
                else:
                    self.opponent_attack()
                    self.turn = self.player_pokemon

            # Mostrar el log de mensajes
            self.display_message_log()

            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.turn == self.player_pokemon:
                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                            attack_index = event.key - pygame.K_1
                            if 0 <= attack_index < len(self.player_moves):
                                self.player_attack(self.player_moves[attack_index])
                                self.turn = self.opponent_pokemon

            if self.player_pokemon.stats["hp"] <= 0 or self.opponent_pokemon.stats["hp"] <= 0:
                self.game_over = True

                # Déterminer le gagnant
                if self.opponent_pokemon.stats["hp"] <= 0:
                    winner = self.player_pokemon.name
                else:
                    winner = self.opponent_pokemon.name

                # Si le joueur gagne, ajouter le Pokémon vaincu au Pokédex
                if winner == self.player_pokemon.name:
                    from .pokedex import Pokedex  # Import du Pokédex
                    pokedex = Pokedex()  # Création d'une instance du Pokédex
                    pokedex.add_pokemon(self.opponent_pokemon.name)  # Ajout du Pokémon vaincu
                    pokedex.save_pokedex()  # Recharger le Pokédex après l'ajout pour refléter les changements

                # Afficher l'écran de victoire/défaite
                overlay = pygame.Surface((800, 600))
                overlay.set_alpha(128)
                overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0, 0))

                font = pygame.font.Font('assets/fonts/Consolab.ttf', 64)
                text = font.render(f"{winner.capitalize()} WINS!", True, (255, 215, 0))
                text_rect = text.get_rect(center=(400, 300))
                self.screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False


    def display_attack_options(self):
        """ Affichage des attaques disponibles avec leurs PP restants """
        for i, move in enumerate(self.player_moves):
            move_text = f"{i + 1}. {move.name} ({move.pp} PP)"
            draw_text(self.screen, move_text, 345, 460 + (i * 25), 25, (50,50,50))

    def player_attack(self, attack):
        """ Exécute une attaque du joueur """
        if attack.pp > 0:
            damage, effectiveness, critical, _ = self.combat.apply_damage(self.player_pokemon, self.opponent_pokemon, attack)
            attack.pp -= 1  # Réduction du PP

            # Añadir mensajes al log
            self.add_message(f"{self.player_pokemon.name.capitalize()} used {attack.name}!")
            if critical:
                self.add_message("--> Critical hit!")
            if effectiveness > 1:
                self.add_message("It's super effective!")
            elif effectiveness < 1:
                self.add_message("It's not very effective...")

    def opponent_attack(self):
        """ L'IA choisit une attaque aléatoire """
        move = random.choice(self.player_moves)
        damage, effectiveness, critical, _ = self.combat.apply_damage(self.opponent_pokemon, self.player_pokemon, move)

        # Añadir mensajes al log
        self.add_message(f"{self.opponent_pokemon.name.capitalize()} used {move.name}!")
        if critical:
            self.add_message("--> Critical hit!")
        if effectiveness > 1:
            self.add_message("It's super effective!")
        elif effectiveness < 1:
            self.add_message("It's not very effective...")