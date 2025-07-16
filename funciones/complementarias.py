import csv
import os
import pygame
import random

archivo_puntajes = "./archivo/registro.csv"

def leer_puntajes() -> dict:

    """
    Lee el archivo de puntajes y devuelve un diccionario con los nombres de los jugadores y sus puntajes máximos.

    Returns:
        dict: Diccionario con nombres como claves y puntajes enteros como valores.
    """

    if not os.path.exists(archivo_puntajes):
        return {}
    with open(archivo_puntajes, mode="r", newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        # Saltar cabecera
        next(lector, None)
        return {fila[0]: int(fila[1]) for fila in lector if fila}
    

def guardar_puntajes(historico: dict) -> None:
    """
    Guarda el diccionario de puntajes en el archivo CSV, ordenado de mayor a menor puntaje.

    Args:
        historico (dict): Diccionario con nombres y puntajes a guardar.
    """

    with open(archivo_puntajes, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Jugador", "Puntos"])
        ranking = sorted(historico.items(), key=lambda x: x[1], reverse=True)
        for nombre, puntos in ranking:
            escritor.writerow([nombre, puntos])

def registrar_puntaje(nombre: str, puntos: int) -> None:
    """
    Registra un nuevo puntaje para un jugador. Si ya existe y el nuevo puntaje es mayor, lo actualiza.

    Args:
        nombre (str): Nombre del jugador.
        puntos (int): Puntaje obtenido.
    """
    nombre = nombre.strip()
    historico = leer_puntajes()
    if nombre in historico:
        if puntos > historico[nombre]:
            historico[nombre] = puntos
    else:
        historico[nombre] = puntos
    guardar_puntajes(historico)

def cargar_carta(nombre: str)-> pygame.Surface:
    """
    Carga una imagen de carta desde la carpeta 'assets/cartas' y la redimensiona.

    Args:
        nombre (str): Nombre de la carta (por ejemplo, '1 de espada').

    Returns:
        pygame.Surface: Imagen de la carta redimensionada (80x120).
    """    
    ruta = f"assets/cartas/{nombre}.jpg"
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, (80, 120))


def generar_mazo() -> list:
    """
    Genera un mazo completo de cartas del Truco (sin comodines, 40 cartas).

    Returns:
        list: Lista de strings representando cada carta.
    """
    palos = ["basto", "espada", "oro", "copa"]
    valores = ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]
    return [f"{valor} de {palo}" for palo in palos for valor in valores]


def repartir_cartas(mazo: list) -> list:
    """
    Mezcla el mazo y reparte tres cartas a dos jugadores.

    Args:
        mazo (list): Lista de cartas sin repartir.

    Returns:
        list: Lista con dos sublistas, una para cada jugador (cada una con 3 cartas).
    """
    random.shuffle(mazo)
    return [mazo[:3], mazo[3:6]]