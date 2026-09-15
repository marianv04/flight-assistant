from fastmcp import FastMCP
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.calendar_tool import (
    add_flight_event,
    delete_flight_event,
    update_flight_event
)
from tools.amadeus_tool import (
    search_flights,
    price_flight_offer,
    search_flight_availability,
    availability_from_offer as amadeus_avail_from_offer,
    flight_inspiration_search_impl,
    flight_cheapest_date_search,
    get_airline_checkin_links,
)

LAST_OFFERS = {}
LAST_EVENTS = {}

mcp = FastMCP("flight_assistant_mcp")


# CALENDARIO:

def find_event_id_by_description(query: str):
    query = query.lower()

    for eid, info in LAST_EVENTS.items():
        if info["title"].lower() in query:
            return eid

    for eid, info in LAST_EVENTS.items():
        if info["date"] in query:
            return eid

    for eid, info in LAST_EVENTS.items():
        if info["time"] in query:
            return eid

    if len(LAST_EVENTS) == 1:
        return next(iter(LAST_EVENTS.keys()))

    if LAST_EVENTS:
        return list(LAST_EVENTS.keys())[-1]

    return None


@mcp.tool
def add_event(title: str, date: str, time: str, duration_minutes: int = 90):

    created = add_flight_event(title, date, time, duration_minutes)

    event_id = created["event_id"]

    LAST_EVENTS[event_id] = {
        "title": title,
        "date": date,
        "time": time
    }
    print(event_id)

    return {
    "status": "success",
    "event_id": event_id,
    "htmlLink": created.get("htmlLink"),
    "assistant_message": (
        f"El evento ha sido creado correctamente. "
        f"Su ID REAL es: {event_id}. "
        f"Para modificarlo o eliminarlo DEBES usar este ID exacto."
        )
    }



@mcp.tool
def delete_event(event_id: str = None):

    if not event_id:
        event_id = find_event_id_by_description("")

    if not event_id:
        return {"error": "No se pudo encontrar el evento a eliminar."}

    result = delete_flight_event(event_id)

    LAST_EVENTS.pop(event_id, None)

    return result


@mcp.tool
def update_event(event_id: str = None, title: str = None, date: str = None, time: str = None, duration_minutes: int = None):

    if not event_id:
        event_id = find_event_id_by_description(
            f"{title or ''} {date or ''} {time or ''}"
        )

    if not event_id:
        return {"error": "No se pudo encontrar el evento que deseas modificar."}

    result = update_flight_event(event_id, title, date, time, duration_minutes)

    if event_id in LAST_EVENTS:
        if title: LAST_EVENTS[event_id]["title"] = title
        if date:  LAST_EVENTS[event_id]["date"] = date
        if time:  LAST_EVENTS[event_id]["time"] = time

    return result


# FLIGHT SEARCH:

@mcp.tool
def flight_search(origin: str, destination: str, date: str, adults: int = 1):

    global LAST_OFFERS
    LAST_OFFERS = {}

    result = search_flights(origin, destination, date, adults)
    offers = result.get("data", [])

    response_list = []

    for offer in offers:
        oid = f"ID#{offer['id']}"
        print(oid)
        LAST_OFFERS[oid] = offer

        seg = offer["itineraries"][0]["segments"][0]
        dep = seg["departure"]["at"][11:16]
        arr = seg["arrival"]["iataCode"]
        price = offer["price"]["total"]

        response_list.append({
            "id": oid,
            "departure": dep,
            "arrival": arr,
            "price": f"{price}€"
        })

    return {
        "system_note": (
            "IMPORTANTE: Para pedir precio o disponibilidad, usa EXCLUSIVAMENTE "
            "el valor 'id' tal como aparece (ej: 'ID#3'). No inventes números."
        ),
        "offers": response_list
    }


# FLIGHT PRICE:

@mcp.tool
def flight_price(offer_id: str):

    if offer_id not in LAST_OFFERS:
        print("ERROR: ese ID NO está en memoria")
        return {"error": f"ID '{offer_id}' no existe. IDs válidos: {list(LAST_OFFERS.keys())}"}

    offer = LAST_OFFERS[offer_id]

    response = price_flight_offer(offer)
    return response


# AVAILABILITY FROM OFFER:

@mcp.tool
def availability_from_offer(offer_id: str):

    if offer_id not in LAST_OFFERS:
        return {"error": f"ID '{offer_id}' no existe. Ejecuta flight_search primero."}

    offer = LAST_OFFERS[offer_id]
    return amadeus_avail_from_offer(offer)


# AVAILABILITY DIRECTA:

@mcp.tool
def flight_availability(origin: str, destination: str, date: str, adults: int = 1):

    return search_flight_availability(origin, destination, date, adults)


# INSPIRATION SEARCH:

@mcp.tool
def flight_inspiration_search(origin: str, date: str, one_way: bool = True):

    return flight_inspiration_search_impl(origin, date, one_way)


# SEARCH CHEAPEST DATE:

@mcp.tool
def flight_cheapest_date(origin: str, destination: str, departure_date: str, one_way: bool = True):

    return flight_cheapest_date_search(origin, destination, departure_date, one_way)


# CHECK IN LINKS:

@mcp.tool
def airline_checkin_links(airline_code: str):

    return get_airline_checkin_links(airline_code)


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
