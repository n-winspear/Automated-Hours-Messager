import requests
from ics import Calendar

class ICSParser:

    def __init__(self, ics_path: str) -> None:
        self.__ics_path = ics_path
        self.__calendar = self.__get_calendar_from_ics()

    def __get_calendar_from_ics(self) -> Calendar:
        cal = Calendar(requests.get(self.__ics_path).text)
        return cal

    def get_calendar_events(self) -> dict:
        return list(self.__calendar.timeline)
