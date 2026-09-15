# Flight Assistant — Agente Inteligente de Vuelos y Calendario

Flight Assistant es un agente conversacional que combina:
- Un modelo local en LM Studio (Qwen, Llama, Mistral…)
- APIs de Amadeus (búsqueda de vuelos, precios, disponibilidad…)
- Google Calendar (crear, modificar y eliminar eventos)
- MCP (Model Context Protocol) para conectar el modelo con las herramientas

El usuario interactúa de forma natural y el agente decide automáticamente qué herramienta usar en cada momento.

## Configurar Variables de Entorno
Crea un archivo .env en la raíz del proyecto:

AMADEUS_KEY=tu_api_key_de_amadeus
AMADEUS_SECRET=tu_api_secret_de_amadeus

SERVICE_ACCOUNT_FILE=service-account.json
CALENDAR_ID=tu_calendar_id@group.calendar.google.com
GOOGLE_SCOPES=https://www.googleapis.com/auth/calendar

## Configurar Google Calendar
1. Crear un Service Account en Google Cloud.
2. Descargar el archivo service-account.json.
3. Compartir tu calendario con el email del servicio con permisos Editor.

## Cómo Ejecutar el Proyecto
1. Iniciar el servidor MCP.
2. Iniciar Ngrok.
3. Iniciar la consola del asistente.

## Cómo Funciona
### agent.py
- Se conecta automáticamente al túnel Ngrok.
- Envía la conversación y los mensajes al modelo en LM Studio.
- Expone todas las herramientas MCP al modelo.
- Almacena memoria conversacional.
- Garantiza que el modelo use herramientas cuando corresponda (vuelos, precios, eventos…).

### server.py
Implementa las herramientas MCP:

#### Herramientas de Amadeus
- flight_search → buscar vuelos
- flight_price → obtener precio final (desglose real)
- flight_availability → disponibilidad por ruta
- availability_from_offer → disponibilidad de una oferta concreta
- flight_inspiration_search → destinos disponibles desde un origen
- flight_cheapest_date → fechas más baratas
- airline_checkin_links → enlaces de check-in online

#### Herramientas de Google Calendar
- add_event → crear evento
- update_event → modificar evento existente
- delete_event → eliminar evento
- Memoria automática para identificar eventos recientes

## Ejemplos de Uso
### Buscar vuelos
Usuario > Busca vuelos de Madrid a Londres el 5 de enero

### Obtener precio
Usuario > Dame el precio detallado de la segunda opción

### Crear un evento
Usuario > Crea un evento llamado Vuelo a París el 3 de febrero a las 10:00

### Modificar un evento
Usuario > Cambia el evento que acabas de crear a las 11:00

### Eliminar un evento
Usuario > Borra el evento del 3 de febrero
