import sys

import pyautogui


def main():
    # Chemin absolu du fichier principal
    print("maintest called")
    if len(sys.argv) > 1:
        parametre = sys.argv[1]
        print("Paramètre passé :", parametre)
    else:
        print("Aucun paramètre n'a été passé.")
    pyautogui.moveTo(100, 100, duration=1)


if __name__ == "__main__":
    main()