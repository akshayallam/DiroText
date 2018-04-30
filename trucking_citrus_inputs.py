import trucking_citrus
import sys
from html.parser import HTMLParser


# https://stackoverflow.com/questions/11061058/using-htmlparser-in-python-3-2
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def geo_show(json_text):
    latitude = json_text["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]["Latitude"]
    longitude = json_text["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]["Longitude"]
    return str(latitude) + "," + str(longitude)


def routing_show(json_text):
    steps = []

    for step_num, step in enumerate(json_text["response"]["route"][0]["leg"][0]["maneuver"]):
        steps.append("Step {}) ".format(step_num + 1) + strip_tags(step["instruction"]) + "\n")

    steps.append(strip_tags(json_text["response"]["route"][0]["summary"]["text"]) + "\n")

    steps.append("SMS Service Courtesy of Twilio\nDirections Courtesy of HERE Routing API and HERE Geocoder API ")
    return "\n".join(steps)


def main(starting_address, destination_address, weight, height):

    starting_url = trucking_citrus.build_geo_url(starting_address)
    destination_url = trucking_citrus.build_geo_url(destination_address)

    starting_json_text = trucking_citrus.get_result(starting_url)
    destination_json_text = trucking_citrus.get_result(destination_url)

    starting_coord = geo_show(starting_json_text)
    destination_coord = geo_show(destination_json_text)

    routing_url = trucking_citrus.build_search_url(starting_coord, destination_coord, weight, height)
    routing_json_text = trucking_citrus.get_result(routing_url)

    return routing_show(routing_json_text)