import pandas as pd
import requests
import os

class Geospatial_Location_Webscraper:
    def __init__(self):
        super(Geospatial_Location_Webscraper, self).__init__()

    def submit_batch_csv(self, input_csv_filename, output_csv_filename):
        # Ensure the output file exists, create it if not
        if not os.path.exists(output_csv_filename):
            open(output_csv_filename, 'wb').close()

        # The endpoint for batch geocoding
        url = "https://geocoding.geo.census.gov/geocoder/locations/addressbatch"

        # Open the CSV file and submit it to the geocoding service
        with open(input_csv_filename, 'rb') as file:
            # The 'files' parameter takes a dictionary with the form field name and the file object
            files = {'addressFile': (input_csv_filename, file)}
            # The 'payload' can include additional parameters such as benchmark and vintage
            payload = {'benchmark': 'Public_AR_Census2020', 'vintage': 'Census2020_Census2020'}
            response = requests.post(url, files=files, data=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Write the response content to the output CSV file
            with open(output_csv_filename, 'wb') as output_file:
                output_file.write(response.content)


    def process_geocoded_results(self, input_csv, output_csv):
        # Read the CSV file, ensuring all data is read as string type
        df = pd.read_csv(input_csv, header=None, dtype=str, quotechar='"')

        # Define a new DataFrame to hold processed data
        processed_df = pd.DataFrame()

        def parse_coord(coord):
            if pd.isna(coord) or coord.strip() == '':
                return '00.00000000000000'
            else:
                return coord.strip()

        # Extract index, latitude, and longitude
        processed_df['Index'] = df[0].astype(int)  # Convert index to integer for sorting
        processed_df['Latitude'] = df[5].str.split(',', expand=True)[1].apply(parse_coord)
        processed_df['Longitude'] = df[5].str.split(',', expand=True)[0].apply(parse_coord)

        # Sort the DataFrame by the index
        processed_df.sort_values(by='Index', inplace=True)

        # Save the sorted and processed data to a new CSV file
        processed_df.to_csv(output_csv, index=False, header=True)


    def calculate_closest_address_to_target(self, geocoded_csv, addresses_csv, TargetLat, TargetLong):
        # Read the sorted geocoded results and addresses
        geocoded_df = pd.read_csv(geocoded_csv)
        addresses_df = pd.read_csv(addresses_csv, header=None, names=['Name', 'Address', 'City'])

        # Calculate the distance to the target for each coordinate
        geocoded_df['Distance'] = ((geocoded_df['Latitude'] - TargetLat) ** 2 + (geocoded_df['Longitude'] - TargetLong) ** 2) ** 0.5

        # Find the index of the closest address
        closest_index = geocoded_df['Distance'].idxmin()
        closest_geocoded_index = geocoded_df.loc[closest_index, 'Index']

        # Find the corresponding address in addresses_df
        closest_address = addresses_df.iloc[closest_geocoded_index - 1]  # assuming the CSV index starts from 1

        # Return the closest address details
        return closest_address




# optimized from 23:43 down to 18 seconds