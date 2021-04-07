from datetime import datetime

class CleanedEvent:

    def __init__(self, title: str, start_datetime: datetime, end_datetime: datetime) -> None:
        self.title = title
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.start_date = start_datetime.date()
        self.end_date = end_datetime.date()
        self.start_time = start_datetime.strftime("%-I:%M %p")
        self.end_time = end_datetime.strftime("%-I:%M %p")

    def __str__(self) -> str:
        return f"EVENT: {self.title}\nSTART: {self.start_date} - {self.start_time}\nEND: {self.end_date} - {self.end_time}\n"

    def __repr__(self) -> str:
        return f"<EVENT: {self.title}\nSTART: {self.start_date} - {self.start_time}\nEND: {self.end_date} - {self.end_time}>\n"