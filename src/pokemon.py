import requests  # Import the requests module to make HTTP requests.
from io import BytesIO  # Import BytesIO to handle in-memory binary data.
import pygame  # Import the pygame module to handle game graphics and events.
import random  # Import the random module to generate random numbers.
import math  # Import the math module, though it's not currently used.

# Initialisation de Pygame (n'oublie pas d'appeler pygame.init() dans ton programme principal)
pygame.init()

class Pokemon:
    def __init__(self, name, level=1):
        """Initialise le Pokémon avec son nom et niveau (par défaut à 1).
        Récupère les données du Pokémon, ses types, stats, images et mouvements.
        """
        self.name = name.lower()  # Convertir le nom en minuscule.
        self.level = level  # Ajouter un attribut pour le niveau du Pokémon.
        self.data = self._fetch_pokemon_data()  # Récupérer les données du Pokémon depuis l'API.
        self.types = self.data.get("types", [])  # Récupérer les types du Pokémon.
        self.stats = self.data.get("stats", {"hp": 100})  # Récupérer les stats, avec des points de vie par défaut.
        self.front_image = self._load_image("front")  # Charger l'image du Pokémon (vue de face).
        self.back_image = self._load_image("back")  # Charger l'image du Pokémon (vue de dos).
        self.moves = self._fetch_pokemon_moves()  # Récupérer les mouvements du Pokémon.
        
        # Attributs pour les effets visuels
        self.attack_effect = None  # Aucun effet d'attaque initialement.
        self.defense_effect = None  # Aucun effet de défense initialement.
        self.damage_text = None  # Aucun texte de dommage initialement.
        self.damage_timer = 0  # Pas de minuterie de dommage initialement.
        self.damage_pos = None  # Aucune position de dommage initialement.

    def _fetch_pokemon_data(self):
        """Récupère les données du Pokémon depuis l'API PokeAPI."""
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.name}")  # Faire une requête GET à PokeAPI.
        if response.status_code == 200:  # Si la réponse est correcte.
            data = response.json()  # Convertir la réponse JSON en dictionnaire Python.
            return {
                "id": data["id"],  # Récupérer l'ID du Pokémon.
                "name": data["name"],  # Récupérer le nom du Pokémon.
                "types": [t["type"]["name"] for t in data["types"]],  # Récupérer les types du Pokémon.
                "stats": {s["stat"]["name"]: s["base_stat"] for s in data["stats"]},  # Récupérer les stats du Pokémon.
            }
        return {}  # Retourner un dictionnaire vide si la requête échoue.

    def _fetch_pokemon_moves(self):
        """Récupère les mouvements du Pokémon depuis l'API PokeAPI."""
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{self.name}")  # Faire une requête GET à PokeAPI.
        if response.status_code == 200:  # Si la réponse est correcte.
            data = response.json()  # Convertir la réponse JSON en dictionnaire Python.
            moves = [move["move"]["name"] for move in data.get("moves", [])]  # Extraire les mouvements.
            return moves
        return []  # Retourner une liste vide si la requête échoue.

    def _load_image(self, view_type="front"):
        """Charge l'image du Pokémon (vue de face ou de dos) depuis l'URL PokeAPI."""
        if "id" in self.data:
            # Construire la URL selon le type de vue
            if view_type == "back":
                url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{self.data['id']}.png"
            else:
                url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{self.data['id']}.png"
            
            response = requests.get(url)  # Faire une requête GET pour obtenir l'image.
            if response.status_code == 200:
                try:
                    image = pygame.image.load(BytesIO(response.content)).convert_alpha()  # Charger l'image en mémoire.
                    return pygame.transform.scale(image, (100, 100))  # Redimensionner l'image à 100x100 pixels.
                except:
                    return None  # Retourner None si le chargement de l'image échoue.
        return None  # Retourner None si l'ID n'est pas valide ou la requête échoue.

    def get_random_move(self):
        """Retourne un mouvement aléatoire du Pokémon, ou 'tackle' comme mouvement de secours."""
        if self.moves:
            return random.choice(self.moves)  # Retourner un mouvement aléatoire.
        return "tackle"  # Retourner 'tackle' si le Pokémon n'a pas de mouvements.

    def attack(self, target):
        """Attaque le Pokémon cible et déclenche l'effet visuel. Retourne les dégâts infligés."""
        damage = random.randint(10, 30)  # Calculer les dégâts de manière aléatoire.
        target.stats["hp"] -= damage  # Réduire les points de vie du Pokémon cible.
        
        return damage  # Retourner les dégâts infligés.

    def draw(self, screen, x, y, is_player=False):
        """Dessine l'image du Pokémon avec des effets visuels (secousses, texte de dommage, etc.)."""
        draw_x, draw_y = x, y  # Initialiser les coordonnées de dessin.
        
        # Si un effet de défense est actif, appliquer un petit décalage (secousse).
        if self.defense_effect and self.defense_effect.active:
            offset = 5
            draw_x += random.randint(-offset, offset)  # Ajouter un décalage aléatoire sur l'axe X.
            draw_y += random.randint(-offset, offset)  # Ajouter un décalage aléatoire sur l'axe Y.

        # Sélectionner l'image correcte en fonction de si c'est le joueur ou non.
        image_to_use = self.back_image if is_player else self.front_image
        
        # Si l'image sélectionnée n'est pas disponible, utiliser la vue de face comme sauvegarde.
        if not image_to_use:
            image_to_use = self.front_image
        if image_to_use:
            screen.blit(image_to_use, (draw_x, draw_y))  # Dessiner l'image du Pokémon.

        # Si un texte de dommage existe et le timer est encore actif, dessiner le texte.
        if self.damage_text and self.damage_timer > 0:
            font = pygame.font.Font('assets/fonts/Consolab.ttf', 26)  # Charger la police de texte.
            text = font.render(f"-{self.damage_text}", True, (255, 0, 0))  # Rendre le texte en rouge.
            # Positionner le texte au-dessus de la tête du Pokémon.
            if not self.damage_pos:
                self.damage_pos = [draw_x + image_to_use.get_width() // 2, draw_y - 20]
            # Faire monter le texte et disparaître progressivement.
            self.damage_pos[1] -= 0.3  # Déplacer vers le haut.
            alpha = int(255 * (self.damage_timer / 60))  # Calculer la transparence.
            text.set_alpha(alpha)  # Appliquer la transparence.
            text_rect = text.get_rect(center=(self.damage_pos[0], self.damage_pos[1]))  # Centrer le texte.
            screen.blit(text, text_rect)  # Dessiner le texte à l'écran.
            self.damage_timer -= 1  # Réduire le timer.
            if self.damage_timer <= 0:
                self.damage_text = None  # Réinitialiser le texte de dommage lorsque le timer est écoulé.
                self.damage_pos = None  # Réinitialiser la position.

        # Dessiner les effets d'attaque et de défense par-dessus l'image.
        if self.attack_effect:
            self.attack_effect.draw(screen, draw_x, draw_y)
        if self.defense_effect:
            self.defense_effect.draw(screen, draw_x, draw_y)

    @staticmethod
    def get_pokemon_names(limit=151):
        """Récupère les noms des Pokémon jusqu'à une limite donnée (par défaut 151)."""
        url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"  # Faire une requête GET pour récupérer les noms.
        response = requests.get(url)
        pokemon_names = []  # Liste pour stocker les noms des Pokémon.
        
        if response.status_code == 200:  # Si la réponse est correcte.
            data = response.json()  # Convertir la réponse JSON en dictionnaire Python.
            for pokemon in data['results']:  # Pour chaque Pokémon dans les résultats.
                pokemon_names.append(pokemon['name'])  # Ajouter son nom à la liste.
        
        return pokemon_names  # Retourner la liste des noms.
