from geopy.geocoders import Nominatim
from geopy import distance
import threading
import time

closecities = []
is_done = False
start_time = False
# find the cities within 20 miles of the location entered

def currentlyClose(location):
    global is_done,start_time
    try:
        # Prompt user for zip code or city name
        print("finding cities close to: {}".format(location))
        with open('cities.txt', 'r') as file:
            cities = file.read().splitlines()
        # Prompt user for zip code or city name
        start_time = True
        # Geocode location using Nominatim
        geolocator = Nominatim(user_agent="my_app")
        location_coords = geolocator.geocode(location, exactly_one=True).point

        # Find cities within 20 miles of location
        nearby_cities = []
        for city in cities:
            city_coords = geolocator.geocode(city, exactly_one=True).point
            if distance.distance(location_coords, city_coords).miles <= 20:
                nearby_cities.append(city)

        # Print out nearby cities
        print("Cities within 20 miles of {}:".format(location))
        for city in nearby_cities:
            closecities.append(city)
        is_done = True
    except Exception as e:
        print(e)

def print_time():
    seconds = 0
    while not is_done:
        if start_time:
            print("Running timer : {}  seconds - ".format(seconds), end="\r")
            seconds += 1
            time.sleep(1)

def currentlyCloseWithTimer(location):
    timer_thread = threading.Thread(target=print_time)
    timer_thread.start()
    currentlyClose(location)
    timer_thread.join()




def checkCache(location):
    with open('closecities.txt', 'r') as file:
        lines = file.read().splitlines()
        try:
            zip_index = lines.index(location)
            cities = []
            for i in range(zip_index + 1, len(lines)):
                if lines[i].startswith("--"):
                    break
                cities.append(lines[i])
            return cities
        except ValueError:
            return False


def saveCache(location, cities):
    with open('closecities.txt', 'a') as file:
        file.write(location + "\n")
        for city in cities:
            file.write(city + "\n")


def searching():
    location = input("Enter zip code or city name: ")
    if location == "":
        location = "New York"

    _request_ = checkCache(f"-- {location}")
    if _request_ == False:
        currentlyCloseWithTimer(location)
        saveCache(f"-- {location}", closecities)
    else:
        print(_request_)
        exit()


