import requests


def patch_to_endpoint(video_id):
    # Endpoint URL avec l'ID de la vidéo à mettre à jour
    endpoint_url = f"https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/videos/{video_id}"

    # Données à envoyer dans la requête PATCH
    data = {
        "influenceurs_id": 8,
        "paramUrl": "https://www.tiktok.com/@kevinrobinx/video/7333648055385853216?is_from_webapp=1&sender_device=pc"
    }

    try:
        # Effectuer la requête PATCH
        response = requests.patch(endpoint_url, json=data)

        # Vérifier si la requête a réussi (code de statut 200)
        if response.status_code == 200:
            print(response.json())
            print("Requête PATCH réussie !")
        else:
            print(response.json())
            print("La requête PATCH a échoué. Code de statut :", response.status_code)

    except requests.exceptions.RequestException as e:
        print("Une erreur s'est produite lors de la requête PATCH :", e)


# Appeler la fonction pour effectuer la requête PATCH avec l'ID de la vidéo spécifié
if __name__ == "__main__":
    video_id = 8
    patch_to_endpoint(video_id)
