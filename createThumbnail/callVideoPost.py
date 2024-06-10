import requests


def post_to_endpoint():
    # Endpoint URL
    endpoint_url = "https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/videos"

    # Données à envoyer dans la requête POST
    data = {
        "influenceurs_id": 8
    }

    try:
        # Effectuer la requête POST
        response = requests.post(endpoint_url, json=data)

        # Vérifier si la requête a réussi (code de statut 200)
        if response.status_code == 200:
            print("Requête POST réussie !")
        else:
            print("La requête POST a échoué. Code de statut :", response.status_code)

    except requests.exceptions.RequestException as e:
        print("Une erreur s'est produite lors de la requête POST :", e)


# Appeler la fonction pour effectuer la requête POST
if __name__ == "__main__":
    post_to_endpoint()
