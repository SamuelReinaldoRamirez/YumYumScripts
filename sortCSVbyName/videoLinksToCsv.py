import csv

def parse_input_file(input_file):
    restaurant_data = []
    with open(input_file, 'r') as file:
        lines = file.readlines()
        current_restaurant = None
        for line in lines:
            if line.startswith("http"):
                if current_restaurant:
                    current_restaurant.append(line.strip())
            else:
                if current_restaurant:
                    restaurant_data.append(current_restaurant)
                # Supprime les ";" des noms de restaurants et ordonne par ordre alphabétique
                current_restaurant = [line.strip().replace(";", "")]
        if current_restaurant:
            restaurant_data.append(current_restaurant)
    # Ordonne les lignes par ordre alphabétique des noms de restaurants
    restaurant_data.sort(key=lambda x: x[0])
    return restaurant_data

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['nom_resto', 'video_links'])
        for item in data:
            writer.writerow([item[0], '\n'.join(item[1:])])

def main(input_file, output_file):
    restaurant_data = parse_input_file(input_file)
    write_to_csv(restaurant_data, output_file)

if __name__ == "__main__":
    input_file = "formatResto/scriptAide.txt"  # Remplacez par le chemin de votre fichier d'entrée
    output_file = "formatResto/videoLinks.csv"  # Remplacez par le chemin de votre fichier CSV de sortie souhaité
    main(input_file, output_file)
