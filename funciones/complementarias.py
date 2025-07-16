import csv
import os
import pygame
import random

archivo_puntajes = "./archivo/registro.csv"

def leer_puntajes() -> dict:
    if not os.path.exists(archivo_puntajes):
        return {}
    with open(archivo_puntajes, mode="r", newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo)
        # Saltar cabecera
        next(lector, None)
        return {fila[0]: int(fila[1]) for fila in lector if fila}
    

def guardar_puntajes(historico: dict) -> None:
    with open(archivo_puntajes, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Jugador", "Puntos"])
        ranking = sorted(historico.items(), key=lambda x: x[1], reverse=True)
        for nombre, puntos in ranking:
            escritor.writerow([nombre, puntos])

def registrar_puntaje(nombre: str, puntos: int) -> None:
    nombre = nombre.strip()
    historico = leer_puntajes()
    if nombre in historico:
        if puntos > historico[nombre]:
            historico[nombre] = puntos
    else:
        historico[nombre] = puntos
    guardar_puntajes(historico)

def cargar_carta(nombre):
    ruta = f"assets/cartas/{nombre}.jpg"
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, (80, 120))


def generar_mazo() -> list:
    palos = ["basto", "espada", "oro", "copa"]
    valores = ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]
    return [f"{valor} de {palo}" for palo in palos for valor in valores]


def repartir_cartas(mazo: list) -> list:
    random.shuffle(mazo)
    return [mazo[:3], mazo[3:6]]