from funciones.complementarias import *
import random
import sys

def jugar_truco():
    """
    Función principal que ejecuta el juego de Truco con interfaz gráfica usando Pygame.
    Maneja los distintos estados del juego: menú, ingreso de nombre, selección de puntos,
    animación de reparto, juego, ranking y final.
    """
    pygame.init()

    # Dimensiones y ventana
    ANCHO, ALTO = 1000, 600
    VENTANA = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Truco")

    # Colores y fuente
    VERDE_MESA = (0, 100, 0)
    BLANCO = (255, 255, 255)
    ROJO = (255, 50, 50)
    fuente = pygame.font.SysFont("Comic Sans", 30)

    # Posiciones de cartas
    posiciones_jugador = [(200 + i * 100, ALTO - 150) for i in range(3)]
    posiciones_maquina = [(200 + i * 100, 50) for i in range(3)]
    zona_jugada_jugador = (ANCHO // 2 - 40, ALTO // 2 + 60)
    zona_jugada_maquina = (ANCHO // 2 - 40, ALTO // 2 - 180)
    
    # Imagen del reverso de las cartas
    reverso = pygame.image.load("assets/cartas/dorso_carta.jpg")
    reverso = pygame.transform.scale(reverso, (80, 120))
    
    # Reloj de control de FPS
    reloj = pygame.time.Clock()

    # Variables de estado del juego
    estado = "menu"
    input_text = ""
    nombre_jugador = ""

    puntos_objetivo = 15
    mano_jugador = []
    mano_maquina = []
    imagenes_mano = []
    rects_cartas = []
    puntos_jugador = 0
    puntos_maquina = 0
    puntos_mano = [0, 0]
    ronda = 1
    carta_jugada_jugador = None
    carta_jugada_maquina = None
    mostrando_resultado = False
    resultado_texto = ""
    animacion_frame = 0
    animacion_max_frames = 60
    mazo_anim = []

    def iniciar_mano():
        """
        Inicializa una nueva mano del Truco, repartiendo cartas a ambos jugadores
        y actualizando las variables necesarias.
        """
        nonlocal mano_jugador, mano_maquina, imagenes_mano, rects_cartas, puntos_mano, ronda
        puntos_mano[:] = [0, 0]
        ronda = 1
        mazo = generar_mazo()
        manos = repartir_cartas(mazo)
        mano_jugador = manos[0]
        mano_maquina = manos[1]
        imagenes_mano = [cargar_carta(c) for c in mano_jugador]
        rects_cartas.clear()
        for i, img in enumerate(imagenes_mano):
            rect = img.get_rect(topleft=posiciones_jugador[i])
            rects_cartas.append(rect)
    
    # Bucle principal del juego
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN:
                if estado == "input_nombre":
                    if evento.key == pygame.K_RETURN and input_text.strip():
                        nombre_jugador = input_text.strip()
                        input_text = ""
                        estado = "seleccion_puntos"
                    elif evento.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 20:
                            input_text += evento.unicode
            
            # Lógica de los distintos estados
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if estado == "menu":
                    for i, texto_opcion in enumerate(["Jugar Truco", "Ranking", "Salir"]):
                        superficie = fuente.render(texto_opcion, True, BLANCO)
                        rect = superficie.get_rect(midtop=(ANCHO // 2, 200 + i * 100))
                        if rect.collidepoint(x, y):
                            if texto_opcion == "Jugar Truco":
                                estado = "input_nombre"
                                input_text = ""
                            elif texto_opcion == "Ranking":
                                estado = "ranking"
                            elif texto_opcion == "Salir":
                                pygame.quit()
                                sys.exit()

                elif estado == "seleccion_puntos":
                    # Selección de objetivo de puntos
                    if ANCHO // 2 - 100 <= x <= ANCHO // 2 + 100:
                        if ALTO // 2 <= y <= ALTO // 2 + 50:
                            puntos_objetivo = 15
                        elif ALTO // 2 + 60 <= y <= ALTO // 2 + 110:
                            puntos_objetivo = 30
                        puntos_jugador = 0
                        puntos_maquina = 0
                        estado = "animacion_repartir"
                        animacion_frame = 0
                        mazo_anim = generar_mazo()

                elif estado == "ranking":
                    # Ranking historico
                    rect_menu = fuente.render("Menú", True, BLANCO).get_rect(topright=(ANCHO - 20, 20))
                    if rect_menu.collidepoint(x, y):
                        estado = "menu"

                elif estado == "juego":
                    # Menú dentro del juego
                    rect_menu = fuente.render("Menú", True, BLANCO).get_rect(topright=(ANCHO - 20, 20))
                    if rect_menu.collidepoint(x, y):
                        estado = "menu"
                        continue
                    
                    # Resultado de la ronda
                    if mostrando_resultado:
                        mostrando_resultado = False
                        carta_jugada_jugador = None
                        carta_jugada_maquina = None
                        ronda += 1
                        if puntos_mano[0] == 2 or puntos_mano[1] == 2 or ronda > 3:
                            if puntos_mano[0] > puntos_mano[1]:
                                puntos_jugador += 1
                                registrar_puntaje(nombre_jugador, puntos_jugador)
                                if puntos_jugador >= puntos_objetivo:
                                    resultado_texto = "¡Has ganado!"
                                    estado = "final"
                                    continue
                            elif puntos_mano[0] < puntos_mano[1]:
                                puntos_maquina += 1
                                if puntos_maquina >= puntos_objetivo:
                                    resultado_texto = "Has perdido"
                                    estado = "final"
                                    continue
                            iniciar_mano()
                    else:
                        # Detectar clic en carta
                        for i, rect in enumerate(rects_cartas):
                            if rect.collidepoint(x, y):
                                if carta_jugada_jugador is None:
                                    carta_jugada_jugador = mano_jugador.pop(i)
                                    carta_jugada_maquina = random.choice(mano_maquina)
                                    mano_maquina.remove(carta_jugada_maquina)

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

                                    if jerarquia[carta_jugada_jugador] < jerarquia[carta_jugada_maquina]:
                                        puntos_mano[0] += 1
                                        resultado_texto = "Ganaste esta ronda"
                                    elif jerarquia[carta_jugada_jugador] > jerarquia[carta_jugada_maquina]:
                                        puntos_mano[1] += 1
                                        resultado_texto = "La máquina ganó esta ronda"
                                    else:
                                        resultado_texto = "Empate en esta ronda"

                                    mostrando_resultado = True
                                    imagenes_mano = [cargar_carta(c) for c in mano_jugador]
                                    rects_cartas.clear()
                                    for i, img in enumerate(imagenes_mano):
                                        rect = img.get_rect(topleft=posiciones_jugador[i])
                                        rects_cartas.append(rect)
                                    break

        VENTANA.fill(VERDE_MESA)

        if estado == "menu":
            for i, texto_opcion in enumerate(["Jugar Truco", "Ranking", "Salir"]):
                superficie = fuente.render(texto_opcion, True, BLANCO)
                rect = superficie.get_rect(midtop=(ANCHO // 2, 200 + i * 100))
                VENTANA.blit(superficie, rect.topleft)

        elif estado == "input_nombre":
            texto_prompt = fuente.render("Ingrese su nombre:", True, BLANCO)
            VENTANA.blit(texto_prompt, (ANCHO // 2 - texto_prompt.get_width() // 2, ALTO // 2 - 80))
            input_rect = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 - 30, 300, 60)
            pygame.draw.rect(VENTANA, (0, 0, 0), input_rect)
            texto_input = fuente.render(input_text, True, BLANCO)
            VENTANA.blit(texto_input, (input_rect.x + 10, input_rect.y + 10))

        elif estado == "seleccion_puntos":
            texto = fuente.render("¿A cuántos puntos querés jugar?", True, BLANCO)
            VENTANA.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2 - 60))
            pygame.draw.rect(VENTANA, (0, 0, 0), (ANCHO // 2 - 100, ALTO // 2, 200, 50))
            pygame.draw.rect(VENTANA, (0, 0, 0), (ANCHO // 2 - 100, ALTO // 2 + 60, 200, 50))
            texto15 = fuente.render("Jugar a 15", True, BLANCO)
            texto30 = fuente.render("Jugar a 30", True, BLANCO)
            VENTANA.blit(texto15, (ANCHO // 2 - texto15.get_width() // 2, ALTO // 2 + 10))
            VENTANA.blit(texto30, (ANCHO // 2 - texto30.get_width() // 2, ALTO // 2 + 70))
        
        elif estado == "animacion_repartir":
            posiciones_jugador = [(200 + i * 100, ALTO - 150) for i in range(3)]
            posiciones_maquina = [(200 + i * 100, 50) for i in range(3)]

            centro_x = ANCHO // 2 - 40
            centro_y = ALTO // 2 - 60
            reloj_anim = pygame.time.Clock()

            # Mezcla visual
            for _ in range(15):
                VENTANA.fill(VERDE_MESA)
                for _ in range(10):
                    x = centro_x + random.randint(-50, 50)
                    y = centro_y + random.randint(-30, 30)
                    VENTANA.blit(reverso, (x, y))
                texto_anim = fuente.render("Barajando...", True, BLANCO)
                VENTANA.blit(texto_anim, (ANCHO // 2 - texto_anim.get_width() // 2, ALTO // 2 + 100))
                pygame.display.flip()
                reloj_anim.tick(15)

            # Reparto boca abajo
            for i in range(3):
                VENTANA.fill(VERDE_MESA)
                VENTANA.blit(reverso, (20, 20))  # Mazo
                for j in range(i + 1):
                    VENTANA.blit(reverso, posiciones_jugador[j])
                    VENTANA.blit(reverso, posiciones_maquina[j])
                texto_anim = fuente.render("Repartiendo...", True, BLANCO)
                VENTANA.blit(texto_anim, (ANCHO // 2 - texto_anim.get_width() // 2, ALTO // 2 + 100))
                pygame.display.flip()
                pygame.time.delay(300)

            # Asignar manos y mostrar reales del jugador
            mazo = generar_mazo()
            manos = repartir_cartas(mazo)
            mano_jugador[:] = manos[0]
            mano_maquina[:] = manos[1]
            imagenes_mano[:] = [cargar_carta(c) for c in mano_jugador]
            rects_cartas.clear()
            for i, img in enumerate(imagenes_mano):
                rect = img.get_rect(topleft=posiciones_jugador[i])
                rects_cartas.append(rect)

            VENTANA.fill(VERDE_MESA)
            VENTANA.blit(reverso, (20, 20))  # Mazo
            for i, img in enumerate(imagenes_mano):
                VENTANA.blit(img, posiciones_jugador[i])
            for i in range(3):
                VENTANA.blit(reverso, posiciones_maquina[i])
            texto_anim = fuente.render("¡Listo para jugar!", True, BLANCO)
            VENTANA.blit(texto_anim, (ANCHO // 2 - texto_anim.get_width() // 2, ALTO // 2 + 100))
            pygame.display.flip()
            pygame.time.delay(800)

            puntos_mano[:] = [0, 0]
            ronda = 1
            carta_jugada_jugador = None
            carta_jugada_maquina = None
            mostrando_resultado = False
            estado = "juego"


        elif estado == "ranking":
            ranking = leer_puntajes()
            for i, (nombre, puntos) in enumerate(ranking.items()):
                texto = fuente.render(f"{nombre}: {puntos}", True, BLANCO)
                VENTANA.blit(texto, (100, 150 + i * 35))
            rect_menu = fuente.render("Menú", True, BLANCO).get_rect(topright=(ANCHO - 20, 20))
            VENTANA.blit(fuente.render("Menú", True, BLANCO), rect_menu.topleft)

        elif estado == "juego":
            VENTANA.blit(reverso, (20, 20))
            for i, img in enumerate(imagenes_mano):
                VENTANA.blit(img, posiciones_jugador[i])
            for i in range(len(mano_maquina)):
                VENTANA.blit(reverso, posiciones_maquina[i])
            if carta_jugada_jugador:
                img = cargar_carta(carta_jugada_jugador)
                VENTANA.blit(img, zona_jugada_jugador)
            if carta_jugada_maquina:
                img = cargar_carta(carta_jugada_maquina)
                VENTANA.blit(img, zona_jugada_maquina)
            if mostrando_resultado:
                texto = fuente.render(resultado_texto, True, ROJO)
                rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
                VENTANA.blit(texto, rect.topleft)
            rect_menu = fuente.render("Menú", True, BLANCO).get_rect(topright=(ANCHO - 20, 20))
            VENTANA.blit(fuente.render("Menú", True, BLANCO), rect_menu.topleft)
            texto_j = fuente.render(f"{nombre_jugador}: {puntos_jugador}", True, BLANCO)
            texto_m = fuente.render(f"Máquina: {puntos_maquina}", True, BLANCO)
            rect_j = texto_j.get_rect(bottomright=(ANCHO - 20, ALTO - 40))
            rect_m = texto_m.get_rect(bottomright=(ANCHO - 20, ALTO - 10))
            VENTANA.blit(texto_j, rect_j.topleft)
            VENTANA.blit(texto_m, rect_m.topleft)

        elif estado == "final":
            texto = fuente.render(resultado_texto, True, ROJO)
            rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
            VENTANA.blit(texto, rect.topleft)
            pygame.display.flip()
            pygame.time.delay(3000)
            estado = "menu"

        pygame.display.flip()
        reloj.tick(60)


