import requests
from bs4 import BeautifulSoup

def download_video_without_watermark(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Trouver le lien de téléchargement sans watermark
    download_link = soup.find('a', class_='pure-button pure-button-primary is-center u-bl dl-button download_link without_watermark vignette_active notranslate')
    if download_link:
        video_url = download_link['href']
        # Télécharger la vidéo
        response = requests.get(video_url)
        if response.status_code == 200:
            # Enregistrer la vidéo dans un fichier
            with open('video_without_watermark.mp4', 'wb') as f:
                f.write(response.content)
            print("La vidéo sans watermark a été téléchargée avec succès.")
        else:
            print("Échec du téléchargement de la vidéo.")
    else:
        print("Impossible de trouver le lien de téléchargement sans watermark.")

def main():
    # URL de l'endpoint
    url = "https://ssstik.io/abc?url=dl"

    # Données du corps de la requête
    body_data = {
        'id': 'https://www.tiktok.com/@creteilsoleil/video/7364797349878648097?is_from_webapp=1&sender_device=pc',
        'locale': 'en',
        'tt': 'QnNYelI3'
    }

    # En-têtes de la requête
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://ssstik.io/',
        'HX-Request': 'true',
        'HX-Trigger': '_gcaptcha_pt',
        'HX-Target': 'target',
        'HX-Current-URL': 'https://ssstik.io/',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Content-Length': str(len(body_data)),
        'Origin': 'https://ssstik.io',
        'Alt-Used': 'ssstik.io',
        'Connection': 'keep-alive',
        'Cookie': '_ga_ZSF3D6YSLC=GS1.1.1714780501.3.1.1714781407.0.0.0; _ga=GA1.1.585973887.1714307405',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }

    # Envoyer la requête POST
    response = requests.post(url, headers=headers, data=body_data)

    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        print("Requête réussie!")
        # Afficher les en-têtes de la réponse
        print("En-têtes de la réponse:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")

        # Afficher le contenu de la réponse
        print("\nContenu de la réponse:")
        print(response.text)
        # Votre code pour récupérer la réponse HTML de la requête ici

        # Supposons que response_content contient le contenu HTML de la réponse
        download_video_without_watermark(response.text)
    else:
        print("La requête a échoué avec le code de statut:", response.status_code)

if __name__ == "__main__":
    main()
