import os

def rename_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            # Construire le nouveau nom de fichier en remplaçant l'extension .jpg par .csv
            new_filename = os.path.splitext(filename)[0] + ".csv"
            # Renommer le fichier
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f"Le fichier {filename} a été renommé en {new_filename}")

if __name__ == "__main__":
    # Chemin du dossier contenant les fichiers
    directory_path = "output"

    # Appeler la fonction pour renommer les fichiers
    rename_files(directory_path)
