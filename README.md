# SpoToYou

Transférez vos playlists Spotify vers YouTube Music. Ce script Python utilise spotipy et ytmusicapi pour automatiser le processus. Open source et facile à utiliser.

## ✨ Fonctionnalités

- Authentification sécurisée à Spotify et YouTube Music
- Sélection de vos playlists Spotify
- Transfert automatique des morceaux vers une nouvelle playlist YouTube Music
- Affichage clair des morceaux trouvés / non trouvés

---

## 🔧 Prérequis

- Python 3.7 ou plus
- Un compte Spotify
- Un compte YouTube Music
- Une clé d'authentification `browser.json` pour YouTube Music (voir ci-dessous)

---

## 📦 Installation

1. Téléchargez SpoToYou.py

2. Installez les dépendances : pip install -r requirements.txt

3. Configurez browser.json (Pour se connecter à votre compte YT Music et créer une playlist)

## 🔐 Configuration de l'authentification YouTube Music (`browser.json`)

### 📋 Étapes (via Firefox recommandé) :

1. **Ouvrez** un nouvel onglet dans **Firefox**. (Uniquement Firefox, c'est trop galère sur les autres moteurs)
2. **Allez sur** [https://music.youtube.com](https://music.youtube.com) et connectez-vous à votre compte Google/YouTube Music.
3. **Appuyez sur `Ctrl + Shift + I`** pour ouvrir les outils de développement.
4. Allez dans l’onglet **"Network"** (ou "Réseau").
5. **Filtrez** les requêtes réseau avec `browse` dans la barre de recherche. (Si vous n'en avez pas, cliquez sur Bibilothèque ou Explorer).
6. Cliquez sur **une requête POST** vers `browse` (statut `200`, domaine `music.youtube.com`).
7. **Faites un clic droit** sur la requête > `Copy` > `Copy request headers` (ou "Copier les en-têtes de requête").
8. Ouvrez un éditeur de texte et **collez les en-têtes copiés** dans un nouveau fichier.
9. **Enregistrez ce fichier** sous le nom `browser.json` dans le même dossier que le script.

> ⚠️ **Ne partagez jamais votre fichier `browser.json` publiquement.** Il contient vos cookies d'authentification Google.
