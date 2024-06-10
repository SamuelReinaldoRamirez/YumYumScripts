import sys
import csv
import time
import tkinter as tk

import keyboard
import pyautogui
import pyperclip

button_clicked = None
parametre = ""

def print_red(text):
    print("\033[0;31m{}\033[0m".format(text))

def print_green(text):
    print("\033[0;32m{}\033[0m".format(text))

def print_yellow(text):
    print("\033[0;33m{}\033[0m".format(text))

def print_blue(text):
    print("\033[0;34m{}\033[0m".format(text))

def print_magenta(text):
    print("\033[0;35m{}\033[0m".format(text))

def print_cyan(text):
    print("\033[0;36m{}\033[0m".format(text))

def print_gray(text):
    print("\033[0;37m{}\033[0m".format(text))

def print_bold_red(text):
    print("\033[1;31m{}\033[0m".format(text))

def print_underline_green(text):
    print("\033[4;32m{}\033[0m".format(text))

def print_inverse_yellow(text):
    print("\033[7;33m{}\033[0m".format(text))

def read_csv(csv_file):
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                print(row)  # Afficher chaque ligne du CSV
    except FileNotFoundError:
        print_red("Le fichier CSV spécifié n'a pas été trouvé.")
    finally:
        print_red("finally")


# Fonction pour déplacer la souris et effectuer un clic
def move_and_click(x, y, clicks=1):
    print("click " + str(clicks))
    pyautogui.moveTo(x, y, duration=0.3)
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


# # Exemple d'utilisation avec pyperclip
# def copy_text():
#     pyautogui.hotkey('ctrl', 'c')
#     text = pyperclip.paste()
#     print_yellow(text)
#     pyperclip.copy(text.encode('utf-8'))
#
# def paste_text():
#     text = pyperclip.paste()
#     print("paste")
#     print_yellow(text)
#     pyautogui.typewrite(text.decode('utf-8'))

# Fonction pour scroller de 10 pixels
def scroll():
    print("scroll")
    pyautogui.scroll(100)

def couper():
    print("couper")
    pyautogui.hotkey('ctrl', 'x')

