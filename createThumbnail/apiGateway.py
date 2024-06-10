import requests

def appeler_api_gateway():
    # URL de l'API Gateway
    url = "https://20dz3u69zg.execute-api.eu-north-1.amazonaws.com/prod"

    try:
        # Faire une requête GET à l'endpoint de l'API Gateway
        response = requests.get(url)

        # Vérifier si la requête a réussi (code de statut 200)
        if response.status_code == 200:
            print("Requête réussie. Réponse:")
            print(response.json())  # Afficher la réponse JSON
        else:
            print("La requête a échoué avec le code de statut :", response.status_code)
    except Exception as e:
        print("Une erreur s'est produite lors de la requête :", e)

# Appeler la fonction pour effectuer la requête à l'API Gateway
if __name__ == "__main__":
    appeler_api_gateway()
