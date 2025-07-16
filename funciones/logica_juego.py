from funciones.complementarias import *
import random

# Jerarquía de las cartas del truco
jerarquia = {
    "1 de espada": 1, "1 de basto": 2, "7 de espada": 3, "7 de oro": 4,
    "3 de basto": 5, "3 de espada": 5, "3 de oro": 5, "3 de copa": 5,
    "2 de basto": 6, "2 de espada": 6, "2 de oro": 6, "2 de copa": 6,
    "1 de oro": 7, "1 de copa": 7,
    "12 de basto": 8, "12 de espada": 8, "12 de oro": 8, "12 de copa": 8,
    "11 de basto": 9, "11 de espada": 9, "11 de oro": 9, "11 de copa": 9,
    "10 de basto": 10, "10 de espada": 10, "10 de oro": 10, "10 de copa": 10,
    "7 de basto": 11, "7 de copa": 11,
    "6 de basto": 12, "6 de espada": 12, "6 de oro": 12, "6 de copa": 12,
    "5 de basto": 13, "5 de espada": 13, "5 de oro": 13, "5 de copa": 13,
    "4 de basto": 14, "4 de espada": 14, "4 de oro": 14, "4 de copa": 14,
}

def generar_mazo() -> list:
    palos = ["basto", "espada", "oro", "copa"]
    valores = ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]
    return [f"{valor} de {palo}" for palo in palos for valor in valores]

def repartir_cartas(mazo: list) -> list:
    random.shuffle(mazo)
    return [mazo[:3], mazo[3:6]]

def elegir_carta(mano: list)-> str:
    while True:
        print("\nTus cartas:")
        for i, carta in enumerate(mano, start=1):
            print(f"{i}. {carta}")
        try:
            eleccion = int(input("Elige el número de la carta que quieres jugar: "))
            if 1 <= eleccion <= len(mano):
                return mano.pop(eleccion - 1)  # Devuelve la carta elegida y la elimina de la mano
            else:
                print("Número inválido.")
        except ValueError:
            print("Debes ingresar un número.")


def jugar_truco():
    print("Bienvenido al Truco!")
    mazo = generar_mazo()
    nombre_jugador = input("Ingrese su nombre: ")

    puntos_jugador = 0
    puntos_maquina = 0
    objetivo = int(input("¿Jugar a 15 o 30 puntos? "))

    while puntos_jugador < objetivo and puntos_maquina < objetivo:
        manos = repartir_cartas(mazo)
        mano_jugador, mano_oponente = manos

        print("\nTus cartas iniciales:", mano_jugador)

        ronda = 1
        puntos_mano = [0, 0]  # [puntos jugador, puntos oponente]

        while ronda <= 3 and puntos_mano[0] < 2 and puntos_mano[1] < 2:
            print(f"\nRonda {ronda}")

            # Jugador elige su carta
            carta_jugador = elegir_carta(mano_jugador)
            print(f"Has jugado: {carta_jugador}")
            carta_oponente = random.choice(mano_oponente)
            mano_oponente.remove(carta_oponente)
            print(f"El oponente ha jugado: {carta_oponente}")

            # Determinar quién gana la ronda
            if jerarquia[carta_jugador] < jerarquia[carta_oponente]:
                print("Ganaste esta ronda.")
                puntos_mano[0] += 1
            elif jerarquia[carta_jugador] > jerarquia[carta_oponente]:
                print("El oponente ganó esta ronda.")
                puntos_mano[1] += 1
            else:
                print("Empate en esta ronda.")

            ronda += 1

        # Asignar puntos al ganador de la mano
        if puntos_mano[0] > puntos_mano[1]:
            print("\nGanaste la mano!")
            puntos_jugador += 1
        elif puntos_mano[0] < puntos_mano[1]:
            print("\nEl oponente ganó la mano.")
            puntos_maquina += 1
        else:
            print("\nLa mano terminó empatada.")

        print(f"\nPuntajes: {nombre_jugador} {puntos_jugador}, maquina {puntos_maquina}")
        registrar_puntaje(nombre_jugador, puntos_jugador)

        if ronda == 3:
            salir = input("¿Deseas continuar jugando? (si/no): ").lower()
            if salir != "si":
                print("\n¡Gracias por jugar! Mostrando el ranking histórico:")
                print(leer_puntajes())  
                return
            
    # Registrar puntaje histórico
    registrar_puntaje(nombre_jugador, puntos_jugador)
    print("\n¡Juego terminado!")
    print(f"Puntajes finales: {nombre_jugador} {puntos_jugador}, maquina {puntos_maquina}")