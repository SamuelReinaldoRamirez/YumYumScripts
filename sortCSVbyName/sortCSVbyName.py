import csv

def sort_csv(input_file, output_file):
    # Lecture du fichier CSV
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        # Tri des lignes par ordre alphabétique de la colonne "name"
        sorted_rows = sorted(reader, key=lambda row: row['name'])

    # Écriture du résultat trié dans un nouveau fichier CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writeheader()
        writer.writerows(sorted_rows)

if __name__ == "__main__":
    # Appel de la fonction avec les noms des fichiers d'entrée et de sortie
    sort_csv("restaurants.csv", "output_sorted.csv")
