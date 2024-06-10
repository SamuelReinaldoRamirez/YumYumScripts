#script pour écrire les adresse email proton à partir des noms des restos
import csv
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def convert_to_proton_format(input_str):
    # Supprimer les accents et convertir en minuscules
    input_str = remove_accents(input_str.lower())
    # Convertir les espaces et caractères spéciaux en "."
    result = ''
    prev_char_is_special = False
    for char in input_str:
        if char.isspace() or not char.isalnum():
            if not prev_char_is_special:
                result += '.'
                prev_char_is_special = True
        else:
            result += char
            prev_char_is_special = False
    # Ajouter "@proton.me" à la fin
#    result += '.yummap'
    result += '.jpg'
    return result

def process_csv(input_file, output_file):
    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    modified_rows = []
    for row in rows:
        modified_row = [convert_to_proton_format(cell) for cell in row]
        modified_rows.append(modified_row)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(modified_rows)

if __name__ == "__main__":
    # Utilisation du script
    input_file = 'input.csv'  # Nom du fichier CSV d'entrée
    output_file = 'outputAlphabetic.csv'  # Nom du fichier CSV de sortie
    process_csv(input_file, output_file)
