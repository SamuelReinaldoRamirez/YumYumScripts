import json
import requests


def lambda_handler(event, context):
    # print(event.get("url_tiktok"))
    # URL de l'API à appeler
    # api_url = 'https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/thumbnail_tiktok'
    # api_url = 'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@micke.mlk/video/7341039647209966881'
    api_url = 'https://www.tiktok.com/oembed'


    # # Paramètres de la requête
    # params = {
    #     "url_tiktok": "https://www.tiktok.com/@micke.mlk/video/7267217004291984673"
    # }

    # Paramètres de la requête
    params = {
        "url": event.get("url_tiktok")
        # "url": "https://www.tiktok.com/@micke.mlk/video/7267217004291984673"
    }

    headers = {
        'accept': 'application/json, text/javascript, /; q=0.01',
        'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
        'dnt': '1',
        'origin': 'https://tiktok.coderobo.org',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    try:
        # Appel de l'API avec les paramètres
        response = requests.get(api_url, params=params, headers=headers)

        # Vérification de la réponse
        if response.status_code == requests.codes.ok:
            print(response.json().get('thumbnail_url'))
            # Conversion de la réponse en JSON
            data = response.json()

            # Extraction du résultat
            # thumbnail_url = data.get('thumbnail_url')

            # Retourner le résultat dans la réponse de la Lambda
            return {
                'statusCode': 200,
                'body': data.get('thumbnail_url'),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
        else:
            # Si la requête a échoué, retourner un code d'erreur
            print("Error:", response.status_code, response.text)
            return {
                'statusCode': 500,
                'body': "Erreur lors de la récupération de l'image",
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
    except Exception as e:
        # Gérer les erreurs
        return {
            'statusCode': 500,
            'body': str(e),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

# if __name__ == "__main__":
#     main()