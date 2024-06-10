import pyautogui
import csv
import keyboard
import time

# Fonction pour déplacer la souris et effectuer un clic
def move_and_click(x, y, clicks=1):
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
                print("Attente... Appuyez sur la touche 'w' pour continuer.")
                keyboard.wait("w")
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
                print("Attente... Appuyez sur la touche 'w' pour continuer.")
                keyboard.wait("w")
            elif action == "w":
                move_and_click(x, y, clicks=consecutive_coords)
            consecutive_coords = 0
        elif len(line) == 2 and consecutive_coords == 0:  # Coordonnées de souris avec 2 lignes
            x, y = map(int, line)
            move_and_click(x, y, clicks=2)
        elif len(line) == 3:  # Coordonnées de souris avec 3 lignes
            x, y = map(int, line)
            move_and_click(x, y, clicks=3)

if __name__ == "__main__":
    # Exemple d'utilisation
    execute_actions("actionsEnregistrees.csv")
