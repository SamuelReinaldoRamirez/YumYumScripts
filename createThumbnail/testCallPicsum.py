import base64
import json
import requests
import boto3


def lambda_handler(event, context):
    # URL de l'API à appeler
    # api_url = 'https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/thumbnail_tiktok'
    # api_url = 'https://www.tiktok.com/oembed?url=https://www.tiktok.com/@micke.mlk/video/7341039647209966881'
    api_url = 'https://picsum.photos/200'

    # En-têtes de la requête
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://picsum.photos/',
        'Alt-Used': 'picsum.photos',
        'Connection': 'keep-alive',
        'Cookie': '_ga_T978ZC858K=GS1.1.1714667821.5.1.1714668937.0.0.0; _ga=GA1.1.2035376694.1705691560',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1'
    }

    # session = boto3.Session(
    #     aws_access_key_id='VOTRE_ACCESS_KEY_ID',
    #     aws_secret_access_key='VOTRE_SECRET_ACCESS_KEY',
    #     region_name='VOTRE_REGION'
    # )
    #
    # # Créer un client S3
    # s3_client = session.client('s3')
    #
    # # Nom du bucket S3 où vous souhaitez télécharger l'image
    # nom_bucket = 'VOTRE_NOM_BUCKET'
    #
    # # Nom de l'objet dans S3 (par exemple, nom de fichier)
    # nom_objet = 'image.jpg'





    try:
        # Appel de l'API avec les paramètres
        response = requests.get(api_url, headers=headers)

        # Vérification de la réponse
        if response.status_code == requests.codes.ok:
            print(response)
            print(response.content)
            # Afficher le code d'état de la réponse
            print("Code d'état :", response.status_code)

            # Afficher les en-têtes HTTP de la réponse
            print("En-têtes HTTP :", response.headers)

            # Afficher le contenu de la réponse sous forme de texte brut
            print("Contenu texte :", response.text)

            image_base64 = base64.b64encode(response.content)
            print('TTTTTTTTTTTTTTTTTTTTTTTTTTTTS')
            print(image_base64)

            # Retourner le résultat dans la réponse de la Lambda
            return {
                'statusCode': 200,
                'body': image_base64,
                'headers': {
                    'Content-Type': 'image/jpg'
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


def main():
    print(lambda_handler("event", "context"))

if __name__ == "__main__":
    main()