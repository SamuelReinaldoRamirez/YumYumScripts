import csv

def extraire_nom_propre(input_csv, output_csv):
    with open(input_csv, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        noms_propres = [row['nomPropre'] for row in csv_reader]

    with open(output_csv, mode='w', encoding='utf-8', newline='') as csv_out_file:
        writer = csv.writer(csv_out_file)
        # writer.writerow(['nomPropre'])  # Écrire l'en-tête
        for nom_propre in noms_propres:
            writer.writerow([nom_propre.replace(".","_")])

if __name__ == "__main__":
    # Exemple d'utilisation
    input_csv = 'votre_fichier_output_sorted_by_nomPropre.csv'
    output_csv = 'nom_propre_output.csv'
    extraire_nom_propre(input_csv, output_csv)
