import base64

import requests
from PIL import Image
import io

def main():
    # Remplacez 'eu-north-1' et '590184094954' par votre région et votre numéro de compte AWS respectivement
    # region = 'eu-north-1'
    # account_id = '590184094954'
    # api_id = 'sw2d89qfn8'

    # Construisez l'URL de l'API Gateway
    # api_endpoint = f'https://sw2d89qfn8.execute-api.eu-north-1.amazonaws.com/test111'
    api_endpoint = f'https://sw2d89qfn8.execute-api.eu-north-1.amazonaws.com/dlVideoOnInternet'

    # Envoyez une requête GET à l'URL de l'API Gateway
    response = requests.get(api_endpoint)

    image_bytes = io.BytesIO(base64.b64decode(response.content))
    image = Image.open(image_bytes)
    image.show()

    # Vérifiez si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        print("Requête réussie!")
        print("Réponse:", response.text)
    else:
        print("La requête a échoué avec le code de statut:", response.status_code)

if __name__ == "__main__":
    main()
