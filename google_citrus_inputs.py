import google_citrus
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
        return ' '.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def show(json_text: dict) -> None:
    steps = []

    for step_num,step in enumerate(json_text["routes"][0]["legs"][0]["steps"]):
        steps.append("Step {}) ".format(step_num+1) +  strip_tags(step["html_instructions"]).replace("  "," ") + "\nDistance: " + \
        step["distance"]["text"] + "\n")

    distance = strip_tags(json_text["routes"][0]["legs"][0]["distance"]["text"])
    time = strip_tags(json_text["routes"][0]["legs"][0]["duration"]["text"])
    steps.append("This trip takes {distance} and {time}.\n".format(distance = distance, time = time))

    steps.append("SMS Service Courtesy of Twilio\nDirections Courtesy of Google Maps Directions API")
    return "\n".join(steps)

def main(origin, destination, mode):
    '''
    Runs the entire program.
    '''

    url = google_citrus.build_search_url(origin,destination,mode)
    json_text = google_citrus.get_result(url)
    return show(json_text)

