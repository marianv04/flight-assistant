from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
CALENDAR_ID = os.getenv("CALENDAR_ID")
SCOPES = ["https://www.googleapis.com/auth/calendar"]

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("calendar", "v3", credentials=creds)


# AÑADIR EVENTO:

def add_flight_event(title: str, date: str, time: str, duration_minutes: int = 90):
    """Crea un evento en Google Calendar."""

    start_dt = f"{date}T{time}:00"
    start = datetime.datetime.fromisoformat(start_dt)
    end = start + datetime.timedelta(minutes=duration_minutes)

    event = {
        "summary": title,
        "start": {"dateTime": start.isoformat(), "timeZone": "Europe/Madrid"},
        "end": {"dateTime": end.isoformat(), "timeZone": "Europe/Madrid"},
    }

    created = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

    return {
        "status": "success",
        "event_id": created["id"],
        "htmlLink": created.get("htmlLink")
    }


# ELIMINAR EVENTO:

def delete_flight_event(event_id: str):
    """Elimina un evento del Google Calendar usando el ID."""
    
    try:
        service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        return {"status": "success", "message": f"Evento {event_id} eliminado."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# MODIFICAR EVENTO:

def update_flight_event(event_id: str, title: str = None, date: str = None, time: str = None, duration_minutes: int = None):
    """Actualiza un evento existente."""
    
    try:
        event = service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()

        if title:
            event["summary"] = title

        if date or time:
            start_dt = datetime.datetime.fromisoformat(event["start"]["dateTime"])
            
            if date:
                y, m, d = map(int, date.split("-"))
                start_dt = start_dt.replace(year=y, month=m, day=d)

            if time:
                hh, mm = map(int, time.split(":"))
                start_dt = start_dt.replace(hour=hh, minute=mm, second=0)

            if duration_minutes is None:
                old_end = datetime.datetime.fromisoformat(event["end"]["dateTime"])
                duration_minutes = int((old_end - start_dt).total_seconds() / 60)

            end_dt = start_dt + datetime.timedelta(minutes=duration_minutes)

            event["start"]["dateTime"] = start_dt.isoformat()
            event["end"]["dateTime"] = end_dt.isoformat()

        updated = service.events().update(calendarId=CALENDAR_ID, eventId=event_id, body=event).execute()

        return {
            "status": "success",
            "message": f"Evento {event_id} actualizado.",
            "event": updated
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
    