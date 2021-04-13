from datetime import datetime
from icalendar import Calendar
from cleanedevent import CleanedEvent
import recurring_ical_events
import requests

class ICSParser:

    def __init__(self, ics_path: str) -> None:
        self.__ics_path = ics_path
        self.__calendar = self.__get_calendar_from_ics()

    def __get_calendar_from_ics(self) -> Calendar:
        print(self.__ics_path)
        calendar = Calendar.from_ical(requests.get(self.__ics_path).text)
        return calendar

    def get_ics_calendar_events(self, start_date: datetime, end_date: datetime) -> list:
        events = sorted([CleanedEvent(
            title=event["SUMMARY"],
            start_datetime=event["DTSTART"].dt,
            end_datetime=event["DTEND"].dt
        ) for event in recurring_ical_events.of(self.__calendar).between(start_date, end_date)], key = lambda cleaned_event: cleaned_event.start_datetime)

        return events