# ✈️ Flight Assistant

Agente conversacional desarrollado en **Python** que permite buscar vuelos y gestionar eventos de Google Calendar utilizando lenguaje natural.

El sistema utiliza un **LLM ejecutado localmente mediante LM Studio** y **Model Context Protocol (MCP)** para seleccionar y ejecutar automáticamente las herramientas necesarias según la petición del usuario.

## 🚀 Funcionalidades

### ✈️ Búsqueda de vuelos

Integración con **Amadeus API** para:

- Buscar vuelos por origen, destino y fecha.
- Consultar el precio final de una oferta.
- Comprobar disponibilidad.
- Buscar destinos desde un aeropuerto.
- Consultar las fechas más económicas.
- Obtener enlaces de check-in de aerolíneas.

### 📅 Gestión de Google Calendar

El agente puede gestionar eventos mediante lenguaje natural:

- Crear eventos.
- Modificar eventos existentes.
- Eliminar eventos.
- Identificar eventos creados recientemente durante la conversación.

Por ejemplo:

> Usuario: Busca vuelos de Madrid a Londres el 5 de enero.

> Usuario: ¿Cuánto cuesta la segunda opción?

> Usuario: Crea un evento en mi calendario para ese vuelo.

El agente determina qué herramienta debe utilizar en cada petición.

## 🧠 Arquitectura

```text
                    ┌─────────────────┐
                    │     Usuario     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Flight Assistant│
                    │    agent.py     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    LLM local    │
                    │    LM Studio    │
                    └────────┬────────┘
                             │
                             │ MCP
                             ▼
                    ┌─────────────────┐
                    │   MCP Server    │
                    │    server.py    │
                    └───────┬─────────┘
                            │
                  ┌─────────┴─────────┐
                  ▼                   ▼
          ┌──────────────┐     ┌──────────────┐
          │ Amadeus API  │     │Google Calendar│
          │    Flights   │     │     API       │
          └──────────────┘     └──────────────┘
```

## 🛠️ Tecnologías

- Python
- Model Context Protocol (MCP)
- FastMCP
- LM Studio
- Qwen
- Amadeus API
- Google Calendar API
- Google Cloud Service Accounts
- Ngrok

## 📁 Estructura del proyecto

```text
flight-assistant/
│
├── app/
│   ├── agent.py
│   ├── chat.py
│   └── server.py
│
├── tools/
│   ├── amadeus_tool.py
│   └── calendar_tool.py
│
├── .gitignore
└── README.md
```

### `agent.py`

Gestiona la conversación con el usuario y la comunicación con el modelo ejecutado en LM Studio.

El agente recibe las herramientas disponibles mediante MCP y determina cuándo debe utilizarlas para obtener información externa o realizar acciones.

### `server.py`

Implementa el servidor MCP y expone las herramientas disponibles al modelo.

### `amadeus_tool.py`

Gestiona la comunicación con Amadeus API para búsquedas, precios y disponibilidad de vuelos.

### `calendar_tool.py`

Gestiona la integración con Google Calendar para crear, modificar y eliminar eventos.

## 🔧 Configuración

### 1. Variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
AMADEUS_KEY=your_amadeus_api_key
AMADEUS_SECRET=your_amadeus_api_secret
SERVICE_ACCOUNT_FILE=service-account.json
CALENDAR_ID=your_calendar_id
```

### 2. Google Calendar

1. Crear un Service Account en Google Cloud.
2. Descargar sus credenciales como `service-account.json`.
3. Compartir el calendario con el correo electrónico del Service Account y conceder permisos para gestionar eventos.

## ▶️ Ejecución

El proyecto requiere tener **LM Studio** ejecutándose localmente.

1. Iniciar el servidor MCP:

```bash
python app/server.py
```

2. Iniciar el túnel de Ngrok.

```bash
ngrok http 8000
```

3. Ejecutar el asistente:

```bash
python app/chat.py
```

## 🔌 Herramientas MCP

El modelo tiene acceso a las siguientes herramientas:

| Herramienta | Función |
|---|---|
| `flight_search` | Buscar vuelos |
| `flight_price` | Obtener el precio final de una oferta |
| `flight_availability` | Consultar disponibilidad |
| `availability_from_offer` | Consultar disponibilidad de una oferta |
| `flight_inspiration_search` | Buscar destinos desde un origen |
| `flight_cheapest_date` | Buscar fechas más económicas |
| `airline_checkin_links` | Obtener enlaces de check-in |
| `add_event` | Crear eventos |
| `update_event` | Modificar eventos |
| `delete_event` | Eliminar eventos |

## 💬 Ejemplos

```text
Usuario > Busca vuelos de Madrid a Londres el 5 de enero

Usuario > Dame el precio detallado de la segunda opción

Usuario > Crea un evento llamado Vuelo a París el 3 de febrero a las 10:00

Usuario > Cambia el evento que acabas de crear a las 11:00

Usuario > Borra el evento que acabas de modificar
```