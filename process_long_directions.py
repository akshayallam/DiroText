from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC46409dbedc30ffc89e81ccc5faaf4ac2"
# Your Auth Token from twilio.com/console
auth_token  = "8ad3f7e240a6a2a192ee57ca3bca4f6a"

client = Client(account_sid, auth_token)

def send_message(number, text):
    global client
    if len(text) < 1500:
        message = client.messages.create(
            to=str(number),
            from_="+18316099948",
            body=text)
    else:
        threshold = 1500
        while True:
            if len(text) <= threshold:
                message = client.messages.create(
                    to=str(number),
                    from_="+18316099948",
                    body=text)
                break

            for i in range(len(text) - 1, -1, -1):
                if text[i] == '\n' and len(text[:i]) <= threshold:
                    message = client.messages.create(
                        to=str(number),
                        from_="+18316099948",
                        body=text[:i])
                    text = text[i + 1:]
                    break
