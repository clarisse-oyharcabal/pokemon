import json
import os
import requests
import random
from .pokemon import Pokemon
from .effects import Effect

TYPE_CHART_PATH = "type_chart.json"

# Fonction pour récupérer le tableau des types
def fetch_type_chart():
    """
    Cette fonction récupère les relations de dégâts entre les types de Pokémon depuis l'API PokeAPI
    et les enregistre dans un fichier JSON local 'type_chart.json'. Elle parcourt une liste de types
    et pour chaque type, elle extrait les informations de relations de dégâts (double dégâts, moitié de dégâts, pas de dégâts).
    """
    type_chart = {}
    type_list = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground",
                 "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]

    for type_name in type_list:
        url = f"https://pokeapi.co/api/v2/type/{type_name}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            damage_relations = data["damage_relations"]

            type_chart[type_name] = {
                "double_damage_to": [t["name"] for t in damage_relations["double_damage_to"]],
                "half_damage_to": [t["name"] for t in damage_relations["half_damage_to"]],
                "no_damage_to": [t["name"] for t in damage_relations["no_damage_to"]]
            }

    with open(TYPE_CHART_PATH, "w") as file:
        json.dump(type_chart, file, indent=4)

    return type_chart

# Chargement du tableau des types si le fichier JSON existe, sinon récupération des données via l'API
if os.path.exists(TYPE_CHART_PATH):
    with open(TYPE_CHART_PATH, "r") as file:
        type_chart = json.load(file)
else:
    type_chart = fetch_type_chart()

# 🎯 Gestion des attaques
class Attack:
    """
    Représente une attaque utilisée par un Pokémon.
    """
    def __init__(self, name, attack_type, power, pp, stat_modifier=None):
        """
        Initialise une attaque avec son nom, son type, sa puissance, son nombre de PP et un éventuel modificateur de stats.
        """
        self.name = name
        self.attack_type = attack_type
        self.power = power
        self.pp = pp  # Nombre de fois que l'attaque peut être utilisée
        self.stat_modifier = stat_modifier  # Peut modifier l'attaque ou la défense

    def use(self):
        """
        Utilise un PP de l'attaque et retourne True si l'attaque peut être effectuée, False sinon.
        """
        if self.pp > 0:
            self.pp -= 1
            return True
        return False

# 📈 Gestion des changements de stats
class StatModifier:
    """
    Représente un modificateur de statistiques appliqué à un Pokémon.
    """
    def __init__(self, target_stat, amount):
        """
        Initialise un modificateur de stat avec la statistique cible et la quantité de changement.
        """
        self.target_stat = target_stat
        self.amount = amount  # Peut être positif (boost) ou négatif (malus)

    def apply(self, pokemon):
        """
        Applique le modificateur de statistique au Pokémon.
        """
        pokemon.stats[self.target_stat] += self.amount
        return self.amount

# ⚔️ Classe Combat avec coups critiques et changements de stats
class Combat:
    """
    Gère un combat entre deux Pokémon, avec gestion des attaques, des dégâts et des effets visuels.
    """
    def __init__(self, player, enemy):
        """
        Initialise un combat entre un joueur et un ennemi avec leurs informations respectives.
        """
        self.player = player
        self.enemy = enemy
        self.current_effects = []  # Liste pour maintenir les effets actifs
        # Initialiser les positions par défaut
        self.player.position = [60, 340]
        self.enemy.position = [535, 100]

    def damage_effectiveness(self, attack_type, defender):
        """
        Calcule l'efficacité des dégâts d'une attaque en fonction du type de l'attaque et des types du défenseur.
        """
        defender_types = defender.types if defender.types else ["normal"]
        multiplier = 1

        for defender_type in defender_types:
            if attack_type in type_chart:
                if defender_type in type_chart[attack_type]["double_damage_to"]:
                    multiplier *= 2
                elif defender_type in type_chart[attack_type]["half_damage_to"]:
                    multiplier *= 0.5
                elif defender_type in type_chart[attack_type]["no_damage_to"]:
                    multiplier *= 0
        
        return multiplier

    def apply_damage(self, attacker, defender, attack):
        """
        Applique les dégâts d'une attaque à un défenseur en tenant compte de l'efficacité du type, des statistiques et des effets spéciaux.
        """
        if attack.use():  # Vérifie si l'attaque a encore des PP
            effectiveness = self.damage_effectiveness(attack.attack_type, defender)

            level = attacker.level
            attack_stat = attacker.stats.get("attack", 10)
            defense_stat = defender.stats.get("defense", 5)
            power = attack.power

            # Formule de dégâts
            base_damage = (((2 * level / 5 + 2) * power * (attack_stat / defense_stat)) / 50) + 2
            base_damage *= effectiveness

            # Facteur aléatoire
            base_damage *= random.uniform(0.85, 1.0)

            # Coup critique (1/16 chance)
            critical = random.random() < 1/16
            if critical:
                base_damage *= 2

            damage = max(1, int(base_damage))
            defender.stats["hp"] -= damage

            # Afficher le texte de dégâts
            defender.damage_text = str(damage)
            defender.damage_timer = 50  # Durée en frames (1 seconde à 60 FPS)
            # Créer un effet visuel basé sur le type d'attaque
            effect_x = defender.position[0] if hasattr(defender, 'position') else 400
            effect_y = defender.position[1] if hasattr(defender, 'position') else 300
            effect = Effect(effect_x, effect_y, attack.attack_type)
            self.current_effects.append(effect)

            # Appliquer un modificateur de stat si l'attaque en a un
            stat_change = None
            if attack.stat_modifier:
                stat_change = attack.stat_modifier.apply(defender)

            return damage, effectiveness, critical, stat_change
        return 0, 1, False, None  # Si pas de PP, pas de dégâts

    def winner(self):
        """
        Détermine si l'un des Pokémon a gagné le combat (si les points de vie de l'un sont à zéro).
        """
        if self.enemy.stats["hp"] <= 0:
            return self.player.name, self.enemy.name
        elif self.player.stats["hp"] <= 0:
            return self.enemy.name, self.player.name
        return None, None

    def update_effects(self):
        """
        Met à jour tous les effets actifs dans le combat (par exemple, les effets de statut).
        """
        for effect in self.current_effects[:]:  # Utiliser une copie de la liste pour pouvoir la modifier
            effect.update()
            if effect.is_finished():
                self.current_effects.remove(effect)

    def draw_effects(self, screen):
        """
        Dessine tous les effets actifs sur l'écran.
        """
        for effect in self.current_effects:
            effect.draw(screen)
