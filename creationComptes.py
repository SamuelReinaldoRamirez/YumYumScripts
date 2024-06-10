#script qui écrit dans "actions enregistrees les coords quand on strike a, s, z, e, w
import pyautogui
import tkinter as tk
import csv

# Fonction pour écrire dans le fichier CSV et afficher dans la console
def write_to_csv_and_print(action):
    print(action)
    if(len(action)==2):
        with open("actionsEnregistrees.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([action[0], action[1]])
        # Affichage dans la console
        print(f"Action '{action}' ajoutée dans le fichier actionsEnregistrees.csv")
    else:
        with open("actionsEnregistrees.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([action])
        # Affichage dans la console
        print(f"Action '{action}' ajoutée dans le fichier actionsEnregistrees.csv")

# Fonction pour détecter l'appui sur une touche et effectuer l'action correspondante
def detect_key_press(event):
    key_pressed = event.char
    if key_pressed == "a":
        # Obtention des coordonnées de la souris
        x, y = pyautogui.position()
        # Écriture des coordonnées dans le fichier CSV
        write_to_csv_and_print([x,y])
    elif key_pressed in ["z", "e", "s", "w"]:
        # Écriture de l'action dans le fichier CSV
        write_to_csv_and_print(key_pressed)

# Fonction principale
def main():
    # Création de la fenêtre tkinter
    window = tk.Tk()
    window.title("Enregistrement des actions")

    # Association de la fonction de détection de l'appui sur une touche à la fenêtre
    window.bind("<Key>", detect_key_press)

    # Boucle principale de l'interface graphique
    window.mainloop()

if __name__ == "__main__":
    # Écriture de l'en-tête dans le fichier CSV
    with open("actionsEnregistrees.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y"])
    # Exécution de la fonction principale
    main()
