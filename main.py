#on va target xanos et recup 10ids pars 10 ids les données de placeID des restos. Si dans le batch il manque des données, on regarde si il y a bien 10 resto qui ont été questionnés.
#si oui, alors on lance la requet pour récupérer les placeId à partir e nom et localisation.
# du coup on se retrouve avec 10 placeIds par 10 placeIds.

#en fait on va faire un script get placeId qu'on execute sur les ids de restos en questions quand les placesIds ne sont pas remplies#
#on parcours les placeidS avec les ids de resto correspondant et on requete places pour avoir les données de details

#puis on fait un post dans xano pour peupler la bdd

# https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants?_limit={batch_size}&_start={start_index}
# https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants?_limit=10&_start=0
import ast

import requests
import time
import csv
import json
import datetime
from colorama import init, Fore


xanoKey = 'LYxWamUX'
YOUR_GOOGLE_MAPS_API_KEY = 'AIzaSyBM05T0u8LoAKr2MtbTIjXtFmrU-06ye6U'

# #DUMP
# def get_tables():
#     url = f"https://x8ki-letl-twmt.n7.xano.io/api:{xanoKey}/schema"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json().get('tables', [])
#     else:
#         print(f"Erreur lors de la récupération des tables depuis Xano: {response.text}")
#         return None
#
# def export_table(table_name):
#     url = f"https://x8ki-letl-twmt.n7.xano.io/api:{xanoKey}/{table_name}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Erreur lors de la récupération des données de la table {table_name} depuis Xano: {response.text}")
#         return None
#
# def export_database():
#     tables = get_tables()
#     if tables:
#         for table in tables:
#             table_name = table.get('name')
#             data = export_table(table_name)
#             if data:
#                 with open(f"{table_name}_data.json", "w") as json_file:
#                     json.dump(data, json_file, indent=4)
#                 print(f"Données de la table '{table_name}' exportées avec succès.")
#             else:
#                 print(f"Échec de l'export des données de la table '{table_name}'.")



def get_all_restaurants():
    url = f"https://x8ki-letl-twmt.n7.xano.io/api:{xanoKey}/restaurants"
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Erreur lors de la récupération des restaurants depuis Xano: {response.text}")
        return None

def get_restaurant_by_id(id):
    url = f"https://x8ki-letl-twmt.n7.xano.io/api:{xanoKey}/restaurants/{id}"
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Erreur lors de la récupération de restaurant {id} depuis Xano: {response.text}")
        return None

def update_place_id_for_resto(resto, place_id):
    id = resto["id"]
    url = f"https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants/{id}"  # Remplacez cette URL par la vôtre
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "id": id,
        # "restaurants_id": id,
        "name": resto["name"],
        "address_str": resto["address_str"],
        "published": resto["published"],
        "GPS_address": resto["GPS_address"],
        "video_links": resto["video_links"],
        "phone_number": resto["phone_number"],
        "tags_id": resto["tags_id"],
        "placeId": place_id,
        "ratings": resto["ratings"],
        "price": resto["price"],
        "website_url": resto["website_url"],
        "handicap": resto["handicap"],
        "vege": resto["vege"],
        "schedule": resto["schedule"],
        "picture_profile": resto["picture_profile"],
        "number_of_reviews": resto["number_of_reviews"],
        "reviews": resto["reviews"],
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        return data
        print("PlaceId updated successfully.")
    else:
        print(f"Error updating placeId: {response.text}")

def getPlaceIdRequestDetails(resto):
    return [resto["name"], resto["GPS_address"]["data"]["lat"], resto["GPS_address"]["data"]["lng"]]

