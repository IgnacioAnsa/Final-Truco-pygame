import csv
import os

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
