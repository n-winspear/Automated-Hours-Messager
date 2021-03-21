
import base64
import requests
import json
import datetime
import os
from dotenv import load_dotenv
load_dotenv()

# API Credentials
base_uri = 'https://api.messagemedia.com/v1/messages'
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# API Auth Header
api_auth_input = "{}:{}".format(API_KEY, API_SECRET)
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
    office_manager = ["Sythey", "+6421848159"]
    nathan_test = ["Nathan", "+6421856498"]

    nathan_hours = "".join(
        [f"  {block}\n" for block in hours["nathan"]]) if hours['nathan'] else None
    
    divya_hours = "".join(
        [f"  {block}\n" for block in hours["divya"]]) if hours['divya'] else None

    message_content = build_message_content(nathan_hours, divya_hours)

    # Request Body
    return json.dumps({
        "messages": [
            {
                "content": f"Good morning {direct_report[0]}, {message_content}\n\nThis message was sent from Nathan's automated message system",
                "destination_number": f"{direct_report[1]}",
                "delivery_report": True,
                "format": "SMS"
            },
            {
                "content": f"Good morning {nathan_test[0]},{message_content}\n\nThis message was sent from Nathan's automated message system",
                "destination_number": f"{nathan_test[1]}",
                "delivery_report": True,
                "format": "SMS"
            },        
        ]
    })


def build_message_content(nathan_hours, divya_hours):

    message_content = ""
    if nathan_hours:
        message_content += f"\n\nNathan will be in today from:\n{nathan_hours}"

    if divya_hours:
        message_content += f"\n\nDivya will be in today from:\n{divya_hours}"

    return message_content


def get_hours():
    day = datetime.datetime.today().weekday()
    
    if day == 0:
        return {
            "nathan": ['8:30am - 3:45pm'],
            "divya": None,
        }

    elif day == 1:
        return {
            "nathan": ['8:30am - 10:00am', '11:00am - 1:00pm', '2:15pm - 4:45pm'],
            "divya": ['8:30am - 2:30pm'],
        }
    elif day == 2:
        return {
            "nathan": ['10:15am - 11:45am'],
            "divya": ['8:30am - 2:30pm'],
        }
    elif day == 3:
        return {
            "nathan": ['10:15am - 11:45am', '1:15pm - 5:00pm'],
            "divya": ['8:30am - 5:00pm']
        }

    elif day == 4:
        return {
            "nathan": None,
            "divya": None
        }
    else:
        return ['Not a weekday']
    

def send_message():
    hours = get_hours()

    print("Sending messages...")
    request_body = build_request_body(hours)
    response = requests.post(base_uri, request_body, headers=headers)
    print("Messages sent!" if response.status_code == 202 else "Messages failed to send.")
    
    try:
        print("Creating log...")
        log_folder_path = "/home/pi/Documents/Github/Automated-Hours-Messager/logs"
        filename = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")

        f = open("{}/{}.txt".format(log_folder_path, filename), "w")
        f.write("Messages sent at: {}\n\n{}".format(
            datetime.datetime.now(), json.dumps(response.json(), indent=4, sort_keys=True)))
        f.close()
        print("Log created!")
    except:
        print('Failed to create log.')

send_message()
