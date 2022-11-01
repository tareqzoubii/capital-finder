from http.server import BaseHTTPRequestHandler
# from datetime import datetime
from urllib import parse
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        the_path = self.path
        url_components = parse.urlsplit(the_path)
        print(url_components)
        query_list = parse.parse_qsl(url_components.query)
        dictionary = dict(query_list)
        
        # send request to API
        if 'capital' in dictionary:
            capital = dictionary['capital'] # saving to query
            url ='https://restcountries.com/v3.1/capital/'
            r = requests.get(url+capital)
            data = r.json() # to form json!
            print(data)
            country = data[0]['name']['common']
            message = f"{dictionary['capital']} is the capital of {country}"
        
        elif 'country' in dictionary:
            country = dictionary['country']
            url = 'https://restcountries.com/v3.1/name/'
            r = requests.get(url + country)
            data = r.json()
            capital = data[0]['capital'][0]
            message = f"The capital of {dictionary['country']} is {capital}"
        
        else:
            message = "You entered something wrong, please enter a country or capital"


        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode())

        return