def fetch_place_id(restaurant_name, latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={restaurant_name}&location={latitude},{longitude}&radius=500&type=restaurant&key={YOUR_GOOGLE_MAPS_API_KEY}"  # Remplacez YOUR_GOOGLE_MAPS_API_KEY par votre clé API Google Maps
    response = requests.get(url)
    data = response.json()
    if data.get('results'):
        return data['results'][0]['place_id']
    return None

def fetch_restaurant_details(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={YOUR_GOOGLE_MAPS_API_KEY}"  # Remplacez YOUR_GOOGLE_MAPS_API_KEY par votre clé API Google Maps
    response = requests.get(url)
    data = response.json()
    result = data.get('result', {})
    result_utile = {
        "ratings": result.get('rating', None),
        "price": result.get('price_level', None),
        "website_url": result.get('website', ''),
        "handicap": result.get('wheelchair_accessible_entrance', False),
        "vege": result.get('serves_vegetarian_food', False),
        "schedule": result["opening_hours"].get('weekday_text', []),
        "picture_profile": result["photos"][0].get('photo_reference', ''),
        "number_of_reviews": result.get("user_ratings_total", None),
        "reviews": result.get('reviews', [])
    }
    return result_utile

# def get_tables():
#     url = f"https://x8ki-letl-twmt.n7.xano.io/api:{xanoKey}/schema"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json().get('tables', [])
#     else:
#         print(f"Erreur lors de la récupération des tables depuis Xano: {response.text}")
#         return None
#
# def export_table(table_name):
#     url = f"https://x8ki-letl-twmt.n7.xano.io/api:{xanoKey}/{table_name}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Erreur lors de la récupération des données de la table {table_name} depuis Xano: {response.text}")
#         return None
#
# def export_database():
#     tables = get_tables()
#     if tables:
#         for table in tables:
#             table_name = table.get('name')
#             data = export_table(table_name)
#             if data:
#                 with open(f"{table_name}_data.json", "w") as json_file:
#                     json.dump(data, json_file, indent=4)
#                 print(f"Données de la table '{table_name}' exportées avec succès.")
#             else:
#                 print(f"Échec de l'export des données de la table '{table_name}'.")

def exportRestos(nameAppend=""):
    restos = get_all_restaurants()
    # Obtenir la date et l'heure actuelles
    maintenant = datetime.datetime.now()

    # Formater la date et l'heure dans un format approprié pour le nom de fichier
    nom_export = maintenant.strftime("%Y-%m-%d_%H")

    # Utiliser le nom_export pour nommer votre fichier d'export
    # nom_fichier_export = f"export_{nom_export}.csv"

    csv_filename = f"restaurants_data{nom_export}{nameAppend}.csv"
    field_names = [
        "id",
        "created_at",
        "name",
        "address_str",
        "published",
        "video_links",
        "phone_number",
        "tags_id",
        "placeId",
        "ratings",
        "price",
        "website_url",
        "handicap",
        "vege",
        "schedule",
        "picture_profile",
        "number_of_reviews",
        "GPS_address",
        "reviews"
    ]
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)

        writer.writeheader()
        for restaurant in restos:
            print(restaurant)
            try:
                writer.writerow(restaurant)
            except Exception as e:
                print(f"Une erreur s'est produite lors de l'écriture des données du restaurant : {e}")

    print(f"Les données ont été écrites dans le fichier CSV : {csv_filename}")

# # Définir le nom du fichier CSV
# csv_filename = "restaurants_data.csv"
#
# # Les noms des champs dans les données
# field_names = [
#     "id",
# #     "created_at",
# #     "name",
# #     "address_str",
# #     "published",
# #     "video_links",
# #     "phone_number",
# #     "tags_id",
# #     "placeId",
# #     "ratings",
# #     "price",
# #     "website_url",
# #     "handicap",
# #     "vege",
# #     "schedule",
# #     "picture_profile",
# #     "number_of_reviews",
# #     "GPS_address",
# #     "reviews"
# ]
#
# # Écrire les données dans le fichier CSV
# with open(csv_filename, mode='w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=field_names)
#
#     writer.writeheader()
#     for restaurant in get_all_restaurants():
#         writer.writerow(restaurant)
#
# print(f"Les données ont été écrites dans le fichier CSV : {csv_filename}")

# def majDetailsRestos(all_restaurants = get_all_restaurants()):
#     print("METTRE A JOUR LES COLONNES DE RESTAURANT DANS LE CODE DUMP DE LA TABLE RESTAURANT EN COURS... y a-t-il eu des modifications faites sur les colonnes depuis le dernier dump?")
#     exportRestos()
#     time.sleep(3)
#     for resto in all_restaurants:
#         try:
#             details = getPlaceIdRequestDetails(resto)
#             placeId = fetch_place_id(details[0], details[1], details[2])
#             resto = update_place_id_for_resto(resto, placeId)
#             print(resto)
#             restoDetails = fetch_restaurant_details(placeId)
#             resto = update_details_for_resto(resto, restoDetails)
#         except Exception as e:
#             print(f"Une erreur s'est produite lors du traitement du restaurant : {e}")
#             time.sleep(15)
#             # Ajoutez ici la gestion des compteurs ou d'autres actions en cas d'erreur
#         finally:
#             # Reprendre le traitement là où l'erreur s'est produite
#             print("reprise")
#         continue
#     exportRestos("postMAJDETAILS")

# def postResto():
#     resto = {
#         "name": "",
#         "address_str": "",
#         "published": false,
#         "GPS_address": null,
#         "video_links": [],
#         "phone_number": "",
#         "tags_id": [],
#         "placeId": null,
#         "ratings": 0,
#         "reviews": [],
#         "price": "",
#         "website_url": "",
#         "handicap": false,
#         "vege": false,
#         "schedule": [],
#         "picture_profile": "",
#         "number_of_reviews": 0
#     }




def majDetailsRestos(all_restaurants = get_all_restaurants()):
    print("METTRE A JOUR LES COLONNES DE RESTAURANT DANS LE CODE DUMP DE LA TABLE RESTAURANT EN COURS... y a-t-il eu des modifications faites sur les colonnes depuis le dernier dump?")
    exportRestos()
    time.sleep(3)
    max_attempts = 3  # Nombre maximal de tentatives
    for resto in all_restaurants:
        attempts = 0  # Initialiser le compteur de tentatives
        while attempts < max_attempts:
            try:
                details = getPlaceIdRequestDetails(resto)
                placeId = fetch_place_id(details[0], details[1], details[2])
                resto = update_place_id_for_resto(resto, placeId)
                print(resto)
                restoDetails = fetch_restaurant_details(placeId)
                resto = update_details_for_resto(resto, restoDetails)
                break  # Sortir de la boucle while si le traitement réussit
            except Exception as e:
                attempts += 1  # Incrémenter le compteur de tentatives
                print(f"Une erreur s'est produite lors du traitement du restaurant : {e}")
                time.sleep(20)
                if attempts == max_attempts:
                    print(f"Le traitement du restaurant a échoué après {max_attempts} tentatives.")
                    break
                else:
                    print("Tentative de retraitement...")
            else:
                # Si aucune exception n'est levée, sortir de la boucle while
                break
    exportRestos("postMAJDETAILS")



# Fonction pour effectuer la requête POST
# def send_post(data):
#     url = 'https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants'
#     headers = {'Content-Type': 'application/json'}
#     payload = {
#         "name": data['name'],
#         "address_str": data['address_str'],
#         "published": data['published'],
#         "GPS_address": data['GPS_address'],
#         "video_links": data['video_links'], #pb?
#         "phone_number": data['phone_number'],
#         "tags_id": data['tags_id'], #pb?
#         "placeId": data['placeId'],
#         "ratings": data['ratings'],
#         "reviews": data['reviews'],
#         "price": data['price'],
#         "website_url": data['website_url'],
#         "handicap": data['handicap'],
#         "vege": data['vege'],
#         "schedule": data['schedule'],
#         "picture_profile": data['picture_profile'],
#         "number_of_reviews": data['number_of_reviews']
#     }
#     response = requests.post(url, json=payload, headers=headers)
#     print(response.status_code)


    # print(data['name'])
    # print(data['address_str'])
    # print(ast.literal_eval(data['video_links']))
    # print(data['phone_number'])
    # print(ast.literal_eval(data['tags_id']))
    # print(data['placeId'])
    # print(int(data['ratings']))
    # print(ast.literal_eval(data['reviews']))
    # print(data['price'])
    # print(data['website_url'])
    # print(True if data['handicap'].lower() == 'true' else False)
    # print(True if data['vege'].lower() == 'true' else False)
    # print(ast.literal_eval(data['schedule']))
    # print(data['picture_profile'])
    # print(int(data['number_of_reviews']))

def send_post(data):
    url = 'https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants'
    headers = {'Content-Type': 'application/json'}

    gps_address_str = data['GPS_address']
    gps_address_dict = eval(gps_address_str)
    # Convertir le dictionnaire Python en objet JSON
    gps_address_json = json.dumps(gps_address_dict)

    # Conversion des valeurs booléennes et numériques
    published = True if data['published'].lower() == 'true' else False
    handicap = True if data['handicap'].lower() == 'true' else False
    vege = True if data['vege'].lower() == 'true' else False
    ratings = float(data['ratings'])
    number_of_reviews = int(data['number_of_reviews'])

    # Création du payload au format JSON
    payload = {
        "name": data['name'],
        "address_str": data['address_str'],
        "published": published,
        "GPS_address": gps_address_json,
        "video_links": ast.literal_eval(data['video_links']),
        "phone_number": data['phone_number'],
        "tags_id": ast.literal_eval(data['tags_id']),
        "placeId": data['placeId'],
        "ratings": ratings,
        "reviews": data['reviews'],
        "price": data['price'],
        "website_url": data['website_url'],
        "handicap": handicap,
        "vege": vege,
        "schedule": ast.literal_eval(data['schedule']),
        "picture_profile": data['picture_profile'],
        "number_of_reviews": number_of_reviews
    }

    print(payload)
    response = requests.post(url, json=payload, headers=headers)
    print("Response:", response.text)
    print(response.status_code)


def update_details_for_resto(resto, details):
    id = resto["id"]
    url = f"https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants/{id}"  # Remplacez cette URL par la vôtre
    headers = {
        'Content-Type': 'application/json',
    }

    ###
    print(details["reviews"])
    # reviews_dict = eval(details["reviews"])
    # print(reviews_dict)
    # reviews = json.dumps(reviews_dict)
    # print(reviews)
    ###

    data = {
        "id": id,
        # "restaurants_id": id,
        "name": resto["name"],
        "address_str": resto["address_str"],
        "published": resto["published"],
        "GPS_address": resto["GPS_address"],
        "video_links": resto["video_links"],
        "phone_number": resto["phone_number"],
        "tags_id": resto["tags_id"],
        "placeId": resto["placeId"],
        "ratings": details["ratings"],
        "price": details["price"],
        "website_url": details["website_url"],
        "handicap": details["handicap"],
        "vege": details["vege"],
        "schedule": details["schedule"], #
        "picture_profile": "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=" + details["picture_profile"] + f"&key={YOUR_GOOGLE_MAPS_API_KEY}", #https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=$photoReference&key=$apiKey
        "number_of_reviews": details["number_of_reviews"],
        "reviews": details["reviews"], #à décortiquer

    #     gps_address_str = data['GPS_address']
    # gps_address_dict = eval(gps_address_str)
    # # Convertir le dictionnaire Python en objet JSON
    # gps_address_json = json.dumps(gps_address_dict)


    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        return data
        print("PlaceId updated successfully.")
    else:
        print(f"Error updating placeId: {response.text}")


# Exemple d'utilisation
if __name__ == "__main__":
    # majDetailsRestos()

    # postrestos
    with open('restaurants_data2024-04-06_05postMAJDETAILS.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        i=0
        for row in reader:
            print(row)
            send_post(row)
            i+=1
            if(i==6):
                i=0
                time.sleep(20)

    #exportRestos()







