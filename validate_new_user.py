# Download the Python helper library from twilio.com/docs/python/install
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC46409dbedc30ffc89e81ccc5faaf4ac2"
auth_token = "8ad3f7e240a6a2a192ee57ca3bca4f6a"
client = Client(account_sid, auth_token)

name = input('Enter a phone number')

validation_request = client.validation_requests \
                           .create(name,
                                   friendly_name="My Home Phone Number")

print(validation_request.validation_code)