import pandas as pd
from bs4 import BeautifulSoup as BS
import requests, concurrent.futures
from operator import add



class Geospatial_Location_Webscraper:
    def __init__(self):
        super(Geospatial_Location_Webscraper, self).__init__()

    def URL_Generator (self, CSV_file):
        url = []
        addresses = pd.read_csv(CSV_file, delimiter=",")
        list_of_addresses = [x for x in addresses.values]


        for i in range(len(list_of_addresses)):
            url.append("https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=" + \
                list_of_addresses[i][1].replace(" ", "%20").replace("#", "%23").replace("'", "%27") + "%2C" + \
                list_of_addresses[i][2].replace(" ", "%20") + "&benchmark=4")

        return url, list_of_addresses

    def web_crawler(self, url, Target_Lat, Target_Long):

        self.userLat = Target_Lat
        self.userLong = Target_Long
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Start a thread for each URL
            future_to_url = {executor.submit(self.get_page, url[i], Target_Lat, Target_Long): url[i] for i in range(len(url))}
            for future in concurrent.futures.as_completed(future_to_url):
                i = url.index(future_to_url[future])
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (url[i], exc))
                else:
                    print('%r page is %d bytes' % (url[i], len(data)))

    def get_page(self, url, Target_Lat, Target_Long, list_of_addresses):


        list_of_x_coords = []
        list_of_y_coords = []
        diff_of_lat = []
        diff_of_long = []

        for i in range(20):
            page = requests.get(url[i])
            html_outlines = BS(page.content, "html.parser")
            coordinate = html_outlines.find_all("span")
            y_coord = coordinate[7:8]
            x_coord = coordinate[8:9]


        #checks if data returned from website is valid if not replaces it with 99.99999999
            if len(x_coord) == 0:
                x_coord = ["<span>99.99999999999999</span>"]
                y_coord = ["<span>99.99999999999999</span>"]
            list_x = [str(i) for i in x_coord]
            list_y = [str(i) for i in y_coord]

        #converts all the data from a website string into a float and stores in a list
            for x_c in list_x:
                list_of_x_coords.append(float(x_c[6:15]))
                diff_of_lat.append(Target_Lat - float(x_c[6:15]))
            for y_c in list_y:
                list_of_y_coords.append(float(y_c[6:16]))
                diff_of_long.append(Target_Long - float(y_c[6:16]))


        # calculates the closest lat and long to the target lat and long
        res1 = list(map(abs, diff_of_lat))
        res2 = list(map(abs, diff_of_long))
        res3 = list(map(add, res1, res2))
        res3.index(min(res3))
        index3 = res3.index(min(res3))



        # #creates a CSV file with all the x and y of the addresses given in CSV then returns desired target
        Lat_and_long = {"X": list_of_x_coords, "Y": list_of_y_coords}
        to_csv = pd.DataFrame(Lat_and_long)
        to_csv.to_csv("Coordinates.csv")
        return list_of_addresses[index3][:]




# webscraper = Geospatial_Location_Webscraper()
# urls, addresses = webscraper.URL_Generator('addresses.csv')
# webscraper.get_page(urls, 37.065984, -79.601172, addresses)
