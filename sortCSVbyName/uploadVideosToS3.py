import boto3
import os
import ffmpeg

def generate_and_upload_thumbnail(video_file_path, bucket_name):
    # Générer le chemin de la miniature
    thumbnail_file_path = os.path.splitext(video_file_path)[0] + ".jpg"
    # Générer la miniature
    (
        ffmpeg.input(video_file_path)
        .filter('scale', w=320, h=240)
        .output(thumbnail_file_path, vframes=1)
        .run()
    )
    print(f"Miniature générée à partir de '{video_file_path}' sous '{thumbnail_file_path}'.")
    # Téléverser la miniature sur S3
    s3 = boto3.client('s3')
    s3_key = os.path.basename(thumbnail_file_path)
    s3.upload_file(thumbnail_file_path, bucket_name, s3_key)
    print(f"La miniature '{s3_key}' a été téléversée sur S3 dans le seau '{bucket_name}'.")

def upload_folder_to_s3_with_thumbnails(source_folder, bucket_name):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            # Vérifier si le fichier est une vidéo
            if file_path.endswith('.mp4'):
                generate_and_upload_thumbnail(file_path, bucket_name)
            # Téléverser le fichier sur S3
            s3 = boto3.client('s3')
            s3_key = os.path.relpath(file_path, source_folder)
            s3.upload_file(file_path, bucket_name, s3_key)
            print(f"Le fichier '{file}' a été téléversé sur S3 avec la clé '{s3_key}' dans le seau '{bucket_name}'.")

if __name__ == "__main__":
    # Chemin vers le dossier à téléverser et nom du seau S3
    source_folder = "csvVideoLinksForMiniaturesSafe"
    bucket_name = "yummap"

    # Utilisation de la fonction pour téléverser le dossier sur S3 avec les miniatures
    upload_folder_to_s3_with_thumbnails(source_folder, bucket_name)
