import os
from pydub import AudioSegment

def convert_to_wav():
    """
    Converts specific MP3 audio files to WAV format. The function looks for MP3 files in the 'assets/sounds' 
    directory and converts each file into a corresponding WAV file if it exists.

    The files that are processed are:
        - 'menu.mp3'
        - 'pokedex.mp3'
        - 'combat.mp3'

    Each of these MP3 files is converted to a WAV file in the same directory.
    If the MP3 file doesn't exist or an error occurs during conversion, appropriate messages are printed.
    """
    for music_type in ['menu', 'pokedex', 'combat']:
        mp3_path = f'assets/sounds/{music_type}.mp3'  # Path to the MP3 file
        wav_path = f'assets/sounds/{music_type}.wav'  # Path to save the WAV file
        
        # Check if the MP3 file exists
        if os.path.exists(mp3_path):
            try:
                # Load the MP3 file using AudioSegment
                sound = AudioSegment.from_mp3(mp3_path)
                
                # Export the loaded sound to WAV format
                sound.export(wav_path, format='wav')
                print(f"Conversion réussie : {mp3_path} -> {wav_path}")
            except Exception as e:
                # Handle any errors that occur during the conversion
                print(f"Erreur lors de la conversion de {mp3_path} : {e}")
        else:
            # If the MP3 file doesn't exist, print a message
            print(f"Fichier MP3 non trouvé : {mp3_path}")

# Call the function to start the conversion process
convert_to_wav()
