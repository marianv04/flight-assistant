import os
import requests
from dotenv import load_dotenv

load_dotenv()

AMADEUS_KEY = os.getenv("AMADEUS_KEY")
AMADEUS_SECRET = os.getenv("AMADEUS_SECRET")

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_KEY,
        "client_secret": AMADEUS_SECRET,
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        raise Exception(f"Error al obtener token: {response.text}")

    return response.json()["access_token"]


# FLIGHT SEARCH:

def search_flights(origin: str, destination: str, date: str, adults: int = 1, max_results: int = 5):
    """Buscar vuelos a partir del origen, destino y fecha."""

    token = get_amadeus_token()

    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": adults,
        "max": max_results,
        "currencyCode": "EUR",
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en Flight Search: {response.text}")

    return response.json()


# FLIGHT PRICE:

def price_flight_offer(offer):
    """ Envía a Amadeus la oferta completa para obtener el precio final. """

    token = get_amadeus_token()

    url = "https://test.api.amadeus.com/v1/shopping/flight-offers/pricing"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "data": {
            "type": "flight-offers-pricing",
            "flightOffers": [offer]
        }
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error al obtener precio: {response.text}")

    return response.json()


# AVAILABILITY DIRECTA:

def search_flight_availability(origin: str, destination: str, date: str, adults: int = 1):
    """ Busca la disponibilidad apartir del origen, destino y fecha. """
    token = get_amadeus_token()

    url = "https://test.api.amadeus.com/v1/shopping/availability/flight-availabilities"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "originDestinations": [
            {
                "id": "1",
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDateTime": {"date": date}
            }
        ],
        "travelers": [
            {"id": str(i+1), "travelerType": "ADULT"}
            for i in range(adults)
        ],
        "sources": ["GDS"]
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en Flight Availability: {response.text}")

    return response.json()


# AVAILABILITY FROM OFFER:

def availability_from_offer(offer):
    """ Extrae origen, destino y fecha de la oferta elegida y llama a Availability Search. """

    seg = offer["itineraries"][0]["segments"][0]

    origin = seg["departure"]["iataCode"]
    destination = seg["arrival"]["iataCode"]
    date = seg["departure"]["at"].split("T")[0]

    return search_flight_availability(origin, destination, date)


# FLIGHT INSPIRATION:

def flight_inspiration_search_impl(origin: str, date: str, one_way: bool = True):
    token = get_amadeus_token()

    url = "https://test.api.amadeus.com/v1/shopping/flight-destinations"

    params = {
        "origin": origin,
        "departureDate": date,
        "oneWay": str(one_way).lower(),
        "viewBy": "DATE"
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en Flight Inspiration Search: {response.text}")

    return response.json()


# FLIGHT CHEAPEST DATE:

def flight_cheapest_date_search(origin: str, destination: str, departure_date: str, one_way: bool = True):
    token = get_amadeus_token()

    url = "https://test.api.amadeus.com/v1/shopping/flight-dates"

    params = {
        "origin": origin,
        "destination": destination,
        "departureDate": departure_date,
        "oneWay": str(one_way).lower(),
        "viewBy": "DATE"
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en Flight Cheapest Date Search: {response.text}")

    return response.json()


# CHECK IN LINKS:

def get_airline_checkin_links(airline_code: str):
    
    """ Devuelve los enlaces de check-in online para una aerolínea. """

    token = get_amadeus_token()

    url = "https://test.api.amadeus.com/v2/reference-data/urls/checkin-links"

    params = {
        "airlineCode": airline_code.upper()
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en Check-in Links: {response.text}")

    return response.json()
