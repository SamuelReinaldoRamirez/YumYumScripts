import pyautogui
import csv
import keyboard
import time
import tkinter as tk

button_clicked = None

# Fonction pour déplacer la souris et effectuer un clic
def move_and_click(x, y, clicks=1):
    print("click " + str(clicks))
    pyautogui.moveTo(x, y)
    if clicks == 1:
        pyautogui.click()
    elif clicks == 2:
        pyautogui.doubleClick()
    elif clicks == 3:
        pyautogui.tripleClick()

# Fonction pour copier le texte sélectionné
def copy_text():
    pyautogui.hotkey('ctrl', 'c')

# Fonction pour coller le texte copié
def paste_text():
    pyautogui.hotkey('ctrl', 'v')

# Fonction pour scroller de 10 pixels
def scroll():
    print("scroll")
    pyautogui.scroll(-50)

# Fonction pour exécuter les actions en fonction du contenu du fichier CSV
def execute_actions(filename):
    global button_clicked

    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        lines = list(reader)

    consecutive_coords = 0
    for line in lines:
        if line[0] == "X" and line[1] == "Y":
            continue
        elif len(line) == 1:  # Action spéciale (z, e, s, w)
            action = line[0]
            if action == "z":
                copy_text()
            elif action == "e":
                paste_text()
            elif action == "s":
                scroll()
            elif action == "w":
                print("Attente... Appuyez sur le bouton 'Lancer les actions' pour continuer.")
                # Ici, nous n'avons plus besoin de keyboard.wait("w")
                button2.wait_variable(button_clicked)
        elif len(line) == 2:  # Coordonnées de souris avec 1 ligne
            x, y = map(int, line)
            move_and_click(x, y)
            consecutive_coords = 1
        elif len(line) == 1 and consecutive_coords > 0:  # Nouvelle action après des coordonnées
            action = line[0]
            x, y = map(int, lines[lines.index(line) - 1])
            if action == "z":
                copy_text()
            elif action == "e":
                paste_text()
            elif action == "s":
                scroll()
            elif action == "w":
                print("Attente... Appuyez sur le bouton 'Lancer les actions' pour continuer.")
                button2.wait_variable(button_clicked)
            elif action == "w":
                move_and_click(x, y, clicks=consecutive_coords)
            consecutive_coords = 0
        elif len(line) == 2 and consecutive_coords == 0:  # Coordonnées de souris avec 2 lignes
            x, y = map(int, line)
            move_and_click(x, y, clicks=2)
        elif len(line) == 3:  # Coordonnées de souris avec 3 lignes
            x, y = map(int, line)
            move_and_click(x, y, clicks=3)

def start_execution():
    execute_actions("actionsEnregistrees.csv")

def reprend_execution():
    global button_clicked
    button_clicked.set(1)

if __name__ == "__main__":
    # Création de l'interface utilisateur avec un bouton
    root = tk.Tk()
    root.title("Lancement des actions")

    # Définir les dimensions et la position de la fenêtre
    window_width = 200  # Largeur de la fenêtre
    window_height = 200  # Hauteur de la fenêtre
    screen_width = root.winfo_screenwidth()  # Largeur de l'écran
    screen_height = root.winfo_screenheight()  # Hauteur de l'écran
    x_position = screen_width - window_width - 100  # Position x de la fenêtre (100 pixels à partir du bord droit)
    y_position = (screen_height - window_height) // 2  # Position y centrée verticalement

    # Définir la géométrie de la fenêtre
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    button_clicked = tk.IntVar()
    # Créer les boutons
    button = tk.Button(root, text="Lancer les actions", command=start_execution)
    button.pack(padx=10, pady=10)
    button2 = tk.Button(root, text="Reprendre les actions", command=reprend_execution)
    button2.pack(padx=10, pady=40)

    # Lancer l'interface utilisateur
    root.mainloop()


