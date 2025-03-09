import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="e2c480fee20140a59ec7bcf73e399e59",
    client_secret="8e07210151064725934836cfc4b3136f",
    redirect_uri="http://localhost:8080",
    scope="user-read-playback-state"
))

user = sp.current_user()
print(f"\n🔹 API Authenticated as: {user['display_name']} ({user['id']})")
