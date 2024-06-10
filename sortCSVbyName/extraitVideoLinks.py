import csv
import os

nomDossier = "csvVideoLinks/"

def extraire_colonnes(input_csv):
    noms_videos = {}
    with open(input_csv, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        i=0
        for row in csv_reader:
            i+=1
            nom_propre = row['nomPropre']
            video_links = eval(row['video_links'])  # Convertir la chaîne en liste
            noms_videos[nom_propre] = video_links
        print(i)
    return noms_videos


def creer_dossiers_et_fichiers(noms_videos):
    for nom_propre, video_links in noms_videos.items():
        # Créer le dossier nomPropre s'il n'existe pas
        dossier_nom_propre = nom_propre.replace('.', '_')  # Remplacer les points par des underscores
        if not os.path.exists(nomDossier + dossier_nom_propre):
            os.makedirs(nomDossier + dossier_nom_propre)

        # Chemin du fichier CSV à créer dans le dossier nomPropre
        fichier_csv = os.path.join(nomDossier + dossier_nom_propre, f"{dossier_nom_propre}.csv")

        # Écrire les données dans le fichier CSV
        with open(fichier_csv, mode='w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Écrire l'en-tête
            # writer.writerow([nom_propre])
            # Écrire les données ligne par ligne
            for video_link in video_links:
                writer.writerow([video_link])

        # # Écrire les données dans le fichier CSV
        # with open(fichier_csv, mode='w', encoding='utf-8', newline='') as csv_file:
        #     writer = csv.writer(csv_file)
        #     # Écrire l'en-tête
        #     writer.writerow(['nomPropre', 'videoLink'])
        #     # Écrire les données ligne par ligne
        #     for video_link in video_links:
        #         writer.writerow([nom_propre, video_link])

if __name__ == "__main__":
    # Exemple d'utilisation
    input_csv = 'votre_fichier_output_sorted_by_nomPropre.csv'
    noms_videos = extraire_colonnes(input_csv)
    creer_dossiers_et_fichiers(noms_videos)
