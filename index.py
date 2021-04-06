import os
import arrow
from datetime import datetime
from dateutil import tz
from texter import Texter
from icsparser import ICSParser
from ics import Event
from dotenv import load_dotenv
load_dotenv()

CURRENT_EMPLOYEES = ['Nathan']

def get_ics_paths() -> list:
    employees = []
    for employee in CURRENT_EMPLOYEES:
        employees.append({
            "name": employee,
            "ics_path": os.getenv(f"{employee.upper()}_ICS")
        })
    return employees

def get_calendar_events() -> list:
    employees = get_ics_paths()
     
    for employee in employees:
        parser = ICSParser(employee["ics_path"])
        employee["events"] = parser.get_calendar_events()

    return employees

def get_hour_blocks(employees: list) -> list:
    hour_blocks = []
    current_date = arrow.get(datetime.now())

    for employee in employees:
        employee_hour_blocks = []
        for event in employee["events"]:
            print(event.begin.date(), event.name)
            #if event.begin.date() == current_date.date():
            if event.begin.date() == arrow.get(2021, 3, 18).date():
                if event.name == 'ISL / SLD':
                    start_time = event.begin.strftime("%-I:%M %p")
                    end_time = event.end.strftime("%-I:%M %p")
                    employee_hour_blocks.append(f'{start_time} - {end_time}')

        hour_blocks.append({
            "name": employee["name"],
            "hour_blocks": employee_hour_blocks
        })
    
    return hour_blocks


def main() -> None:
    employees = get_calendar_events()
    hour_blocks = get_hour_blocks(employees)
    print(hour_blocks)


main()