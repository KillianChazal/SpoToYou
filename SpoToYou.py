from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import time

def test_ytmusic_connection(browser_auth_file="browser.json"):
    """Test de la connexion à YouTube Music avec browser.json"""
    if not os.path.exists(browser_auth_file):
        print(f"Fichier {browser_auth_file} non trouvé.")
        print("Suivez le tutoriel sur GitHub'")
        return None

    try:
        ytmusic = YTMusic(browser_auth_file)
        playlists = ytmusic.get_library_playlists(limit=1)
        print("Connexion YouTube Music réussie via browser.json")
        return ytmusic

    except Exception as e:
        print(f"Erreur lors de la connexion à YouTube Music : {e}")
        return None

def get_spotify_playlists(sp):
    """Récupère et affiche les playlists Spotify de l'utilisateur"""
    try:
        user_id = sp.me()['id']
        playlists = sp.user_playlists(user_id)

        if not playlists or not playlists.get('items'):
            print("Aucune playlist trouvée sur votre compte Spotify.")
            return None

        print(f"\n=== VOS PLAYLISTS SPOTIFY ===")
        for i, playlist in enumerate(playlists['items'], 1):
            name = playlist['name']
            track_count = playlist['tracks']['total']
            owner = playlist['owner']['display_name']
            print(f"{i}. {name} ({track_count} morceaux) - par {owner}")

        return playlists['items']

    except Exception as e:
        print(f"Erreur lors de la récupération des playlists : {e}")
        return None

def get_spotify_tracks(sp, playlist_id):
    """Récupère tous les morceaux d'une playlist Spotify"""
    tracks = []
    try:
        results = sp.playlist_items(playlist_id, limit=100)

        while results:
            if results.get('items'):
                for item in results['items']:
                    if not item:
                        continue

                    track = item.get('track')
                    if track and track.get('name'):
                        name = track['name']
                        artists = [artist['name'] for artist in track.get('artists', [])]
                        artist = artists[0] if artists else "Artiste inconnu"

                        search_query = f"{name} {artist}"
                        tracks.append({
                            'name': name,
                            'artist': artist,
                            'search_query': search_query
                        })

            if results.get('next'):
                results = sp.next(results)
            else:
                break

        return tracks

    except Exception as e:
        print(f"Erreur lors de la récupération des morceaux : {e}")
        return []

def search_and_add_tracks(ytmusic, playlist_id, tracks):
    """Recherche et ajoute les morceaux à la playlist YouTube Music"""
    added_count = 0
    not_found_count = 0
    errors = []

    print(f"\n=== AJOUT DES MORCEAUX ===")
    total = len(tracks)

    for i, track in enumerate(tracks, 1):
        print(f"({i}/{total}) {track['name']} - {track['artist']}")

        try:
            search_results = ytmusic.search(track['search_query'], filter="songs", limit=5)

            if search_results and isinstance(search_results, list):
                first_result = search_results[0]
                if 'videoId' in first_result and first_result['videoId']:
                    video_id = first_result['videoId']
                    ytmusic.add_playlist_items(playlist_id, [video_id])
                    print("Ajouté")
                    added_count += 1
                else:
                    print("videoId manquant")
                    not_found_count += 1
                    errors.append(f"{track['name']} - {track['artist']} (videoId manquant)")
            else:
                print("Aucun résultat trouvé")
                not_found_count += 1
                errors.append(f"{track['name']} - {track['artist']} (Aucun résultat)")

        except Exception as e:
            print(f"Erreur : {e}")
            not_found_count += 1
            errors.append(f"{track['name']} - {track['artist']} (Erreur: {e})")

        time.sleep(0.1)

    return added_count, not_found_count, errors

def main():
    print("=== SpoToYou ===")

    print("\n=== CONNEXION À YOUTUBE MUSIC ===")
    ytmusic = test_ytmusic_connection("browser.json")
    if not ytmusic:
        return

    print("\n=== CONNEXION À SPOTIFY ===")
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id="fab9e6b7a8c246d885108e62b5f32b28",
            client_secret="f9aeece64bb442f48f625c64778e7ca3",
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="playlist-read-private playlist-read-collaborative"
        ))

        user_info = sp.me()
        print(f"Connecté en tant que {user_info['display_name']}")

    except Exception as e:
        print(f"Erreur lors de la connexion Spotify : {e}")
        return

    playlists = get_spotify_playlists(sp)
    if not playlists:
        return

    while True:
        try:
            choice = input(f"\nChoisissez une playlist (1-{len(playlists)}) : ")
            index = int(choice)
            if 1 <= index <= len(playlists):
                selected_playlist = playlists[index - 1]
                break
            else:
                print(f"Entrez un nombre entre 1 et {len(playlists)}")
        except ValueError:
            print("Veuillez entrer un nombre valide")
        except KeyboardInterrupt:
            print("\nOpération annulée.")
            return

    playlist_name = selected_playlist['name']
    playlist_id = selected_playlist['id']
    print(f"Playlist sélectionnée : {playlist_name}")

    print("Récupération des morceaux...")
    tracks = get_spotify_tracks(sp, playlist_id)

    if not tracks:
        print("Aucun morceau à transférer.")
        return

    print(f"{len(tracks)} morceaux trouvés")

    print("Création de la playlist sur YouTube Music...")
    try:
        yt_playlist_name = f"{playlist_name}"
        yt_playlist_id = ytmusic.create_playlist(
            title=yt_playlist_name,
            description=f"Playlist importée depuis Spotify",
            privacy_status="PRIVATE"
        )
        print(f"Playlist créée : {yt_playlist_name}")

    except Exception as e:
        print(f"Erreur lors de la création de la playlist : {e}")
        return

    added, not_found, errors = search_and_add_tracks(ytmusic, yt_playlist_id, tracks)

    print(f"\n=== RÉSUMÉ DU TRANSFERT ===")
    print(f"Playlist créée : {yt_playlist_name}")
    print(f"Morceaux ajoutés : {added}/{len(tracks)}")
    print(f"Morceaux non trouvés : {not_found}")
    if len(tracks):
        print(f"Taux de réussite : {(added / len(tracks)) * 100:.1f}%")

    if errors:
        print("\n=== MORCEAUX NON AJOUTÉS ===")
        for err in errors[:10]:
            print(f"• {err}")
        if len(errors) > 10:
            print(f"... et {len(errors) - 10} autres")

    print("\nTransfert terminé.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOpération interrompue par l'utilisateur.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
