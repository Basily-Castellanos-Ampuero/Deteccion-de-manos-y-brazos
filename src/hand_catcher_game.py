"""
Minijuego de captura de figuras con detección de manos.
Demuestra la aplicación práctica de la detección de pose y manos.
"""

import cv2
import numpy as np
import random
import time
from typing import List, Tuple, Optional
import config


class Figure:
    """
    Representa una figura que cae desde arriba.
    """
    
    def __init__(self, x: int, y: int, figure_type: str, speed: float):
        """
        Inicializa una figura.
        
        Args:
            x: Posición X inicial
            y: Posición Y inicial
            figure_type: Tipo de figura ('circle' o 'square')
            speed: Velocidad de caída en píxeles por frame
        """
        self.x = x
        self.y = y
        self.type = figure_type  # 'circle' o 'square'
        self.speed = speed
        self.size = 50  # Tamaño de la figura
        self.active = True
        
        # Color según tipo
        if self.type == 'circle':
            self.color = (0, 255, 255)  # Amarillo (círculos = mano abierta)
        else:
            self.color = (255, 0, 255)  # Magenta (cuadrados = mano cerrada)
    
    def update(self):
        """Actualiza la posición de la figura."""
        self.y += self.speed
    
    def draw(self, frame):
        """
        Dibuja la figura en el frame.
        
        Args:
            frame: Frame donde dibujar
        """
        if not self.active:
            return
        
        center = (int(self.x), int(self.y))
        
        if self.type == 'circle':
            # Dibujar círculo
            cv2.circle(frame, center, self.size, self.color, -1)
            cv2.circle(frame, center, self.size, (255, 255, 255), 3)
            # Icono de mano abierta
            cv2.putText(frame, "OPEN", (int(self.x) - 30, int(self.y) + 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        else:
            # Dibujar cuadrado
            top_left = (int(self.x) - self.size, int(self.y) - self.size)
            bottom_right = (int(self.x) + self.size, int(self.y) + self.size)
            cv2.rectangle(frame, top_left, bottom_right, self.color, -1)
            cv2.rectangle(frame, top_left, bottom_right, (255, 255, 255), 3)
            # Icono de mano cerrada
            cv2.putText(frame, "FIST", (int(self.x) - 25, int(self.y) + 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    def is_out_of_bounds(self, height: int) -> bool:
        """
        Verifica si la figura salió de la pantalla.
        
        Args:
            height: Alto de la pantalla
            
        Returns:
            bool: True si salió de la pantalla
        """
        return self.y > height + self.size
    
    def check_collision(self, hand_x: int, hand_y: int, collision_radius: int = 80) -> bool:
        """
        Verifica si la mano colisionó con la figura.
        
        Args:
            hand_x: Posición X de la mano
            hand_y: Posición Y de la mano
            collision_radius: Radio de colisión
            
        Returns:
            bool: True si hay colisión
        """
        if not self.active:
            return False
        
        # Calcular distancia
        distance = np.sqrt((self.x - hand_x)**2 + (self.y - hand_y)**2)
        return distance < (self.size + collision_radius)


class HandCatcherGame:
    """
    Minijuego de captura de figuras con las manos.
    """
    
    def __init__(self, frame_width: int, frame_height: int):
        """
        Inicializa el juego.
        
        Args:
            frame_width: Ancho del frame
            frame_height: Alto del frame
        """
        self.width = frame_width
        self.height = frame_height
        
        # Estado del juego
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.paused = False
        
        # Figuras activas
        self.figures: List[Figure] = []
        
        # Timing
        self.last_spawn_time = time.time()
        self.spawn_interval = 2.0  # Segundos entre spawns
        
        # Velocidad base
        self.base_speed = 3.0
        
        # Contador de frames
        self.frame_count = 0
        
        # Estado de la mano
        self.hand_open = False
        self.hand_closed = False
        
        print("Minijuego iniciado!")
        print("Círculos amarillos = Atrapar con mano ABIERTA")
        print("Cuadrados magenta = Atrapar con mano CERRADA")
        print("Presiona G para activar/desactivar el juego")
    
    def is_hand_open(self, hand_landmarks) -> bool:
        """
        Detecta si la mano está abierta.
        
        Args:
            hand_landmarks: Landmarks de la mano
            
        Returns:
            bool: True si la mano está abierta
        """
        if hand_landmarks is None:
            return False
        
        # Verificar que los dedos estén extendidos
        # Comparar punta del dedo con su articulación base
        
        # Índice (landmarks 5-8)
        index_extended = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
        
        # Medio (landmarks 9-12)
        middle_extended = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
        
        # Anular (landmarks 13-16)
        ring_extended = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
        
        # Meñique (landmarks 17-20)
        pinky_extended = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y
        
        # Mano abierta = al menos 3 dedos extendidos
        extended_count = sum([index_extended, middle_extended, ring_extended, pinky_extended])
        
        return extended_count >= 3
    
    def is_hand_closed(self, hand_landmarks) -> bool:
        """
        Detecta si la mano está cerrada (puño).
        
        Args:
            hand_landmarks: Landmarks de la mano
            
        Returns:
            bool: True si la mano está cerrada
        """
        if hand_landmarks is None:
            return False
        
        # Verificar que los dedos estén doblados
        # Las puntas deben estar cerca de la palma
        
        # Índice
        index_closed = hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y
        
        # Medio
        middle_closed = hand_landmarks.landmark[12].y > hand_landmarks.landmark[10].y
        
        # Anular
        ring_closed = hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y
        
        # Meñique
        pinky_closed = hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y
        
        # Mano cerrada = al menos 3 dedos doblados
        closed_count = sum([index_closed, middle_closed, ring_closed, pinky_closed])
        
        return closed_count >= 3
    
    def spawn_figure(self):
        """Crea una nueva figura en posición aleatoria."""
        # Posición X aleatoria (evitar bordes)
        x = random.randint(100, self.width - 100)
        y = -50  # Arriba de la pantalla
        
        # Tipo aleatorio
        figure_type = random.choice(['circle', 'square'])
        
        # Velocidad aumenta con el score
        speed = self.base_speed + (self.score * 0.1)
        
        # Crear y agregar figura
        figure = Figure(x, y, figure_type, speed)
        self.figures.append(figure)
    
    def update(self, hand_landmarks_list):
        """
        Actualiza el estado del juego.
        
        Args:
            hand_landmarks_list: Lista de landmarks de manos detectadas
        """
        if self.game_over or self.paused:
            return
        
        self.frame_count += 1
        
        # Spawn de nuevas figuras
        current_time = time.time()
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_figure()
            self.last_spawn_time = current_time
            
            # Reducir intervalo gradualmente (hacer más difícil)
            self.spawn_interval = max(0.8, 2.0 - (self.score * 0.05))
        
        # Obtener estado de la mano (primera mano detectada)
        if hand_landmarks_list and len(hand_landmarks_list) > 0:
            hand_landmarks = hand_landmarks_list[0]
            
            # Detectar estado
            self.hand_open = self.is_hand_open(hand_landmarks)
            self.hand_closed = self.is_hand_closed(hand_landmarks)
            
            # Obtener posición de la muñeca (landmark 0)
            wrist = hand_landmarks.landmark[0]
            hand_x = int(wrist.x * self.width)
            hand_y = int(wrist.y * self.height)
            
            # Verificar colisiones
            for figure in self.figures:
                if not figure.active:
                    continue
                
                if figure.check_collision(hand_x, hand_y):
                    # Verificar si el gesto es correcto
                    if figure.type == 'circle' and self.hand_open:
                        # Correcto: círculo con mano abierta
                        self.score += 10
                        figure.active = False
                        print(f"¡BIEN! +10 puntos. Score: {self.score}")
                    elif figure.type == 'square' and self.hand_closed:
                        # Correcto: cuadrado con mano cerrada
                        self.score += 10
                        figure.active = False
                        print(f"¡BIEN! +10 puntos. Score: {self.score}")
                    elif self.hand_open or self.hand_closed:
                        # Incorrecto: gesto equivocado
                        self.lives -= 1
                        figure.active = False
                        print(f"¡ERROR! Gesto incorrecto. Vidas: {self.lives}")
                        
                        if self.lives <= 0:
                            self.game_over = True
                            print(f"GAME OVER! Score final: {self.score}")
        
        # Actualizar figuras
        figures_to_remove = []
        for figure in self.figures:
            if not figure.active:
                figures_to_remove.append(figure)
                continue
            
            figure.update()
            
            # Verificar si salió de la pantalla
            if figure.is_out_of_bounds(self.height):
                self.lives -= 1
                figures_to_remove.append(figure)
                print(f"¡Figura perdida! Vidas: {self.lives}")
                
                if self.lives <= 0:
                    self.game_over = True
                    print(f"GAME OVER! Score final: {self.score}")
        
        # Remover figuras inactivas
        for figure in figures_to_remove:
            self.figures.remove(figure)
    
    def draw(self, frame):
        """
        Dibuja el juego en el frame.
        
        Args:
            frame: Frame donde dibujar
        """
        # Dibujar todas las figuras
        for figure in self.figures:
            figure.draw(frame)
        
        # Dibujar HUD (Head-Up Display)
        self.draw_hud(frame)
        
        # Dibujar indicador de estado de mano
        self.draw_hand_status(frame)
        
        # Dibujar mensaje de game over si aplica
        if self.game_over:
            self.draw_game_over(frame)
        
        if self.paused:
            self.draw_paused(frame)
    
    def draw_hud(self, frame):
        """Dibuja la interfaz de usuario (HUD)."""
        # Fondo semi-transparente para el HUD
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (300, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        
        # Score
        cv2.putText(frame, f"SCORE: {self.score}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Vidas (corazones)
        lives_text = "LIVES: " + "♥ " * self.lives
        cv2.putText(frame, lives_text, (20, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        # Velocidad actual
        speed_text = f"Speed: {self.base_speed + (self.score * 0.1):.1f}"
        cv2.putText(frame, speed_text, (20, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    def draw_hand_status(self, frame):
        """Dibuja el estado actual de la mano."""
        x = self.width - 250
        y = 50
        
        if self.hand_open:
            status = "MANO ABIERTA"
            color = (0, 255, 255)  # Amarillo
        elif self.hand_closed:
            status = "MANO CERRADA"
            color = (255, 0, 255)  # Magenta
        else:
            status = "..."
            color = (150, 150, 150)  # Gris
        
        cv2.putText(frame, status, (x, y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    def draw_game_over(self, frame):
        """Dibuja mensaje de game over."""
        # Fondo semi-transparente
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, self.height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Texto GAME OVER
        text = "GAME OVER"
        font_scale = 2.5
        thickness = 4
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, font_scale, thickness)
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2 - 50
        
        cv2.putText(frame, text, (x, y),
                   cv2.FONT_HERSHEY_DUPLEX, font_scale, (0, 0, 255), thickness)
        
        # Score final
        score_text = f"Score: {self.score}"
        font_scale = 1.5
        thickness = 3
        (text_width, text_height), _ = cv2.getTextSize(score_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2 + 50
        
        cv2.putText(frame, score_text, (x, y),
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness)
        
        # Instrucciones
        instruction = "Presiona R para reiniciar o G para salir"
        font_scale = 0.8
        thickness = 2
        (text_width, text_height), _ = cv2.getTextSize(instruction, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2 + 120
        
        cv2.putText(frame, instruction, (x, y),
                   cv2.FONT_HERSHEY_SIMPLEX, font_scale, (200, 200, 200), thickness)
    
    def draw_paused(self, frame):
        """Dibuja mensaje de pausa."""
        text = "PAUSADO"
        font_scale = 2
        thickness = 3
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, font_scale, thickness)
        
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2
        
        # Fondo
        cv2.rectangle(frame, (x - 20, y - text_height - 10), 
                     (x + text_width + 20, y + 20), (0, 0, 0), -1)
        
        cv2.putText(frame, text, (x, y),
                   cv2.FONT_HERSHEY_DUPLEX, font_scale, (255, 255, 0), thickness)
    
    def reset(self):
        """Reinicia el juego."""
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.paused = False
        self.figures.clear()
        self.last_spawn_time = time.time()
        self.spawn_interval = 2.0
        self.frame_count = 0
        print("\n¡Juego reiniciado!")
    
    def toggle_pause(self):
        """Alterna entre pausar y reanudar."""
        self.paused = not self.paused
        print("Juego pausado" if self.paused else "Juego reanudado")