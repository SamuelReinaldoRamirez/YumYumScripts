#on va target xanos et recup 10ids pars 10 ids les données de placeID des restos. Si dans le batch il manque des données, on regarde si il y a bien 10 resto qui ont été questionnés.
#si oui, alors on lance la requet pour récupérer les placeId à partir e nom et localisation.
# du coup on se retrouve avec 10 placeIds par 10 placeIds.

#en fait on va faire un script get placeId qu'on execute sur les ids de restos en questions quand les placesIds ne sont pas remplies#
#on parcours les placeidS avec les ids de resto correspondant et on requete places pour avoir les données de details

#puis on fait un post dans xano pour peupler la bdd

# https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants?_limit={batch_size}&_start={start_index}
# https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants?_limit=10&_start=0
import ast
from urllib.parse import quote

import requests
import time
import csv
import json
import datetime


xanoKey = 'LYxWamUX'
YOUR_GOOGLE_MAPS_API_KEY = 'AIzaSyBM05T0u8LoAKr2MtbTIjXtFmrU-06ye6U'

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


def get_all_restaurants():
    url = f"https://x8ki-letl-twmt.n7.xano.io/api:{xanoKey}/restaurantsBDD"
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

#EXPORT
def exportRestos(nameAppend=""):
    restos = get_all_restaurants()
    # Obtenir la date et l'heure actuelles
    maintenant = datetime.datetime.now()
    # Formater la date et l'heure dans un format approprié pour le nom de fichier
    nom_export = maintenant.strftime("%Y-%m-%d_%H")
    csv_filename = f"restaurants_data{nom_export}{nameAppend}.csv"
    print_cyan(list(restos[0].keys()))
    field_names = list(restos[0].keys())
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()
        for restaurant in restos:
            try:
                writer.writerow(restaurant)
            except Exception as e:
                print_red(f"Une erreur s'est produite lors de l'export : {e}")
    print_green(f"Les données ont été écrites dans le fichier CSV : {csv_filename}")

#PATCH PLACEID
def getPlaceIdRequestDetails(resto):
    return [resto["name"], resto["GPS_address"]["data"]["lat"], resto["GPS_address"]["data"]["lng"]]

def fetch_place_id(restaurant_name, latitude, longitude):
    encoded_name = quote(restaurant_name)
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={encoded_name}&location={latitude},{longitude}&radius=500&key={YOUR_GOOGLE_MAPS_API_KEY}"  # Remplacez YOUR_GOOGLE_MAPS_API_KEY par votre clé API Google Maps
    response = requests.get(url)
    data = response.json()
    if data.get('results'):
        placeidsQuiMatchLeNom = len(data["results"])
        print_gray(f"{placeidsQuiMatchLeNom} placeId retournés au lieu de 1")
        return data['results'][0]['place_id']
    print_gray(f"0 placeId retournés au lieu de 1")
    return None

def createDataPatchPlaceId(resto, place_id):
    data = {}
    for key, value in resto.items():
        data[key] = value
    data["placeId"] = place_id
    return data

def update_place_id_for_resto(resto, place_id):
    id = resto["id"]
    url = f"https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants/{id}"  # Remplacez cette URL par la vôtre
    headers = {
        'Content-Type': 'application/json',
    }
    data = createDataPatchPlaceId(resto, place_id)
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print_green(resto["name"])
        print_green("update_place_id_for_resto PlaceId updated successfully.")
        return data
    else:
        print_red(resto["name"])
        print_red(f"update_place_id_for_resto Error updating placeId: {response.text}")
        raise requests.RequestException("probleme dans le patch PLACE ID de " + resto["name"])
        # return resto

