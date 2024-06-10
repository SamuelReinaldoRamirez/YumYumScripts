import csv
import unicodedata


def nettoyer_chaine(chaine):
    chaine_propre = ""
    precedent_point = False
    for caractere in chaine:
        # Supprimer les accents
        caractere = unicodedata.normalize('NFD', caractere).encode('ascii', 'ignore').decode('utf-8')
        # Convertir en minuscule
        caractere = caractere.lower()
        # Remplacer les caractères spéciaux par "."
        if not caractere.isalnum():
            if not precedent_point:
                chaine_propre += "."
                precedent_point = True
        else:
            chaine_propre += caractere
            precedent_point = False
    return chaine_propre


def ajouter_colonne(input_csv, output_csv):
    with open(input_csv, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        fieldnames = csv_reader.fieldnames
        # Insérer la nouvelle colonne nomPropre entre les colonnes id et created_at
        new_fieldnames = fieldnames[:fieldnames.index('created_at')] + ['nomPropre'] + fieldnames[fieldnames.index('created_at'):]

        with open(output_csv, mode='w', encoding='utf-8', newline='') as new_csv_file:
            writer = csv.DictWriter(new_csv_file, fieldnames=new_fieldnames, delimiter=',')
            writer.writeheader()

            for row in csv_reader:
                name = row['name']
                placeId = row['placeId']
                nom_propre = nettoyer_chaine(name) + placeId
                # Créer une nouvelle ligne avec la nouvelle colonne
                new_row = {}
                for fieldname in new_fieldnames:
                    if fieldname == 'nomPropre':
                        new_row[fieldname] = nom_propre
                    else:
                        new_row[fieldname] = row[fieldname]
                writer.writerow(new_row)


if __name__ == "__main__":
    # Exemple d'utilisation
    input_csv = 'output_sorted.csv'
    output_csv = 'votre_fichier_output.csv'
    ajouter_colonne(input_csv, output_csv)