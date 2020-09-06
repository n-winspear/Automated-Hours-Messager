
import base64
import requests
import json
import datetime

# API Credentials
base_uri = 'https://api.messagemedia.com/v1/messages'
api_key = 'WulBYmeyo8fxyoKfUXrx'
api_secret = 'r2JvTwe22OXDaIDzhruoZPQywYBWW5'

# API Auth Header
api_auth_input = "{}:{}".format(api_key, api_secret)
api_auth_bytes = api_auth_input.encode('ascii')
api_auth_base64_bytes = base64.b64encode(api_auth_bytes)
api_auth_header = api_auth_base64_bytes.decode('ascii')

# Request Header

headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'Authorization': 'Basic {}'.format(api_auth_header)}


def build_request_body(hours):

    # Details
    direct_report = ["Geoff", "+6421337643"]
    office_manager = ["Steph", "+6421627975"]
    
    messages_hours = ""
    
    for block in hours:
        messages_hours += "  {}\n".format(block)

    # Request Body
    return json.dumps({
        "messages": [
            {
                "content": "Good morning Nathan,\n\n Hours delivered",
                "destination_number": "+6421856498",
                "delivery_report": True,
                "format": "SMS"
            },
        ]
    })

def get_hours():
    day = datetime.datetime.today().weekday()
    
    if day == 0:
        return ['9:30am - 12:30pm', '4:30pm - 5:30pm']
    elif day == 1:
        return ['9:30am - 11:30pm', '4:30pm - 5:30pm']
    elif day == 2:
        return ['2:30pm - 5:30pm']
    elif day == 3:
        return ['11:30am - 1:30pm']
    elif day == 4:
        return ['9:30am - 5:30pm']
    else:
        return ['Not a weekday']


def send_message():
    current_time = datetime.datetime.now()
    hours = get_hours()

    #if current_time.hour == 8:
    request_body = build_request_body(hours)
    response = requests.post(base_uri, request_body, headers=headers)

    log_folder_path = "/home/pi/Documents/Github/Automated-Hours-Messager/logs"
    filename = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")

    f = open("{}/{}.txt".format(log_folder_path, filename), "w")
    f.write("Messages sent at: {}\n\n{}".format(
        datetime.datetime.now(), response.json()))
    f.close()


send_message()
