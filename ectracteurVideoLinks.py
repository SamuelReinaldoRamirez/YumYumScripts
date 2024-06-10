import csv
import os

def create_csv(directory, name, video_links):
    csv_path = os.path.join(directory, name + '.csv')
    # with open(csv_file, newline='', encoding='utf-8') as csvfile:
    # Votre code de traitement du fichier CSV ici

    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['video_links']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for link in video_links:
            writer.writerow({'video_links': link})

def process_csv(csv_file, output_directory):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
    # Votre code de traitement du fichier CSV ici

    # with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            video_links = row['video_links'].strip("[]").replace("'", "").split(", ")
            create_csv(output_directory, name, video_links)

if __name__ == "__main__":
    csv_file = "ExtractionRestos.csv"
    output_directory = "output/"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if os.path.exists(csv_file):
        process_csv(csv_file, output_directory)
        print("Les fichiers CSV ont été créés avec succès dans le dossier spécifié !")
    else:
        print("Le fichier CSV spécifié n'existe pas.")
