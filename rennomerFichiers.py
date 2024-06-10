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
        reader = csv.DictReader(csvfile, delimiter=',')
        fieldnames = reader.fieldnames
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            for idx, row in enumerate(reader):
                print(row)
                if idx == 0:
                    # Skip the first row
                    continue
                row['video_links'] = [replace_last_slash_with_dash(link) for link in eval(row['video_links'])]
                writer.writerow(row)

# Utilisation du script
if __name__ == "__main__":
    input_file = "restaurants_data2024-04-22_23 - AWSVideoLinks - PROD.csv"
    output_file = "outputttt.csv"
    process_csv(input_file, output_file)


# # Exemple d'utilisation
# if __name__ == "__main__":
#     input_string = "https://example.com/path/to/file.txt"
#     output_string = replace_last_slash_with_dash(input_string)
#     print(output_string)
