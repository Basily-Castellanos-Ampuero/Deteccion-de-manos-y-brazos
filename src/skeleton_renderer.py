"""
Módulo para renderizar el esqueleto detectado sobre el frame de video.
Combina la visualización de pose corporal y manos de manera coherente.
"""

import cv2
import numpy as np
from typing import Optional, Tuple, List
import config


class SkeletonRenderer:
    """
    Clase para renderizar el esqueleto de pose y manos sobre el frame de video.
    Proporciona métodos para dibujar de manera personalizada y profesional.
    """
    
    def __init__(self):
        """
        Inicializa el renderizador de esqueleto.
        """
        self.skeleton_color = config.SKELETON_COLOR
        self.hand_color = config.HAND_COLOR
        self.landmark_color = config.LANDMARK_COLOR
        self.line_thickness = config.LINE_THICKNESS
        self.landmark_radius = config.LANDMARK_RADIUS
        
        if config.DEBUG_MODE:
            print("[SkeletonRenderer] Inicializado correctamente")
    
    def draw_pose_skeleton(self, frame: np.ndarray, 
                          pose_landmarks,
                          custom_color: Optional[Tuple[int, int, int]] = None) -> np.ndarray:
        """
        Dibuja el esqueleto de pose corporal de forma personalizada.
        
        Args:
            frame: Frame donde dibujar
            pose_landmarks: Landmarks de MediaPipe Pose
            custom_color: Color personalizado (opcional)
        
        Returns:
            Frame con el esqueleto dibujado
        """
        if pose_landmarks is None:
            return frame
        
        color = custom_color if custom_color is not None else self.skeleton_color
        height, width = frame.shape[:2]
        
        # Convertir landmarks a coordenadas de píxeles
        landmarks_coords = []
        for landmark in pose_landmarks.landmark:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            visibility = landmark.visibility
            landmarks_coords.append((x, y, visibility))
        
        # Definir conexiones importantes para brazos y torso
        # Formato: (punto_inicio, punto_fin)
        connections = [
            # Torso
            (11, 12),  # Hombro izq a hombro der
            (11, 23),  # Hombro izq a cadera izq
            (12, 24),  # Hombro der a cadera der
            (23, 24),  # Cadera izq a cadera der
            
            # Brazo izquierdo
            (11, 13),  # Hombro a codo
            (13, 15),  # Codo a muñeca
            
            # Brazo derecho
            (12, 14),  # Hombro a codo
            (14, 16),  # Codo a muñeca
            
            # Manos básicas (desde muñeca)
            (15, 17),  # Muñeca izq a meñique
            (15, 19),  # Muñeca izq a índice
            (15, 21),  # Muñeca izq a pulgar
            (16, 18),  # Muñeca der a meñique
            (16, 20),  # Muñeca der a índice
            (16, 22),  # Muñeca der a pulgar
        ]
        
        # Dibujar conexiones
        if config.SHOW_CONNECTIONS:
            for connection in connections:
                start_idx, end_idx = connection
                
                # Verificar visibilidad
                if (landmarks_coords[start_idx][2] > 0.5 and 
                    landmarks_coords[end_idx][2] > 0.5):
                    
                    start_point = (landmarks_coords[start_idx][0], 
                                 landmarks_coords[start_idx][1])
                    end_point = (landmarks_coords[end_idx][0], 
                               landmarks_coords[end_idx][1])
                    
                    cv2.line(frame, start_point, end_point, 
                           color, self.line_thickness)
        
        # Dibujar landmarks
        if config.SHOW_LANDMARKS:
            for coord in landmarks_coords:
                x, y, visibility = coord
                if visibility > 0.5:  # Solo dibujar si es visible
                    cv2.circle(frame, (x, y), self.landmark_radius, 
                             self.landmark_color, -1)
                    # Círculo exterior para mejor visibilidad
                    cv2.circle(frame, (x, y), self.landmark_radius + 2, 
                             color, 2)
        
        return frame
    
    def draw_hands_skeleton(self, frame: np.ndarray,
                           multi_hand_landmarks,
                           custom_color: Optional[Tuple[int, int, int]] = None) -> np.ndarray:
        """
        Dibuja el esqueleto de las manos de forma personalizada.
        
        Args:
            frame: Frame donde dibujar
            multi_hand_landmarks: Landmarks de MediaPipe Hands
            custom_color: Color personalizado (opcional)
        
        Returns:
            Frame con el esqueleto de manos dibujado
        """
        if multi_hand_landmarks is None:
            return frame
        
        color = custom_color if custom_color is not None else self.hand_color
        height, width = frame.shape[:2]
        
        # Definir conexiones de la mano
        hand_connections = [
            # Pulgar
            (0, 1), (1, 2), (2, 3), (3, 4),
            # Índice
            (0, 5), (5, 6), (6, 7), (7, 8),
            # Medio
            (0, 9), (9, 10), (10, 11), (11, 12),
            # Anular
            (0, 13), (13, 14), (14, 15), (15, 16),
            # Meñique
            (0, 17), (17, 18), (18, 19), (19, 20),
            # Conexiones entre nudillos
            (5, 9), (9, 13), (13, 17)
        ]
        
        # Dibujar cada mano
        for hand_landmarks in multi_hand_landmarks:
            # Convertir landmarks a coordenadas
            landmarks_coords = []
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                landmarks_coords.append((x, y))
            
            # Dibujar conexiones
            if config.SHOW_CONNECTIONS:
                for connection in hand_connections:
                    start_idx, end_idx = connection
                    start_point = landmarks_coords[start_idx]
                    end_point = landmarks_coords[end_idx]
                    
                    cv2.line(frame, start_point, end_point, 
                           color, self.line_thickness)
            
            # Dibujar landmarks
            if config.SHOW_LANDMARKS:
                for coord in landmarks_coords:
                    cv2.circle(frame, coord, self.landmark_radius, 
                             self.landmark_color, -1)
                    # Círculo exterior
                    cv2.circle(frame, coord, self.landmark_radius + 2, 
                             color, 2)
        
        return frame
    
    def draw_combined_skeleton(self, frame: np.ndarray,
                              pose_landmarks,
                              multi_hand_landmarks) -> np.ndarray:
        """
        Dibuja tanto el esqueleto de pose como el de manos en un solo frame.
        
        Args:
            frame: Frame donde dibujar
            pose_landmarks: Landmarks de pose
            multi_hand_landmarks: Landmarks de manos
        
        Returns:
            Frame con ambos esqueletos dibujados
        """
        # Primero dibujar pose (más grande, va detrás)
        if config.ENABLE_POSE_DETECTION and pose_landmarks is not None:
            frame = self.draw_pose_skeleton(frame, pose_landmarks)
        
        # Luego dibujar manos (más detalladas, van delante)
        if config.ENABLE_HAND_DETECTION and multi_hand_landmarks is not None:
            frame = self.draw_hands_skeleton(frame, multi_hand_landmarks)
        
        return frame
    
    def draw_fps(self, frame: np.ndarray, fps: float,
                position: Tuple[int, int] = (10, 30)) -> np.ndarray:
        """
        Dibuja el contador de FPS en el frame.
        
        Args:
            frame: Frame donde dibujar
            fps: Valor de FPS a mostrar
            position: Posición (x, y) del texto
        
        Returns:
            Frame con FPS dibujado
        """
        if not config.SHOW_FPS:
            return frame
        
        text = f"FPS: {fps:.1f}"
        
        # Fondo semi-transparente para mejor legibilidad
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 
                                    config.TEXT_SCALE, config.TEXT_THICKNESS)[0]
        
        cv2.rectangle(frame, 
                     (position[0] - 5, position[1] - text_size[1] - 5),
                     (position[0] + text_size[0] + 5, position[1] + 5),
                     (0, 0, 0), -1)
        
        # Texto
        cv2.putText(frame, text, position,
                   cv2.FONT_HERSHEY_SIMPLEX, config.TEXT_SCALE,
                   config.TEXT_COLOR, config.TEXT_THICKNESS)
        
        return frame
    
    def draw_instructions(self, frame: np.ndarray,
                         position: Tuple[int, int] = (10, 60)) -> np.ndarray:
        """
        Dibuja instrucciones de uso en el frame.
        
        Args:
            frame: Frame donde dibujar
            position: Posición inicial (x, y) del texto
        
        Returns:
            Frame con instrucciones dibujadas
        """
        if not config.SHOW_INSTRUCTIONS:
            return frame
        
        instructions = [
            "Controles:",
            "ESC/Q - Salir",
            "S - Screenshot",
            "P - Pausar",
            "H - Toggle Manos",
            "B - Toggle Pose",
            "M - Toggle Espejo"
        ]
        
        y_offset = position[1]
        for instruction in instructions:
            cv2.putText(frame, instruction, (position[0], y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                       config.TEXT_COLOR, 1)
            y_offset += 20
        
        return frame
    
    def draw_detection_status(self, frame: np.ndarray,
                            pose_detected: bool,
                            hands_detected: int,
                            position: Tuple[int, int] = (10, 100)) -> np.ndarray:
        """
        Dibuja el estado de detección en el frame.
        
        Args:
            frame: Frame donde dibujar
            pose_detected: Si se detectó pose
            hands_detected: Número de manos detectadas
            position: Posición (x, y) del texto
        
        Returns:
            Frame con estado dibujado
        """
        # Estado de pose
        pose_status = "Pose: ✓" if pose_detected else "Pose: ✗"
        pose_color = (0, 255, 0) if pose_detected else (0, 0, 255)
        
        cv2.putText(frame, pose_status, position,
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                   pose_color, 2)
        
        # Estado de manos
        hand_status = f"Manos: {hands_detected}"
        hand_color = (0, 255, 0) if hands_detected > 0 else (0, 0, 255)
        
        cv2.putText(frame, hand_status, (position[0], position[1] + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                   hand_color, 2)
        
        return frame
    
    def add_overlay(self, frame: np.ndarray, 
                   pose_detected: bool = False,
                   hands_detected: int = 0,
                   fps: float = 0.0) -> np.ndarray:
        """
        Añade un overlay completo con toda la información relevante.
        
        Args:
            frame: Frame base
            pose_detected: Si se detectó pose
            hands_detected: Número de manos detectadas
            fps: FPS actual
        
        Returns:
            Frame con overlay completo
        """
        # FPS
        frame = self.draw_fps(frame, fps)
        
        # Estado de detección
        frame = self.draw_detection_status(frame, pose_detected, hands_detected,
                                          position=(10, frame.shape[0] - 60))
        
        # Instrucciones (esquina superior derecha)
        if config.SHOW_INSTRUCTIONS:
            frame = self.draw_instructions(frame, 
                                         position=(frame.shape[1] - 150, 30))
        
        return frame


if __name__ == "__main__":
    """
    Test básico del renderizador.
    """
    print("=" * 60)
    print("TEST DEL RENDERIZADOR DE ESQUELETO")
    print("=" * 60)
    print("Este módulo debe ser usado junto con los detectores")
    print("Ejecuta main.py para ver el renderizado en acción")