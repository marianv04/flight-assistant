from agent import ask_agent

print("\n──────────────────────────────────────────")
print("        Flight Assistant CLI Console")
print("──────────────────────────────────────────")
print(" Pregúntame por vuelos, precios y eventos.")
print(" Escribe 'exit' para cerrar la sesión.\n")

while True:
    user = input("Usuario > ").strip()
    if user.lower() in ("exit", "quit"):
        print("\n Sesión finalizada. Gracias por usar Flight Assistant.\n")
        break

    respuesta = ask_agent(user)
    print(f"Asistente > {respuesta}\n")
