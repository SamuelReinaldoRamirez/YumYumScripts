import pyautogui
import tkinter as tk
import csv

pending_action = None
pending_parametrized_action = None
temp_digits = ""
ecritureNom = False

# Fonction pour écrire dans le fichier CSV et afficher dans la console
def write_to_csv_and_print(action):
    print(action)
    if len(action) == 2:
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
    global pending_action, temp_digits, pending_parametrized_action, ecritureNom
    key_pressed = event.char
    print("!!!!!!!! key pressed")
    print(key_pressed)
    if key_pressed =="\"":
        ecritureNom = not ecritureNom
    if ecritureNom:
        temp_digits+=key_pressed
    else:
        if key_pressed in ["p"]:
            if pending_action:
                write_to_csv_and_print([pending_action, temp_digits])
                pending_action = None
                pending_parametrized_action = None
                temp_digits = ""
            # Écriture de l'action dans le fichier CSV
            pending_parametrized_action = key_pressed
            #write_to_csv_and_print(key_pressed)
        elif key_pressed in ["f"]:
            #flush
            if pending_action:
                write_to_csv_and_print([pending_action, temp_digits])
                pending_action = None
                pending_parametrized_action = None
                temp_digits = ""
            elif pending_parametrized_action:
                write_to_csv_and_print([pending_parametrized_action, temp_digits])
                pending_action = None
                pending_parametrized_action = None
                temp_digits = ""
            # Écriture de l'action dans le fichier CSV
            write_to_csv_and_print(key_pressed)
        elif pending_parametrized_action is None:
            if key_pressed == "a":
                if pending_action:
                    write_to_csv_and_print([pending_action, temp_digits])
                    pending_action = None
                    temp_digits = ""
                # Obtention des coordonnées de la souris
                x, y = pyautogui.position()
                # Écriture des coordonnées dans le fichier CSV
                write_to_csv_and_print([x, y])
            elif key_pressed in ["z", "e", "s", "w", "r", "q", "x"]:
                if pending_action:
                    write_to_csv_and_print([pending_action, temp_digits])
                    pending_action = None
                    temp_digits = ""
                # Écriture de l'action dans le fichier CSV
                write_to_csv_and_print(key_pressed)
            elif key_pressed in ["l", "m", "d"]:
                if pending_action:
                    write_to_csv_and_print([pending_action, temp_digits])
                    pending_action = None
                    temp_digits = ""
                # Écriture de l'action dans le fichier CSV
                #write_to_csv_and_print(key_pressed)
                pending_action = key_pressed
            elif pending_action and key_pressed.isdigit():
                temp_digits += key_pressed
        else :
            temp_digits += key_pressed

# Fonction principale
def main():
    # Création de la fenêtre tkinter
    window = tk.Tk()
    window.title("Enregistrement des actions")

    x_coord = 3000  # Remplacez par la coordonnée x désirée
    y_coord = 200  # Remplacez par la coordonnée y désirée

    # Définir la géométrie de la fenêtre
    window.geometry(f"+{x_coord}+{y_coord}")

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
