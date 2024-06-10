#script qui réalise des actions à partir d'un fichier csv
import csv
import pyautogui
import time

def click(x, y):
    pyautogui.moveTo(x=x, y=y, duration=0.4)
    pyautogui.click(x=x, y=y)
    print(f"Click à la position X={x}, Y={y}")

def double_click(x, y):
    pyautogui.moveTo(x=x, y=y, duration=0.4)
    pyautogui.doubleClick(x=x, y=y)
    print(f"Double click à la position X={x}, Y={y}")

def triple_click(x, y):
    pyautogui.moveTo(x=x, y=y, duration=0.4)
    for _ in range(3):
        pyautogui.click(x=x, y=y)
    print(f"Triple click à la position X={x}, Y={y}")

def copy_text():
    pyautogui.hotkey('ctrl', 'c')
    print("Texte copié")

def paste_text():
    pyautogui.hotkey('ctrl', 'v')
    print("Texte collé")

def main():
    with open('input.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        consecutive_count = 0
        last_coords = None

        for row in reader:
            print(row)
            print(len(row))
            if(row[1] != ""):
                x, y = map(int, row)
                print(x, y)
                if (x, y) == last_coords:
                    consecutive_count += 1
                else:
                    consecutive_count = 0
                last_coords = (x, y)

                if consecutive_count == 2:
                    triple_click(x, y)
                elif consecutive_count == 1:
                    double_click(x, y)
                elif consecutive_count == 0:
                    click(x, y)
            else: # Ligne contenant une action
                action = row[0]
                if action == 'l':
                    copy_text()
                elif action == 'm':
                    paste_text()
                elif action == 'w':
                    print("Pause de 2 secondes...")
                    time.sleep(2)

if __name__ == "__main__":
    main()