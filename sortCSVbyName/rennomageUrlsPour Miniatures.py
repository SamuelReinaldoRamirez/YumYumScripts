import csv

def replace_last_slash_with_dash(input_string):
    # Trouver l'index de la dernière occurrence de "/"
    last_slash_index = input_string.rfind("/")

    # Vérifier si "/" a été trouvé
    if last_slash_index != -1:
        # Remplacer la dernière occurrence de "/" par " - "
        modified_string = input_string[:last_slash_index] + " - " + input_string[last_slash_index + 1:]
        return modified_string
    else:
        # Si "/" n'est pas trouvé, retourner la chaîne d'entrée inchangée
        return input_string

def process_csv(input_file, output_file):
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        fieldnames = reader.fieldnames
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
            writer.writeheader()
            for row in reader:
                row['video_links'] = [replace_last_slash_with_dash(link) for link in eval(row['video_links'])]

# Utilisation du script
input_file = "input.csv"
output_file = "output.csv"
process_csv(input_file, output_file)


# # Exemple d'utilisation
# if __name__ == "__main__":
#     input_string = "https://example.com/path/to/file.txt"
#     output_string = replace_last_slash_with_dash(input_string)
#     print(output_string)
