import os
import csv


def creer_csv_par_dossier(dossier_racine):
    # Parcours des dossiers fils du dossier racine
    for dossier_fils in os.listdir(dossier_racine):
        chemin_dossier_fils = os.path.join(dossier_racine, dossier_fils)

        # Vérification si l'élément est un dossier
        if os.path.isdir(chemin_dossier_fils):
            # Création du nom du fichier CSV pour ce dossier fils
            nom_csv = f"videos_{dossier_fils}.csv"
            chemin_csv = os.path.join(chemin_dossier_fils, nom_csv)

            # Création du fichier CSV et écriture des en-têtes
            with open(chemin_csv, mode='w', newline='') as fichier_csv:
                writer = csv.writer(fichier_csv)
                # writer.writerow(['Nom du fichier'])

                # Parcours des fichiers dans le dossier fils
                for fichier in os.listdir(chemin_dossier_fils):
                    chemin_fichier = os.path.join(chemin_dossier_fils, fichier)

                    # Vérification si le fichier n'est pas un dossier et n'est pas le CSV
                    if os.path.isfile(chemin_fichier) and not fichier.endswith('.csv'):
                        # Écriture du nom du fichier dans le CSV
                        writer.writerow([fichier])

if __name__ == "__main__":
    # Exemple d'utilisation
    dossier_racine = "csvVideoLinks"
    creer_csv_par_dossier(dossier_racine)
