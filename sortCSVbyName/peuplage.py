import os
import subprocess
import csv

def main():
    print("AAA")
    activate_script = os.path.abspath("../venv/Scripts/python.exe")
    # subprocess.call([activate_script])
    print("AAA")

    # Chemin absolu du fichier principal
    # main_file = os.path.abspath("lecteurBoutonLM.py")
    main_file = os.path.abspath("lecteurBoutonLMinsertionVideo.py")
    # main_file = os.path.abspath("mainTest.py")


    # Lecture du fichier CSV
    # with open("outputYES.csv", mode='r') as file:
    # with open("csvVideoLinks/keopiChIJtY_y3uJv5kcRITnks0-GyFc/videos_keopiChIJtY_y3uJv5kcRITnks0-GyFc.csv", mode='r') as file:
    with open("nom_propre_output.csv", mode='r') as file:
        reader = csv.reader(file)
        lines = list(reader)

    # Parcours de chaque ligne du CSV
    for line in lines:
        # Exécuter le fichier principal avec Python et le paramètre
        # subprocess.call(["python", main_file, line])/
        print("CAAAAALLLLLLLL")
        subprocess.call([activate_script, main_file, line])


if __name__ == "__main__":
    main()
