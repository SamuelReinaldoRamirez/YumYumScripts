import requests
import json


def get_token(file_path):
    # Endpoint pour obtenir le token d'authentification
    api_url = "https://convert.videoconverter.com/v3/user/token"

    try:
        # Envoi de la requête GET à l'endpoint
        response = requests.get(api_url)
        if response.status_code == 200:
            # La requête a réussi
            data = response.json()
            token = data["data"]
            # token = data["data"]["token"]
            print("Token d'authentification obtenu avec succès :", token)
        else:
            print("Échec de la requête. Code de statut :", response.status_code)
            # Affichez les détails de l'erreur si nécessaire
    except requests.exceptions.RequestException as e:
        print("Une erreur s'est produite lors de la requête GET :", e)


# Utilisation de la fonction pour obtenir le token
if __name__ == "__main__":
    video_path = "chemin_vers_votre_video_sur_votre_ordinateur"
    get_token(video_path)
