import time
import random
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "c03c678f84a54e1a98938a82a8efc56d"
SPOTIFY_CLIENT_SECRET = "07cc9db30d144061b1d574cd9d252e46"
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'

scope = "playlist-read-private playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=scope
))

playlist_id = "6elEdllEpIO5fvPDBuDVeT"

suggestions = {
    "happy": "Take on a creative or challenging task!",
    "stressed": "Take a 5-second mindfulness break. Remember to breathe deeply.",
    "sad": "Feel it out! A good cry is all you need sometimes.",
    "angry": "Sometimes a crashout is completely necessary..",
    "bored": "Find a new song or explore something you’re curious about!"
}

quotes = [
    "You’ve got this! Take it one step at a time.",
    "Small progress is still progress.",
    "Breathe. This too shall pass.",
    "Focus on what you can control, one step at a time.",
    "Every small win adds up to big success!"
]

def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        print(f"{mins:02}:{secs:02}", end="\r")
        time.sleep(1)
        seconds -= 1
    print("\nTime's up! Go slay the rest of the day")

def log_mood(mood):
    log_data = {
        "mood": mood,
        "timestamp": time.ctime()
    }
    with open("mood_log.json", "a") as file:
        json.dump(log_data, file)
        file.write("\n")

def recommend_song(mood):
    mood_playlists = {
        "happy": "spotify:playlist:6elEdllEpIO5fvPDBuDVeT",
        "stressed": "spotify:playlist:6SK6CIop8qPST2Rj3B7kvP",
        "sad": "spotify:playlist:4PjwWA5qGjZZ6gemFskn3c",
        "angry": "spotify:playlist:3LBPp2ciQq8L3qTUXmWNg8",
        "bored": "spotify:playlist:2pIzKRC1JmKmhIEoaxhSMm"
    }

    if mood in mood_playlists:
        playlist_id = mood_playlists[mood]
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']

        if tracks:
            track = random.choice(tracks)['track']
            return f"🎵 Recommended Song: {track['name']} by {track['artists'][0]['name']}"
        else:
            return "No song recommendation available right now."
    else:
        return "No playlist found for this mood."


def main():
    print("How are you feeling? (happy, stressed, sad, angry, bored)")
    mood = input("Enter your mood: ").lower()

    if mood in suggestions:
        print(f"\nSuggestion: {suggestions[mood]}")
        print(f"\nMotivational Quote: {random.choice(quotes)}")
        print(f"\n{recommend_song(mood)}")


        log_mood(mood)


        start_timer = input("\nWould you like to start a timer? (yes/no): ").lower()
        if start_timer == "yes":
            if mood == "stressed":
                countdown(5)  # 5 seconds
            elif mood == "sad":
                countdown(15)
            elif mood == "angry":
                countdown(15)
            else:
                countdown(25)
    else:
        print("Sorry, I don't have suggestions for that mood.")

if __name__ == "__main__":
    main()