#PATCH RESTAURANTS DETAILS
def fetch_restaurant_details(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={YOUR_GOOGLE_MAPS_API_KEY}"  # Remplacez YOUR_GOOGLE_MAPS_API_KEY par votre clé API Google Maps
    print_magenta(""+url)
    response = requests.get(url)
    data = response.json()
    result = data.get('result', {})
    if 'current_opening_hours' in result:
        schedule = result["current_opening_hours"].get('weekday_text', [])
    else:
        print_underline_green("l'url " + url + " ne connait pas de current_opening_hours")
        schedule = []

    result_utile = {
        "ratings": result.get('rating', None),
        "price": result.get('price_level', None),
        "website_url": result.get('website', ''),
        "handicap": result.get('wheelchair_accessible_entrance', False),
        "vege": result.get('serves_vegetarian_food', False),
        "schedule": schedule,
        "picture_profile": result["photos"][0].get('photo_reference', ''),
        "number_of_reviews": result.get("user_ratings_total", None),
        "reviews": result.get('reviews', [])
    }
    return result_utile

def mapReviews(bddFormat, tabDataFromMaps):
    tabBddFormatedDataFromMaps = []
    for dataFromMaps in tabDataFromMaps:
        # Initialisation des champs avec des valeurs vides ou nulles
        bddFormatedDataFromMaps = {
            "author": dataFromMaps.get("author_name", ""),
            "text": dataFromMaps.get("text", ""),
            "rating": dataFromMaps.get("rating", None),
            "date_published": None,
            "author_profile_url": dataFromMaps.get("author_url", ""),
            "lang": dataFromMaps.get("original_language", "")
        }
        # Convertir le timestamp en une date lisible par un humain
        timestamp = dataFromMaps.get("time", None)
        if timestamp:
            date_published = datetime.datetime.fromtimestamp(timestamp)
            bddFormatedDataFromMaps["date_published"] = date_published.strftime("%Y-%m-%d %H:%M:%S")
        tabBddFormatedDataFromMaps.append(bddFormatedDataFromMaps)

        extra_keys = set(bddFormat) - set(bddFormatedDataFromMaps.keys())
        if(len(extra_keys)>0):
            print_red(f"les champs de reviews qui sont actuellement laissés vides sont :{extra_keys}")

    return tabBddFormatedDataFromMaps

def createDataPatchDetails(resto, details):
    data = {}
    for key, value in resto.items():
        data[key] = value
    data["ratings"] = details["ratings"]
    data["price"] = details["price"]
    data["website_url"] = details["website_url"]
    data["handicap"] = details["handicap"]
    data["vege"] = details["vege"]
    data["schedule"] = details["schedule"]
    data["picture_profile"] = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=" + details["picture_profile"] + f"&key={YOUR_GOOGLE_MAPS_API_KEY}"
    data["number_of_reviews"] = details["number_of_reviews"]
    data["reviews"] = mapReviews(resto["reviews"][0].keys(), details["reviews"])
    return data


def update_details_for_resto(resto, details):
    id = resto["id"]
    url = f"https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants/{id}"  # Remplacez cette URL par la vôtre
    headers = {
        'Content-Type': 'application/json',
    }
    data = createDataPatchDetails(resto,details)
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print_green("details updated successfully.")
        return response.json()
    else:
        print_red(f"Error updating details: {response.text}")
        raise requests.RequestException("probleme dans le patch de DETAILS " + resto["name"])

#DUMP-PATCH PLACEID-PATCHDETAILS-DUMP
def majDetailsRestos(all_restaurants = get_all_restaurants()):
    print_red("METTRE A JOUR LES COLONNES DE RESTAURANT DANS LE CODE DUMP DE LA TABLE RESTAURANT EN COURS... y a-t-il eu des modifications faites sur les colonnes depuis le dernier dump?")
    exportRestos()
    time.sleep(3)
    max_attempts = 3  # Nombre maximal de tentatives
    for resto in all_restaurants:
        #LIGNE A RETIRER
        resto["cuisine_id"] = 18
        attempts = 0  # Initialiser le compteur de tentatives
        while attempts < max_attempts:
            try:
                print('------------------------------------')
                print("resto")
                print(resto)
                placeIdDetails = getPlaceIdRequestDetails(resto)
                placeId = fetch_place_id(placeIdDetails[0], placeIdDetails[1], placeIdDetails[2])
                resto = update_place_id_for_resto(resto, placeId)
                restoDetails = fetch_restaurant_details(placeId)
                resto = update_details_for_resto(resto, restoDetails)
                print_bold_red(resto)
                break  # Sortir de la boucle while si le traitement réussit
            except Exception as e:
                attempts += 1  # Incrémenter le compteur de tentatives
                print_red(f"Une erreur s'est produite lors du traitement du restaurant : {e}")
                time.sleep(20)
                if attempts == max_attempts:
                    print_red(f"Le traitement du restaurant a échoué après {max_attempts} tentatives.")
                    break
                else:
                    print("Tentative de retraitement...")
            else:
                # Si aucune exception n'est levée, sortir de la boucle while
                break
    exportRestos("postMAJDETAILS")


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
    print_blue(payload)
    print_blue("arreter d'utiliser le payload en dur")
    response = requests.post(url, json=payload, headers=headers)
    print("Response:", response.text)
    print(response.status_code)

if __name__ == "__main__":
    majDetailsRestos()

    # postrestos
    # with open('restaurants_data2024-04-06_05postMAJDETAILS.csv', newline='', encoding='utf-8') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     i=0
    #     for row in reader:
    #         print(row)
    #         send_post(row)
    #         i+=1
    #         if(i==6):
    #             i=0
    #             time.sleep(20)


    #exportRestos()







