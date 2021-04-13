import os
from datetime import datetime, timedelta
from texter import Texter
from logger import Logger
from icsparser import ICSParser
from dotenv import load_dotenv
load_dotenv()

CURRENT_EMPLOYEES = ['Nathan', 'Divya']
RECIPIENTS = [
    {
        "first_name": "Nathan",
        "last_name": "Winspear",
        "phone_number": "+6421856498"
    },
    {
        "first_name": "Geoff",
        "last_name": "Lorigan",
        "phone_number": "+6421337643"
    },
    {
        "first_name": "Demian",
        "last_name": "Rosenthal",
        "phone_number": "+64275310871"
    },
]

START_DATE = datetime.now().date()
END_DATE = START_DATE + timedelta(days=1)

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
        employee["events"] = parser.get_ics_calendar_events(START_DATE, END_DATE)

    return employees

def get_hour_blocks(employees: list) -> list:
    hour_blocks = []
    current_date = datetime.now().date()

    for employee in employees:
        employee_hour_blocks = []
        for event in employee["events"]:
            if event.start_date == current_date:
                if event.title == 'ISL / SLD':
                    employee_hour_blocks.append(f'{event.start_time} - {event.end_time}')

        hour_blocks.append({
            "name": employee["name"],
            "hour_blocks": employee_hour_blocks
        })
    
    return hour_blocks

def build_text_message_content(hour_blocks: list) -> str:
    text_message_content = ""

    for employee in hour_blocks:
        if len(employee["hour_blocks"]) > 0:
            text_message_content += '\n\n{} will be in today from:\n  {}'.format(employee["name"], "  \n".join(employee["hour_blocks"]))
            
    return text_message_content

def main() -> None:
    employees = get_calendar_events()
    hour_blocks = get_hour_blocks(employees)
    text_message_content = build_text_message_content(hour_blocks)
    if text_message_content != "":
        txtr = Texter()
        request_body = txtr.build_request_body(RECIPIENTS, text_message_content)
        response = txtr.send_text_messages(request_body)
        lggr = Logger()
        lggr.create_log(response)


main()