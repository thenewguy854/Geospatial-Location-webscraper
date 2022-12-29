import pandas as pd
from bs4 import BeautifulSoup as BS
import requests
import csv

Target_Lat, Target_Log = 37.065984, -79.601172

addresses = pd.read_csv('addresses.csv', delimiter=",")
list_of_addresses = [x for x in addresses.values]

# Bellow creates all the URLs to check the address in the given CSV
length = len(list_of_addresses)
list_of_x_coords = []
list_of_y_coords = []
for i in range(length):
    url = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=" + \
          list_of_addresses[i][1].replace(" ", "%20").replace("#", "%23").replace("'", "%27") + "%2C" + \
          list_of_addresses[i][2].replace(" ", "%") + "&benchmark=4"

    page = requests.get(url)
    html_outlines = BS(page.content, "html.parser")

    coordinate = html_outlines.find_all("span")

    y_coord = coordinate[7:8]
    x_coord = coordinate[8:9]
    list_x = [str(i) for i in x_coord]
    list_y = [str(i) for i in y_coord]
    for x_c in list_x:
        list_of_x_coords.append(float(x_c[6:15]))
        # to_csv = pd.DataFrame(list_of_x_coords)
        # to_csv.to_csv("Coordinates.csv")
        for y_c in list_y:
            list_of_y_coords.append(float(y_c[6:16]))



Lat_and_long = {"X": list_of_x_coords, "Y": list_of_y_coords}
print(Lat_and_long)
to_csv = pd.DataFrame(Lat_and_long)
to_csv.to_csv("Coordinates.csv")






# line 922 in csv is answer 37.068364, -79.681218, 0.00238, 0.080046 Richard Howe,90 Journeys End Dr,Wirtz
