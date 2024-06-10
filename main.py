# faire passer chaque resto qui merde 1 par 1 pour trouver une strat ; peut etre en ayant recours à d'autres endpoint donc :'
# mieux étudier l'api maps
# script pour update toutes les colones schedules histoire d'avoir des intervalles plus propres
# stocker toutes les photos sur xano et faire un script pour maj cette colone

# https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants?_limit={batch_size}&_start={start_index}
# https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants?_limit=10&_start=0

#dev :
# https://x8ki-letl-twmt.n7.xano.io/api:_q8oxfAF/restaurants
import ast
from urllib.parse import quote

import requests
import time
import csv
import json
import datetime

dev = False
prod = True
xanoKeyDev = '_q8oxfAF'
xanoKey = 'LYxWamUX'
YOUR_GOOGLE_MAPS_API_KEY = 'AIzaSyBM05T0u8LoAKr2MtbTIjXtFmrU-06ye6U'
templateBDDReviews = {'author': 'Monica Rivera', 'text': 'Everything was delicious! Ramen was amazing with lots of flavors. The veggie gyozas as appetizers were tasty too. Nice variety of desserts and I really recommend the matcha financiers with ginger ice cream. Nice wine by the glass as well. Very cozy venue and ambience. A must!', 'rating': '5', 'date_published': 1675549566000, 'author_profile_url': 'https://www.google.com/maps/contrib/107074390665313624214/reviews', 'lang': 'en'}
templateBDDResto = {'id': 127, 'created_at': 1712447719120, 'placeId': 'ChIJt9VeXGRv5kcRA7kQ-xGju00', 'ratings': 3.1, 'name': 'Bambini', 'cuisine_id': 16, 'address_str': '13 Av. du Président Wilson, 75116 Paris', 'published': True, 'video_links': ['https://res.cloudinary.com/di65pb1aa/video/upload/v1710869614/edkqdkpapaabv3zsowpr.mp4', 'https://res.cloudinary.com/di65pb1aa/video/upload/v1710869627/lwgau3bufxnnzcbgxnei.mp4', 'https://res.cloudinary.com/di65pb1aa/video/upload/v1710869644/vpclikcbmkumwjbim1mq.mp4'], 'phone_number': '01 40 70 86 08', 'tags_id': [6, 5], 'price': '', 'website_url': 'https://bambini-restaurant.com/?utm_source=Yext&utm_medium=GMB&y_source=1_MjU3NjI3ODctNzE1LWxvY2F0aW9uLndlYnNpdGU%3D', 'handicap': True, 'vege': False, 'schedule': ['Monday: 12:00\u2009–\u20093:00\u202fPM, 7:00\u2009–\u200911:00\u202fPM', 'Tuesday: 12:00\u2009–\u20093:00\u202fPM, 7:00\u2009–\u200911:00\u202fPM', 'Wednesday: 12:00\u2009–\u20093:00\u202fPM, 7:00\u2009–\u200911:00\u202fPM', 'Thursday: 12:00\u2009–\u20093:00\u202fPM, 7:00\u2009–\u200911:00\u202fPM', 'Friday: 12:00\u2009–\u20093:00\u202fPM, 7:00\u2009–\u200911:00\u202fPM', 'Saturday: 12:00\u2009–\u20093:00\u202fPM, 7:00\u2009–\u200911:00\u202fPM', 'Sunday: 12:00\u2009–\u20093:00\u202fPM, 7:00\u2009–\u200911:00\u202fPM'], 'picture_profile': 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=ATplDJb2fDU4cHtEOuJ_ZZ8mF-k5xnJJXnE4M3w3ZLLgPKR5xjnd71DKrngQC7O68pgNj5Z3Xa_NH9kGRdsHMUEOLdOjo0cEu5IntAQ7rbApQ39pCn2bOewMoyFYy7VNP8ov2gXiNKGbESi_A32A_z3Ifgm6UzFrwGl3pIsR4w6FfWhoZ1M&key=AIzaSyBM05T0u8LoAKr2MtbTIjXtFmrU-06ye6U', 'number_of_reviews': 1839, 'GPS_address': {'type': 'point', 'data': {'lng': 2.288553, 'lat': 48.863029}}, 'reviews': [{'author': 'Mariana Petriyenko', 'text': 'Had an amazing experience here. I don’t get why there any bad reviews. The food was actually AMAZING, so fresh and so good & we tried a variety of different dishes.The vibes were 10/10, service was 10/10 and the live music was beautiful. The only thing is that you can’t see the Eiffel Tower from most of the tables, only a few in a small corner offer those views for dinner. But that didn’t take away from our experience at all. We’ll definitely be back here, loved it!', 'rating': '5', 'date_published': 1708731927000, 'author_profile_url': 'https://www.google.com/maps/contrib/117735846416187591998/reviews', 'lang': 'en'}, {'author': 'Catalina', 'text': 'The hype is real! Fantastic ambience and service. Live music and great food! The restaurant is beautiful, they have nice servers and talented artists performing. We had also a nice Eiffel Tower view. I enjoyed this place a lot. I’m picky with my Italian food, specially with tiramisù (I’d suggest to share it, it’s a huge portion for a single person). I will definitely come back!', 'rating': '5', 'date_published': 1709928721000, 'author_profile_url': 'https://www.google.com/maps/contrib/109433353881580968763/reviews', 'lang': 'en'}, {'author': 'Fearn Short', 'text': 'Last minute reservation made after seeing this restaurant recommend on tiktok. The pizza was big and filling, the decor and room was nice but was very pricey. Little attentions to detail such as the branded ice cube was nice. Seems to be an influencers heaven with girls taking photos with large LED lights throughout the whole night.', 'rating': '3', 'date_published': 1708543276000, 'author_profile_url': 'https://www.google.com/maps/contrib/110616714457220341512/reviews', 'lang': 'en'}, {'author': 'Misha K.', 'text': "I had higher expectations from this restaurant. The service was unfriendly; the waitress kept mentioning how expensive it was, which I found inappropriate. A server shouldn't judge patrons based on perceived affordability; politeness should be universal. It felt like she'd only be kind if she thought you'd leave a big tip. Additionally, the food wasn't tasty.", 'rating': '1', 'date_published': 1711633622000, 'author_profile_url': 'https://www.google.com/maps/contrib/118067884813947705471/reviews', 'lang': 'en'}, {'author': 'Maria emilia Alonzo', 'text': 'Very nice place, views and service. The best apperol spritz in paris by far and the green bean salad is a must. The food is pretty good but a bit overpriced in my opinion. Would definitely recommend for a one time ocasion.', 'rating': '5', 'date_published': 1702731182000, 'author_profile_url': 'https://www.google.com/maps/contrib/108632796295708644587/reviews', 'lang': 'en'}]}

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
    url=''
    if(dev):
        url = f"https://x8ki-letl-twmt.n7.xano.io/api:{xanoKeyDev}/restaurants"
    else: #if prod
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
    if dev:
        nameAppend += " - DEV"
    else:
        nameAppend += " - PROD"
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

def fetch_place_id(restaurant_name, latitude, longitude, radius=100):
    print_red(radius)
    # encoded_name = quote(restaurant_name.replace(' ', ''))
    encoded_name = quote(restaurant_name)
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={encoded_name}&location={latitude},{longitude}&radius={radius}&key={YOUR_GOOGLE_MAPS_API_KEY}"  # Remplacez YOUR_GOOGLE_MAPS_API_KEY par votre clé API Google Maps
    print_red(url)
    response = requests.get(url)
    data = response.json()
    print(data)
    if data.get('results'):
        placeidsQuiMatchLeNom = len(data["results"])
        print_magenta(f"{placeidsQuiMatchLeNom} placeId retournés au lieu de 1")
        if(placeidsQuiMatchLeNom >1 ):
            print_magenta("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            # return fetch_place_id(restaurant_name.replace(' ', ''), latitude, longitude, radius//2)
            for dato in data["results"]:
                print(f"https://maps.googleapis.com/maps/api/place/details/json?place_id=" + dato["place_id"] + f"&fields=name,types,current_opening_hours&key={YOUR_GOOGLE_MAPS_API_KEY}")
        # return data['results'][0]['place_id']
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
    if(dev):
        url = f"https://x8ki-letl-twmt.n7.xano.io/api:{xanoKeyDev}/restaurants/{id}"
    else: #if prod
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
    try:
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
    except Exception as e:
        print_red("fetch_restaurant_details ERROR")
        raise e

def mapReviews(bddFormat, tabDataFromMaps):
    print_blue(bddFormat)
    print_blue(tabDataFromMaps)
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
    data["reviews"] = mapReviews(templateBDDReviews, details["reviews"])
    return data


def update_details_for_resto(resto, details):
    try:
        id = resto["id"]
        if dev:
            url = f"https://x8ki-letl-twmt.n7.xano.io/api:{xanoKeyDev}/restaurants/{id}"
        else:
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
    except Exception as e:
        print_red("update_details_for_resto ERROR")
        raise e

#DUMP-PATCH PLACEID-PATCHDETAILS-DUMP
def majDetailsRestos(all_restaurants = get_all_restaurants()):
    print_red("METTRE A JOUR LES COLONNES DE RESTAURANT DANS LE CODE DUMP DE LA TABLE RESTAURANT EN COURS... y a-t-il eu des modifications faites sur les colonnes depuis le dernier dump?")
    exportRestos()
    time.sleep(3)
    max_attempts = 3  # Nombre maximal de tentatives
    for resto in all_restaurants:
        # #LIGNE A RETIRER
        # resto["cuisine_id"] = 18
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


def convert_string_to_list(input_string):
    print_magenta(input_string)
    try:
        # Essayer d'évaluer la chaîne d'entrée comme une expression Python
        evaluated_value = ast.literal_eval(input_string)

        # Si la valeur évaluée est une liste, retourner cette liste
        if isinstance(evaluated_value, list):
            print_bold_red(evaluated_value)
            return evaluated_value
        # Sinon, retourner la valeur évaluée elle-même
        else:
            print_cyan(evaluated_value)
            return evaluated_value
    except (SyntaxError, ValueError):
        print_magenta(input_string)
        # Si une erreur se produit lors de l'évaluation, retourner la chaîne d'entrée telle quelle
        return input_string


def createDataPostResto(row, restoFormat=templateBDDResto):
    data = {}
    print_blue(row)
    print_red(restoFormat)
    for key, value in restoFormat.items():
        print_underline_green(key)
        print(row[key])
        data[key] = convert_string_to_list(row[key])
    # gps_address_str = row['GPS_address']
    # gps_address_dict = eval(gps_address_str)
    # # Convertir le dictionnaire Python en objet JSON
    # data["GPS_address"] = json.dumps(gps_address_dict)
    return data

def send_post(data):
    if dev:
        url = f'https://x8ki-letl-twmt.n7.xano.io/api:{xanoKeyDev}/restaurants'
    else:
        url = 'https://x8ki-letl-twmt.n7.xano.io/api:LYxWamUX/restaurants'
    headers = {'Content-Type': 'application/json'}
    payload=createDataPostResto(data)
    print_blue(payload)
    print_blue(payload["tags_id"])
    if(payload!={}):
        response = requests.post(url, json=payload, headers=headers)
        print("Response:", response.text)
        print(response.status_code)
        toReturn = response.json()
    else:
        # response.text="le payload ne peut pas etre vide"
        # response.status_code="400"
        print("todo")
        toReturn = "reponse vide"
    return toReturn


#   input_schedule = {
#   "Monday": ["Closed"],
#   "Tuesday": ["7:00 PM  - 3:00 AM"],
#   "Wednesday": ["3:00 AM  - 11:00 PM"],
#   "Thursday": ["11:00 AM - 2:30 AM"],
#   "Friday": ["7:00 PM - 9:00 PM"],
#   "Saturday": ["Closed"],
#   "Sunday": ["7:00 PM  - 2:00 AM"]
#     }
#
#     expected_output = {
#         "Monday": ["0:00 AM - 2:00 AM"],
#         "Tuesday": ["7:00 PM - 11:59 PM"],
#         "Wednesday": ["0:00 AM - 11:00 PM"],
#         "Thursday": ["11:00 AM - 11:59 PM"],
#         "Friday": ["0:00 AM - 2:30 AM", "7:00 PM - 9:00 PM"],
#         "Saturday": ["Closed"],
#         "Sunday": ["7:00 PM - 2:00 AM"]
#     }
# ben non c'est faux... oyons les jours ainsi :
# lundi : jour 0
# mardi :2
# mer : 3
# jeu : 4
# ven : 5
# sam : 6
# dim : 7

# la regles pour modifier le planning est ainsi :
# -si au jour N , le planning depasse apres minuit, on enleve ce temps du planning du jour N et on l'ajoute au planning du jour N+1
# -lundi est le jour N+1 par rapport à dimanche.
# - si en ajoutant les heures au planning du jour N+1, on se rends compte que la plage horaire que l'on comptait ajouter finit au moment où la place horaire qui était déjà là commence, alors on fusionne les 2 plages horaires ensemble.
def transform_schedule(input_schedule):
    def get_next_day(day):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        next_index = (days.index(day) + 1) % 7
        return days[next_index]

    def format_time(time_str):
        # Nettoyer la chaîne de caractères pour supprimer les espaces insécables
        time_str = time_str.replace(" ", " ")
        cleaned_time = datetime.datetime.strptime(time_str, "%I:%M %p").strftime("%I:%M %p")
        print("Cleaned time:", cleaned_time)
        return cleaned_time

    def merge_times(times):
        merged_times = []
        for time_range in times:
            if not merged_times or time_range[0] > merged_times[-1][1]:
                merged_times.append(time_range)
            else:
                # Fusionner les plages horaires en mettant à jour la fin de la plage horaire précédente
                merged_times[-1] = (merged_times[-1][0], max(merged_times[-1][1], time_range[1]))
        return merged_times

    output_schedule = {}

    for day, times in input_schedule.items():
        print("Processing day:", day)
        if times == ["Closed"]:
            output_schedule[day] = ["Closed"]
            print("Day is closed.")
            continue

        formatted_times = []
        for time_str in times:
            start_time, end_time = time_str.split(" - ")
            start_time = format_time(start_time)
            end_time = format_time(end_time)

            if end_time < start_time:
                next_day = get_next_day(day)
                print("Time range crosses midnight. Next day:", next_day)
                # Ajouter la partie de la plage horaire pour le jour actuel
                formatted_times.append((start_time, "11:59 PM"))
                # Calculer le temps restant après minuit
                remaining_time = datetime.datetime.strptime("11:59 PM", "%I:%M %p") - datetime.datetime.strptime("12:00 AM", "%I:%M %p")
                # Ajouter le reste de la plage horaire pour le jour suivant avec l'ajustement
                output_schedule[next_day] = output_schedule.get(next_day, []) + [("12:00 AM", (datetime.datetime.strptime(end_time, "%I:%M %p") + remaining_time).strftime("%I:%M %p"))]
            else:
                formatted_times.append((start_time, end_time))

        print("Before sorting and merging:", formatted_times)

        formatted_times.sort()
        merged_times = merge_times(formatted_times)

        print("After sorting and merging:", merged_times)

        output_schedule[day] = [f"{start} - {end}" for start, end in merged_times]

    return output_schedule

if __name__ == "__main__":

    all_restaurants = get_all_restaurants()
    resto1 = all_restaurants[0]
    placeIdDetails = getPlaceIdRequestDetails(resto1)
    print(placeIdDetails)
    placeId = fetch_place_id(placeIdDetails[0], placeIdDetails[1], placeIdDetails[2])
    print(placeId)


    # # exportRestos(" - AWSVideoLinks")
    #
    # # postrestos
    # with open('outputttt.csv', newline='', encoding='utf-8') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     i=0
    #     for row in reader:
    #         print(row)
    #         # send_post(row)
    #         print_inverse_yellow(send_post(row))
    #         i+=1
    #         if(i==6):
    #             i=0
    #             time.sleep(20)







    # # Test de la fonction
    # input_schedule = {
    #     "Monday": ["Closed"],
    #     "Tuesday": ["7:00 PM - 3:00 AM"],
    #     "Wednesday": ["3:00 AM - 11:00 PM"],
    #     "Thursday": ["11:00 AM - 2:30 AM"],
    #     "Friday": ["7:00 PM - 9:00 PM"],
    #     "Saturday": ["Closed"],
    #     "Sunday": ["7:00 PM - 2:00 AM"]
    # }
    #
    # expected_output = {
    #     "Monday": ["0:00 AM - 2:00 AM"],
    #     "Tuesday": ["7:00 PM - 11:59 PM"],
    #     "Wednesday": ["0:00 AM - 11:00 PM"],
    #     "Thursday": ["11:00 AM - 11:59 PM"],
    #     "Friday": ["0:00 AM - 2:30 AM", "7:00 PM - 9:00 PM"],
    #     "Saturday": ["Closed"],
    #     "Sunday": ["7:00 PM - 2:00 AM"]
    # }
    #
    # print(transform_schedule(input_schedule) == expected_output)


# if __name__ == "__main__":
#     # majDetailsRestos()
#
#     # exportRestos(" - photos maps")
#
#     # postrestos
#     with open('dumpPhotosXano.csv', newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         i=0
#         for row in reader:
#             print(row)
#             # send_post(row)
#             print_inverse_yellow(send_post(row))
#             i+=1
#             if(i==6):
#                 i=0
#                 time.sleep(20)
#
#     exportRestos(" - photos xano")







