import json
import base64
import os
from dotenv import load_dotenv
load_dotenv()

class Texter:

    def __init__(self) -> None:
        self.__base_URL = "https://api.messagemedia.com/v1/messages"
        self.__api_key = os.getenv("API_KEY")
        self.__client_secret = os.getenv("API_SECRET")
        self.__authorization_header = self.__build_authorization_header()

    def __build_authorization_header(self) -> str:
        header_input = f"{self.__api_key}:{self.__client_secret}"
        header_bytes = header_input.encode('ascii')
        header_B64 = base64.b64encode(header_bytes)
        authorization_header = header_B64.decode('ascii')
        return authorization_header

    def __build_request_headers(self) -> dict:
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.__authorization_header}'
        }

    def build_request_body(self, recipients: list, text_message_content: str) -> str:
        request_body = {
            "messages": []
        }

        for recipient in recipients:
            request_body["messages"].append({
                "content": f"Good morning {recipient['first_name']}, {text_message_content}\n\nThis message was sent from Nathan's automated message system",
                "destination_number": f"{recipient['phone_number']}",
                "delivery_report": True,
                "format": "SMS"
            })

        return json.dumps(request_body)