import os
import shutil

def rename_and_copy_files(source_dir, destination_dir):
    # Parcourir chaque dossier RESTO
    for resto_folder in os.listdir(source_dir):
        resto_folder_path = os.path.join(source_dir, resto_folder)
        if os.path.isdir(resto_folder_path):
            # Parcourir les fichiers dans chaque dossier RESTO
            for file_name in os.listdir(resto_folder_path):
                file_path = os.path.join(resto_folder_path, file_name)
                # Vérifier si le fichier est un fichier vidéo
                if not file_name.endswith('.csv'):
                    # Construire le nouveau nom du fichier
                    new_file_name = f"{resto_folder} - {file_name}"
                    new_file_path = os.path.join(destination_dir, new_file_name)
                    # Copier et renommer le fichier dans le dossier de destination
                    shutil.copyfile(file_path, new_file_path)
                    print(f"Le fichier '{file_name}' a été copié et renommé en '{new_file_name}' dans '{destination_dir}'.")

if __name__ == "__main__":
    # Chemin vers le dossier d'entrée et de sortie
    input_dir = "csvVideoLinksForMiniatures"
    output_dir = "csvVideoLinksForMiniaturesSafe"

    # Créer le dossier de sortie s'il n'existe pas
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Appeler la fonction pour renommer et copier les fichiers
    rename_and_copy_files(input_dir, output_dir)
