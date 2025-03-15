import json  # Import the json module to handle reading and writing JSON data.
import os  # Import the os module to handle file and path operations.

class SaveManager:
    SAVE_FILE = "data/last_battle.json"  # Define the path where the battle data will be saved.

    @staticmethod
    def save_battle(player_pokemon, opponent_pokemon):
        """Guarda el último combate
        Saves the details of the last battle (player's and opponent's Pokémon names).
        """
        # Prepare the battle data dictionary to save the Pokémon names
        battle_data = {
            "player_pokemon": player_pokemon.name,  # Store the player's Pokémon name.
            "opponent_pokemon": opponent_pokemon.name  # Store the opponent's Pokémon name.
        }
        
        # Open the SAVE_FILE in write mode and dump the battle data as JSON
        with open(SaveManager.SAVE_FILE, "w") as f:
            json.dump(battle_data, f)  # Write the battle data to the file in JSON format.

    @staticmethod
    def load_last_battle():
        """Carga el último combate guardado
        Loads the last saved battle's Pokémon names.
        Returns None, None if no data is found or if an error occurs.
        """
        # Check if the save file exists; if not, return None for both Pokémon.
        if not os.path.exists(SaveManager.SAVE_FILE):
            return None, None
        
        try:
            # Open the SAVE_FILE in read mode and load the data as JSON
            with open(SaveManager.SAVE_FILE, "r") as f:
                battle_data = json.load(f)  # Parse the JSON data into a dictionary.
                return battle_data["player_pokemon"], battle_data["opponent_pokemon"]  # Return the Pokémon names.
        except:
            return None, None  # Return None if there's an error loading or parsing the file.
