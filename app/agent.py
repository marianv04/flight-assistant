
import requests
import time

LM_URL = "http://127.0.0.1:1234/v1/responses"

conversation = [
    {
        "role": "system",
        "content": (
            "Eres FlightAssistant, un agente experto en vuelos y calendario.\n"
            "TU REGLA PRINCIPAL: siempre que el usuario solicite informacion que requiera "
            "datos reales o acciones externas, DEBES usar una herramienta MCP.\n\n"
            "CUANDO USAR CADA HERRAMIENTA:\n\n"
            "--- VUELOS ---\n"
            "- Usa 'flight_search' para buscar vuelos entre dos aeropuertos en una fecha.\n"
            "- Usa 'flight_price' cuando el usuario pregunta por el precio final, coste, "
            "tarifa, importe o desglose de una oferta concreta.\n"
            "- Usa 'flight_availability' cuando el usuario pregunte por disponibilidad o asientos.\n"
            "- Usa 'availability_from_offer' cuando el usuario pida disponibilidad de una oferta concreta.\n"
            "- Usa 'flight_inspiration_search' cuando pregunte a donde puede viajar desde un aeropuerto.\n"
            "- Usa 'flight_cheapest_date' cuando quiera fechas mas baratas.\n"
            "- Usa 'airline_checkin_links' cuando pida enlaces de check-in para una aerolinea.\n\n"
            "--- GOOGLE CALENDAR ---\n"
            "- Usa 'add_event' si el usuario quiere CREAR un evento.\n"
            "- Usa 'update_event' si el usuario quiere MODIFICAR un evento (titulo, fecha, hora, duracion).\n"
            "- Usa 'delete_event' si el usuario quiere ELIMINAR un evento.\n"
            "SEÑAL: palabras como 'modifica', 'edita', 'cambia', 'mueve', 'renombra', 'corrige', "
            "'borra', 'elimina' DEBEN activar una tool.\n\n"
            "NORMAS IMPORTANTES:\n"
            "1) NO inventes datos si una tool puede obtenerlos.\n"
            "2) NO respondas manualmente si existe una tool adecuada.\n"
            "3) Si se menciona 'el evento que acabas de crear', usa el ULTIMO event_id devuelto.\n"
            "4) Si la peticion coincide con varias tools, elige SIEMPRE la mas especifica.\n"
            "5) Si falta informacion necesaria, pide los datos antes de llamar a la tool.\n"
            "6) Nunca escribas informacion que deberia provenir de una herramienta MCP.\n"
            "7) Si el usuario proporciona una fecha sin año (por ejemplo '15 de marzo'), debes completar explícitamente el año como 2026 antes de llamar a cualquier herramienta.\n"
        )
    }
]


def get_ngrok_url():
    while True:
        try:
            data = requests.get("http://127.0.0.1:4040/api/tunnels").json()
            tunnels = data.get("tunnels", [])
            for t in tunnels:
                if t["proto"] == "https":
                    return t["public_url"]
        except:
            pass

        print("Esperando a ngrok...")
        time.sleep(1)


NGROK_URL = get_ngrok_url()
MCP_URL = f"{NGROK_URL}/mcp/"


def ask_agent(message: str):
    conversation.append({"role": "user", "content": message})

    payload = {
        "model": "qwen/qwen3-4b-2507",
        "input": conversation,
        "tools": [
            {
                "type": "mcp",
                "server_label": "flight_assistant",
                "server_url": MCP_URL,
                "require_approval": "never"
            }
        ]
    }

    resp = requests.post(LM_URL, json=payload).json()

    output_text = ""
    for block in resp.get("output", []):
        if block.get("type") == "message":
            for piece in block.get("content", []):
                if piece["type"] == "output_text":
                    output_text += piece["text"]

    conversation.append({"role": "assistant", "content": output_text})

    return output_text or "No output returned"