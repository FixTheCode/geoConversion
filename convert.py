# -----------------------------------------------------------
# converts Google location history data to csv file
#
# https://github.com/FixTheCode CC0 1.0 Universal
# -----------------------------------------------------------
import argparse
import json
import csv
import math
from datetime import datetime

# identifiers in Google location history file.
# timestampMs is milliseconds since 1970. see https://www.epochconverter.com/
# latitude and longitude are decimal degrees without the decimal point
GOOGLE_LOCATIONS = "locations"
GOOGLE_TIMESTAMP = "timestampMs"
GOOGLE_LATITUTE = "latitudeE7"
GOOGLE_LONGITUDE = "longitudeE7"

parser = argparse.ArgumentParser(
    description="Convert Google Maps location history to CSV file."
)
parser.add_argument("-i", "--input", help="Location history .json file.", required=True)
parser.add_argument("-o", "--output", help="Output.csv file.", required=True)
parser.add_argument("-x", "--header", help="Include header row", required=False)
args = parser.parse_args()

# open location history file
file = open(args.input)
data = json.load(file)

locations = data[GOOGLE_LOCATIONS]
with open(args.output, "w") as csvfile:
    output = csv.writer(csvfile, delimiter=",")
    if args.header:
        output.writerow(["timestamp", "latitude", "longitude"])

    for l, location in enumerate(locations):
        output.writerow(
            [
                str(datetime.utcfromtimestamp(int(location[GOOGLE_TIMESTAMP]) / 1000).strftime('%Y-%m-%d %H:%M:%S')),
                float(location[GOOGLE_LATITUTE]) / math.pow(10, 7),
                float(location[GOOGLE_LONGITUDE]) / math.pow(10, 7),
            ]
        )

print(str(len(locations)) + " locations extracted to", args.output)
