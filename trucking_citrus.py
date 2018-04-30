import json
import urllib.parse
import urllib.request

app_id = "RFW0VSeRRPzRWrihDITl"
app_code = "Nzas-QWvz4cXIDP9jKsNJw"

BASE_URL = "https://route.cit.api.here.com/routing/7.2/calculateroute.json?"


def build_geo_url(address) -> str:
    geo_base_url = "https://geocoder.cit.api.here.com/6.2/geocode.json?"
    query_parameters = [("app_id",app_id),("app_code", app_code),("searchtext", address)]
    return geo_base_url + urllib.parse.urlencode(query_parameters)

def build_search_url(origin, destination, weight, height) -> str:

    query_parameters1 = [("app_id",app_id),("app_code", app_code)]
    query_parameters2 = "&waypoint0=geo!{origin}&waypoint1=geo!{destination}&mode=fastest;truck;traffic:disabled&".\
    format(origin = origin,destination = destination)
    query_parameters3 = [("limitedWeight",weight),("height", height)]
    return BASE_URL + urllib.parse.urlencode(query_parameters1) + query_parameters2 + urllib.parse.urlencode(query_parameters3)


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