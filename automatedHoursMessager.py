
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
    nathan_test = ["Nathan", "+6421856498"]

    nathan_hours = "".join(
        [f"  {block}\n" for block in hours["nathan"]]) if hours['nathan'] else None
    tanya_hours = "".join(
        [f"  {block}\n" for block in hours["tanya"]]) if hours['tanya'] else None

    message_content = build_message_content(nathan_hours, tanya_hours)

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
            {
                "content": f"Good morning {office_manager[0]},{message_content}\n\nThis message was sent from Nathan's automated message system",
                "destination_number": f"{office_manager[1]}",
                "delivery_report": True,
                "format": "SMS"
            },
        ]
    })


def build_message_content(nathan_hours, tanya_hours):

    message_content = ""
    if nathan_hours:
        message_content += f"\n\nNathan will be in today from:\n{nathan_hours}"

    if tanya_hours:
        message_content += f"\n\nTanya will be in today from:\n{tanya_hours}"

    return message_content


def get_hours():
    day = datetime.datetime.today().weekday()

    if day == 0:
        return {
            "nathan": ['9:00am - 5:30pm'],
            "tanya": None
        }

    elif day == 1:
        return {
            "nathan": ['1:00pm - 5:30pm'],
            "tanya": None #['9:30am - 10:30am', '1:30pm - 4:30pm']
        }
    elif day == 2:
        return {
            "nathan": ['9:00am - 5:30pm'],
            "tanya": ['9:30am - 4:30pm'] #['9:00am - 10:30am', '2:30pm - 5:00pm']
        }
    elif day == 3:
        return {
            "nathan": ['9:00am - 5:30pm'],
            "tanya": None
        }

    elif day == 4:
        return {
            "nathan": ['9:00am - 5:30pm'],
            "tanya": None
        }
    else:
        return ['Not a weekday']

    """
    if day == 0:
        return {
            "nathan": ['9:30am - 12:30pm', '4:30pm - 5:30pm'],
            "tanya": None
        }

    elif day == 1:
        return {
            "nathan": ['9:30am - 11:30pm', '4:30pm - 5:30pm'],
            "tanya": ['9:30am - 10:30am', '1:30pm - 4:30pm']
        }
    elif day == 2:
        return {
            "nathan": ['2:30pm - 5:30pm'],
            "tanya": ['9:00am - 10:30am', '2:30pm - 5:00pm']
        }
    elif day == 3:
        return {
            "nathan": ['11:30am - 1:30pm'],
            "tanya": None
        }

    elif day == 4:
        return {
            "nathan": ['9:30am - 5:30pm'],
            "tanya": None
        }
    else:
        return ['Not a weekday']
    """


def send_message():
    current_time = datetime.datetime.now()
    hours = get_hours()

    if current_time.hour == 8:
        request_body = build_request_body(hours)
        response = requests.post(base_uri, request_body, headers=headers)

        log_folder_path = "/home/pi/Documents/Github/Automated-Hours-Messager/logs"
        filename = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")

        f = open("{}/{}.txt".format(log_folder_path, filename), "w")
        f.write("Messages sent at: {}\n\n{}".format(
            datetime.datetime.now(), response))
        f.close()


send_message()
