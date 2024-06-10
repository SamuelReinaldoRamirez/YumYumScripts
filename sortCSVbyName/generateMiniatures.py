import os
import ffmpeg

def generate_thumbnail(video_file_path, thumbnail_file_path):
    (
        ffmpeg.input(video_file_path)
        .filter('scale', w=320, h=240)
        .output(thumbnail_file_path, vframes=1)
        .run(overwrite_output=True)
    )
    print(f"Miniature générée à partir de '{video_file_path}' sous '{thumbnail_file_path}'.")

def generate_thumbnails_for_folder(folder_path):
    # Assurez-vous que le dossier de sortie pour les miniatures existe
    thumbnail_folder = os.path.join(folder_path, "thumbnails")
    if not os.path.exists(thumbnail_folder):
        os.makedirs(thumbnail_folder)

    # Parcourir chaque fichier dans le dossier
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        # Vérifier si le fichier est une vidéo
        if file_path.endswith('.mp4'):
            # Générer le nom de la miniature
            thumbnail_name = os.path.splitext(file_name)[0] + ".jpg"
            thumbnail_path = os.path.join(thumbnail_folder, thumbnail_name)
            # Générer la miniature
            generate_thumbnail(file_path, thumbnail_path)

if __name__ == "__main__":
    # Chemin vers le dossier contenant les vidéos
    video_folder = "csvVideoLinksForMiniaturesSafe"

    # Utilisation de la fonction pour générer les miniatures pour le dossier
    generate_thumbnails_for_folder(video_folder)
