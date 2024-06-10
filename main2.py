#CE SCRIPT écrit dnas un csv les coordonnées pour créer une routine
import pyautogui
import tkinter as tk
import csv

# Variable globale pour stocker le dernier fichier CSV modifié
last_csv = None

def update_coordinates():
    # Obtient les coordonnées x, y de la souris
    x, y = pyautogui.position()
    # Met à jour le texte dans la fenêtre
    coordinates_label.config(text=f"Coordonnées de la souris : X = {x}, Y = {y}")
    # Programme une mise à jour toutes les 100 millisecondes
    coordinates_label.after(100, update_coordinates)

def write_to_csv(button, x, y):
    global last_csv
    filename = f"coordinates_{button}.csv"
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([x, y])
    # Stocke le dernier fichier CSV modifié
    last_csv = filename
    # Imprime les coordonnées ajoutées dans le fichier CSV
    print(f"Coordonnées ajoutées au fichier {filename} : X = {x}, Y = {y}")

def add_special_entry(entry):
    global last_csv
    if last_csv:
        with open(last_csv, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([entry])
        print(f"Entrée '{entry}' ajoutée dans le fichier {last_csv}")

def print_coordinates(event=None, button=None):
    # Obtient les coordonnées x, y de la souris
    x, y = pyautogui.position()
    # Si le bouton est "w", "l" ou "m", ajoute une entrée spéciale
    if button in ["w", "l", "m"]:
        add_special_entry(button)
    # Sinon, écrit les coordonnées dans le fichier CSV correspondant au bouton
    else:
        write_to_csv(button, x, y)

def main():
    # Crée la fenêtre
    window = tk.Tk()
    window.title("Coordonnées de la souris")

    # Crée une étiquette pour afficher les coordonnées
    global coordinates_label
    coordinates_label = tk.Label(window, text="")
    coordinates_label.pack(padx=10, pady=10)

    # Crée des boutons pour imprimer les coordonnées dans différents fichiers CSV
    buttons = {
        "P": "p",
        "A": "a",
        "C": "c",
        "W": "w",
        "L": "l",
        "M": "m"
    }
    for key, value in buttons.items():
        button = tk.Button(window, text=f"Imprimer les coordonnées ({key})", command=lambda value=value: print_coordinates(button=value))
        button.pack(padx=10, pady=5)
        # Associe la fonction print_coordinates à la touche correspondante
        window.bind(value, lambda event=None, value=value: print_coordinates(button=value))

    # Lance la mise à jour des coordonnées
    update_coordinates()

    # Démarre la boucle principale de l'interface graphique
    window.mainloop()

if __name__ == "__main__":
    # Écrit l'en-tête des fichiers CSV
    for button in ["p", "a", "c", "w", "l", "m"]:
        filename = f"coordinates_{button}.csv"
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            if button in ["l", "m"]:
                writer.writerow(["Entry"])
            else:
                writer.writerow(["X", "Y"])
    main()
