import csv

def remove_extension(input_csv, output_csv):
    with open(input_csv, newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = [row[0].replace('.jpg', '') for row in reader]

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['restaurant_name'])  # Écrire l'en-tête du fichier CSV
        for name in data:
            writer.writerow([name])

if __name__ == "__main__":
    input_csv = "outputAlphabetic.csv"
    output_csv = "outputYES.csv"

    remove_extension(input_csv, output_csv)
    print("L'extension '.jpg' a été supprimée de chaque ligne avec succès !")
