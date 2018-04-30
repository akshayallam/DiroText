import json
import urllib.parse
import urllib.request

API_KEY = "AIzaSyBw6d8RlhagggAnA5D4E_tdfAtgNFA2dOI"

BASE_URL = "https://maps.googleapis.com/maps/api/directions/json?"


def build_search_url(origin, destination, mode) -> str:
    query_parameters = [("origin",origin),("destination", destination),("mode", mode),("key", API_KEY)]
    return BASE_URL + urllib.parse.urlencode(query_parameters)


def get_result(url: str) -> dict:
    '''
    Returns the json text that is formed by opening and reading the url.
    '''
    response = None
    try:
        response = urllib.request.urlopen(url)
        json_text = response.read().decode(encoding='utf-8')
        return json.loads(json_text)
    finally:
        if response != None:
            response.close()