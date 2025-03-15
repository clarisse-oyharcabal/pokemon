import json
from .pokemon import Pokemon

class Pokedex:
    """
    The Pokedex class manages a collection of Pokémon and allows operations such as adding new Pokémon
    and saving the updated list to a JSON file.
    """

    def __init__(self):
        """
        Initializes the Pokedex object by setting the file name for storing Pokémon data (`pokedex.json`) 
        and loading the existing data from the file.
        """
        self.pokedex_files = "pokedex.json"
        self.pokedex = self._load_pokedex()

    def _load_pokedex(self):
        """
        Attempts to load the Pokémon data from the `pokedex.json` file.
        If the file is not found or the content is invalid, it returns an empty list.
        
        Returns:
            list: A list containing the Pokémon data from the file or an empty list if the file is not found or corrupted.
        """
        try:
            with open("pokedex.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_pokemon(self, pokemon_name):
        """
        Adds a Pokémon to the Pokedex if it is not already in the list and has a valid image.
        The Pokémon's data (name, types, stats, and sprite) is added to the Pokedex.
        
        Args:
            pokemon_name (str): The name of the Pokémon to add to the Pokedex.
            
        If the Pokémon is already in the list or not found, an error message is printed.
        """
        pokemon = Pokemon(pokemon_name)  # Creates a new Pokemon object
        # Checks if the Pokémon has a front image and is not already in the Pokedex
        if pokemon.front_image and pokemon_name.lower() not in [p["name"].lower() for p in self.pokedex]:
            # Appends the Pokémon data (name, types, stats, sprite) to the Pokedex
            self.pokedex.append({
                "name": pokemon.name,
                "types": pokemon.types,
                "stats": pokemon.stats,
                "sprite": f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_name.lower()}.png"
            })
            # Saves the updated Pokedex to the file
            self.save_pokedex()

            # Reloads the Pokedex from the file to reflect changes
            self.pokedex = self._load_pokedex() 
        else:
            print("❌ Pokémon introuvable ou déjà dans le Pokédex !")

    def save_pokedex(self):
        """
        Saves the current state of the Pokedex to the `pokedex.json` file. The data is written in a formatted JSON
        structure with indentation for readability.
        """
        with open("pokedex.json", "w") as file:
            json.dump(self.pokedex, file, indent=4)