def execute_actions(filename):
    global button_clicked
    global parametre

    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        lines = list(reader)

    consecutive_coords = 0
    for line in lines:
        print_magenta(line)
        if line[0] == "X" and line[1] == "Y":
            continue
        elif len(line) == 1:  # Action spéciale (z, e, s, w)
            action = line[0]
            if action == "f":
                print_cyan("FLUSH")
            elif action == "x":
                couper()
            elif action == "z":
                copy_text()
            elif action == "e":
                paste_text()
            elif action == "s":
                scroll()
            elif action == "r":
                print("YAAAAAAAAAAAAAAAAAAT")
                keyboard.press_and_release('enter')
            elif action == "q":
                print("click DROIT")
                pyautogui.click(button='right')
            elif action == "w":
                print("Attente... Appuyez sur le bouton 'Lancer les actions' pour continuer.")
                # button2.wait_variable(button_clicked)
                time.sleep(0.7)
            elif action == "m":
                print("bon bouton m !!!")
                print(parametre)
                pyperclip.copy(parametre)
            else :
                print_red(f"PROBLEME CAS A GERER {action}")
        elif len(line) == 2:
            # Coordonnées de souris avec 1 ligne
            action = line
            print("AAA")
            print(action)
            if action[0] == "p":
                print(f"parametrized {action[1]}")

                alpha = action[1].split("d")
                print(f"parametrized {alpha}")
                if(alpha[0]=="\"this\""):
                    alpha[0] = parametre
                print(f"parametrized {alpha}")
                try:


                    # tempParam = parametre
                    # parametre = line[0]
                    # print_inverse_yellow(alpha[0])
                    # if (alpha[0] == "this"):
                    #     print_blue("execute action of csvScripts/" + tempParam + ".csv")
                    # aca.pigalle
                    # alphaTemp = alpha[0]
                    # alpha[0] = alpha[0].replace(".","_")
                    print(f"csvVideoLinks/{alpha[0]}/{alpha[0]}.csv")
                    with open(f"csvVideoLinks/{alpha[0]}/videos_{alpha[0]}.csv", mode='r') as file:
                        print("1")
                        # alpha[0] = alphaTemp
                    # with open(f"csvForScripts/aca.pigalle.csv", mode='r') as file:
                        reader = csv.reader(file)
                        lines = list(reader)
                        print("2")

                    # Parcours de chaque ligne du CSV
                    tempParam = parametre
                    for line in lines:
                        print("3")
                        parametre = line[0]
                        # Exécuter le fichier principal avec Python et le paramètre
                        # subprocess.call(["python", main_file, line])
                        # subprocess.call([activate_script, main_file, line])
                        print("YOOOOOOOOOOOOOOOOOOO")
                        print(line)
                        print(line[0])


                        print_blue("execute action of csvScripts/" + alpha[1] + ".csv")
                        execute_actions(f"scripts/{alpha[1]}.csv")
                    parametre = tempParam
                except:
                    print_red("erreur de lecture du script parametré " + parametre)
                finally:
                    print_red("finally du P  " + parametre)
            elif action[0] == "d":
                print(f"execution du script {action[1]}")
                try:
                    execute_actions(f"csvScripts/{action[1]}.csv")
                except:
                    print_red("Le fichier CSV spécifié n'a pas été trouvé.")
                finally:
                    print_red("finally")
            elif action[0]=="l":
                index = action[1]  # Séparer la commande "l, 1" en deux parties
                pp = copy_from_line(index.strip(), "testEcriture.csv")
                print_bold_red(pp)
            elif action[0]=="m":
                print("MAUVAIS bouton m !!!")
                print(parametre)
                pyperclip.copy(parametre)
            else:
                x, y = map(int, line)
                move_and_click(x, y)
                consecutive_coords = 1
        elif len(line) == 1 and consecutive_coords > 0:  # Nouvelle action après des coordonnées
            action = line[0]
            x, y = map(int, lines[lines.index(line) - 1])
            if action == "f":
                print_cyan("FLUSH")
            elif action == "z":
                copy_text()
            elif action == "e":
                paste_text()
            elif action == "s":
                scroll()
            elif action == "r":
                print("YIIIIIIIIIIIIIIIIIIIIIIIIIT")
                keyboard.press_and_release('enter')
            elif action == "q":
                print("click DROIT")
                pyautogui.click(button='right')
            elif action.startswith("l,"):
                _, index = action.split(",")  # Séparer la commande "l, 1" en deux parties
                copy_from_line(index.strip(), "testEcriture.csv")
            elif action == "w":
                print("Attente... Appuyez sur le bouton 'Lancer les actions' pour continuer.")
                # button2.wait_variable(button_clicked)
                time.sleep(0.7)
            elif action == "w":
                move_and_click(x, y, clicks=consecutive_coords)
            else:
                print_red(f"PROBLEME a gerer {action}")
            consecutive_coords = 0
        elif len(line) == 2 and consecutive_coords == 0:  # Coordonnées de souris avec 2 lignes
            x, y = map(int, line)
            move_and_click(x, y, clicks=2)
        elif len(line) == 3:  # Coordonnées de souris avec 3 lignes
            print_yellow(line)
            x, y = map(int, line)
            move_and_click(x, y, clicks=3)
    # Vérification si toutes les lignes ont été lues
    print("Toutes les lignes ont été lues.")
    root.quit()

# Fonction pour copier le texte à partir du fichier CSV source et le coller dans un fichier CSV destination
def copy_from_line(line_index, destination_file):
    print("BBB")
    with open("testEcriture.csv", mode='r') as file:
        reader = csv.reader(file)
        lines = list(reader)
        print("BBB")
        if int(line_index) < len(lines):  # Vérifier si l'index est valide
            print("BBB")
            text_to_copy = lines[int(line_index)][0]  # Récupérer le texte à la ligne spécifiée
            print(text_to_copy)
            # clipboard_content = pyperclip.paste()
            # print("Contenu actuel du presse-papiers : ", clipboard_content)
            # pyperclip.copy('')
            # clipboard_content = pyperclip.paste()
            # print("Contenu actuel du presse-papiers : ", clipboard_content)
            pyperclip.copy(text_to_copy)
            # clipboard_content = pyperclip.paste()
            # print("Contenu actuel du presse-papiers : ", clipboard_content)
            # print("---------------------------")
            # with open(destination_file, mode='a', newline='') as dest_file:
            #     writer = csv.writer(dest_file)
            #     writer.writerow([text_to_copy])
        else:
            print("Index de ligne invalide.")
        return text_to_copy

def start_execution():
    execute_actions("actionsEnregistrees.csv")

def reprend_execution():
    global button_clicked
    button_clicked.set(1)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        parametre = sys.argv[1]
        print("Paramètre passé :", parametre)
    else:
        print("Aucun paramètre n'a été passé.")


    # Création de l'interface utilisateur avec un bouton
    root = tk.Tk()
    root.title("Lancement des actions")

###AVEC bouton
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

###SANS BOUTON
    # time.sleep(3)
    # print_inverse_yellow("ON ATTEND")
    # execute_actions("actionsEnregistrees.csv")
