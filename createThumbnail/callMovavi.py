import requests
import json


def simulate_post_to_movavi(video_url):
    # URL de l'API de Movavi pour le traitement de vidéos
    api_url = "https://cloud.movavi.com/api/v1/file/create"

    # Token d'authentification
    token = "DbXZiciulUvG9NfEhroCwMQ3WaSEM37eJtFGwb4xpRy2DqTXczFlLIeqs0HjPQ1u"

    api_url_with_token = f"{api_url}?token={token}"

    # Données à envoyer dans la requête POST
    data = {
        "source_url": video_url,
        "thumbnail": True  # Pour demander la génération du thumbnail
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Client": "movaviSite/8.63.3-site"
    }

    try:
        # Effectuer la requête POST à l'API de Movavi
        response = requests.post(api_url_with_token, headers=headers, json=data)

        # Vérifier si la requête a réussi (code de statut 200)
        response_data = response.json()
        if response.status_code == 200:
            print("La requête POST a réussi !")
            thumbnail_url = response_data.get('thumbnail_url')
            if thumbnail_url:
                print("Thumbnail URL:", thumbnail_url)
            else:
                print("Aucun thumbnail n'a été généré par Movavi.")
        else:
            print("La requête POST a échoué. Code de statut :", response.status_code)
        print(response)
        print(response_data)

    except requests.exceptions.RequestException as e:
        print("Une erreur s'est produite lors de la requête POST :", e)


# Appeler la fonction pour simuler la requête POST avec le lien de la vidéo TikTok
if __name__ == "__main__":
    video_url = "https://www.tiktok.com/@kevinrobinx/video/7333648055385853216?is_from_webapp=1&sender_device=pc"
    simulate_post_to_movavi(video_url)
