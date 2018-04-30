from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import google_citrus_inputs
import process_long_directions
import trucking_citrus, trucking_citrus_inputs

app = Flask(__name__)

num_requests = 0
mode = ''
origin = ''
destination = ''
truck_height = 0
truck_weight = 0
user_number = ''

@app.route('/sms', methods=['POST'])

def start_chain():
    global num_requests
    #Choose transit option -> user has sent an option
    if num_requests == 0:
        global user_number
        user_number = request.form['From']
        print(user_number)
        transit = MessagingResponse()
        transit.message('Please type a transit mode: Driving, Walking, Bicycling, or Trucking')
        num_requests += 1
        return str(transit)

    #Find out transit mode -> user has entered trucking information
    elif num_requests == 1:
        global mode
        message_body = request.form['Body']
        message_body = message_body.lower().strip()
        resp = MessagingResponse()
        if message_body == 'trucking':
            mode = message_body
            resp.message('Please enter the weight(tons) and height(meters) of the truck in the format \'weight,height\' both rounded to the nearest number.')
            num_requests += 1
            return str(resp)
        elif message_body in ['driving', 'bicycling', 'walking']:
            mode = message_body
            num_requests += 2
            resp.message(f'You selected {message_body}. Please enter your starting address(Enter full address).')
            return str(resp)
        else:
            resp.message(f'{message_body} is not a valid mode of transportation. Please try again.')
            return str(resp)

    elif num_requests == 2:
        return get_trucking_info()

    elif num_requests == 3:
        return starting_address()

    elif num_requests == 4:
        return ending_address()

    elif num_requests == 5:
        return call_google_maps()

#Find out trucking details -> puts them into Trucking API
def get_trucking_info():
    #Has errors subject to the mercy of the user
    global truck_height, truck_weight, num_requests
    message_body = request.form['Body']
    listed = message_body.split(',')
    resp = MessagingResponse()
    try:
        truck_weight = int(listed[0])
        truck_height = int(listed[1])
        num_requests += 1
        resp.message(f'You selected {message_body}. Please enter your starting address(Enter full address).')
    except ValueError:
        resp.message('Invalid height and weight. Please try again.')

    return str(resp)


#User has entered something other than trucking
def starting_address():
    message_body = request.form['Body']
    global origin
    global num_requests
    origin = message_body
    num_requests += 1
    resp = MessagingResponse()
    resp.message('Thank you. Please enter your destination address(Enter full address)')
    return str(resp)


def ending_address():
    message_body = request.form['Body']
    global destination, num_requests, mode
    destination = message_body
    num_requests += 1
    num_requests = 0
    if mode == 'trucking':
        return call_trucker_maps()
    else:
        return call_google_maps()

def call_trucker_maps():
    global mode, origin, destination, truck_weight, truck_height
    #resp = MessagingResponse()
    directions = trucking_citrus_inputs.main(origin, destination, truck_weight, truck_height)
    process_long_directions.send_message(user_number, directions)


def call_google_maps():
    global mode, origin, destination
    #resp = MessagingResponse()
    directions = google_citrus_inputs.main(origin, destination, mode)
    return process_long_directions.send_message(user_number, directions)


if __name__ == "__main__":
    app.run()

