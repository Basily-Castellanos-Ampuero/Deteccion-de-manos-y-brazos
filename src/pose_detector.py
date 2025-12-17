"""
Módulo para la detección de pose corporal usando MediaPipe.
Detecta 33 puntos de referencia del cuerpo, incluyendo brazos, hombros y torso.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, List, Tuple
import config


class PoseDetector:
    """
    Clase para detectar la pose corporal usando MediaPipe Pose.
    Se enfoca principalmente en la detección de brazos y parte superior del cuerpo.
    """
    
    def __init__(self):
        """
        Inicializa el detector de pose con MediaPipe.
        """
        # Inicializar MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Crear el objeto Pose con configuraciones
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,  # False para video en tiempo real
            model_complexity=config.POSE_MODEL_COMPLEXITY,
            smooth_landmarks=config.SMOOTH_LANDMARKS,
            enable_segmentation=False,  # No necesitamos segmentación
            min_detection_confidence=config.POSE_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.POSE_TRACKING_CONFIDENCE
        )
        
        self.results = None
        self.landmarks = None
        
        if config.DEBUG_MODE:
            print("[PoseDetector] Inicializado correctamente")
            print(f"   Complejidad del modelo: {config.POSE_MODEL_COMPLEXITY}")
            print(f"   Confianza de detección: {config.POSE_DETECTION_CONFIDENCE}")
    
    def detect(self, frame: np.ndarray) -> bool:
        """
        Detecta la pose en un frame.
        
        Args:
            frame: Frame de video en formato BGR (OpenCV)
        
        Returns:
            bool: True si se detectó una pose, False en caso contrario
        """
        if frame is None:
            return False
        
        # Convertir BGR a RGB (MediaPipe usa RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Mejorar rendimiento marcando la imagen como no escribible
        frame_rgb.flags.writeable = False
        
        # Procesar el frame
        self.results = self.pose.process(frame_rgb)
        
        # Restaurar flag
        frame_rgb.flags.writeable = True
        
        # Verificar si se detectó alguna pose
        if self.results.pose_landmarks:
            self.landmarks = self.results.pose_landmarks
            return True
        else:
            self.landmarks = None
            return False
    
    def get_landmarks(self):
        """
        Obtiene los landmarks detectados.
        
        Returns:
            Landmarks de la pose o None si no se detectó nada
        """
        return self.landmarks
    
    def get_landmark_coordinates(self, frame_shape: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Convierte landmarks normalizados a coordenadas de píxeles.
        
        Args:
            frame_shape: (height, width) del frame
        
        Returns:
            Lista de tuplas (x, y) con coordenadas en píxeles, o None
        """
        if self.landmarks is None:
            return None
        
        height, width = frame_shape[:2]
        coordinates = []
        
        for landmark in self.landmarks.landmark:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            coordinates.append((x, y))
        
        return coordinates
    
    def get_specific_landmarks(self, landmark_indices: List[int], 
                             frame_shape: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Obtiene coordenadas de landmarks específicos.
        
        Args:
            landmark_indices: Lista de índices de landmarks a obtener
            frame_shape: (height, width) del frame
        
        Returns:
            Lista de coordenadas (x, y) o None
        """
        if self.landmarks is None:
            return None
        
        height, width = frame_shape[:2]
        coordinates = []
        
        for idx in landmark_indices:
            if 0 <= idx < len(self.landmarks.landmark):
                landmark = self.landmarks.landmark[idx]
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                coordinates.append((x, y))
            else:
                coordinates.append(None)
        
        return coordinates
    
    def get_arm_landmarks(self, frame_shape: Tuple[int, int]) -> dict:
        """
        Obtiene los landmarks específicos de los brazos.
        
        Args:
            frame_shape: (height, width) del frame
        
        Returns:
            Diccionario con landmarks de brazos organizados
        """
        if self.landmarks is None:
            return {}
        
        # Índices de MediaPipe Pose para brazos
        # 11: Hombro izquierdo, 12: Hombro derecho
        # 13: Codo izquierdo, 14: Codo derecho
        # 15: Muñeca izquierda, 16: Muñeca derecha
        # 17: Meñique izquierdo, 18: Meñique derecho
        # 19: Índice izquierdo, 20: Índice derecho
        # 21: Pulgar izquierdo, 22: Pulgar derecho
        
        arm_indices = {
            'left_shoulder': 11,
            'right_shoulder': 12,
            'left_elbow': 13,
            'right_elbow': 14,
            'left_wrist': 15,
            'right_wrist': 16,
            'left_pinky': 17,
            'right_pinky': 18,
            'left_index': 19,
            'right_index': 20,
            'left_thumb': 21,
            'right_thumb': 22
        }
        
        height, width = frame_shape[:2]
        arm_coords = {}
        
        for name, idx in arm_indices.items():
            landmark = self.landmarks.landmark[idx]
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            visibility = landmark.visibility
            arm_coords[name] = {'position': (x, y), 'visibility': visibility}
        
        return arm_coords
    
    def is_landmark_visible(self, landmark_index: int, threshold: float = 0.5) -> bool:
        """
        Verifica si un landmark específico es visible.
        
        Args:
            landmark_index: Índice del landmark
            threshold: Umbral de visibilidad (0.0 - 1.0)
        
        Returns:
            bool: True si el landmark es visible
        """
        if self.landmarks is None:
            return False
        
        if 0 <= landmark_index < len(self.landmarks.landmark):
            return self.landmarks.landmark[landmark_index].visibility > threshold
        
        return False
    
    def get_pose_confidence(self) -> float:
        """
        Calcula la confianza promedio de la detección de pose.
        
        Returns:
            float: Confianza promedio (0.0 - 1.0)
        """
        if self.landmarks is None:
            return 0.0
        
        total_visibility = sum(lm.visibility for lm in self.landmarks.landmark)
        avg_visibility = total_visibility / len(self.landmarks.landmark)
        
        return avg_visibility
    
    def draw_landmarks(self, frame: np.ndarray, 
                      draw_connections: bool = True,
                      draw_landmarks: bool = True) -> np.ndarray:
        """
        Dibuja los landmarks de pose en el frame.
        
        Args:
            frame: Frame donde dibujar
            draw_connections: Si dibujar las conexiones entre landmarks
            draw_landmarks: Si dibujar los puntos de landmarks
        
        Returns:
            Frame con los landmarks dibujados
        """
        if self.landmarks is None:
            return frame
        
        # Usar las utilidades de dibujo de MediaPipe
        if draw_connections and config.SHOW_CONNECTIONS:
            self.mp_drawing.draw_landmarks(
                frame,
                self.landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        elif draw_landmarks and config.SHOW_LANDMARKS:
            # Dibujar solo los landmarks sin conexiones
            self.mp_drawing.draw_landmarks(
                frame,
                self.landmarks,
                None,  # Sin conexiones
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        
        return frame
    
    def close(self):
        """
        Libera recursos del detector.
        """
        if self.pose:
            self.pose.close()
            if config.DEBUG_MODE:
                print("[PoseDetector] Recursos liberados")
    
    def __del__(self):
        """
        Destructor para asegurar liberación de recursos.
        """
        self.close()


# Constantes útiles para índices de landmarks
class PoseLandmarks:
    """
    Clase con constantes para los índices de landmarks de MediaPipe Pose.
    Útil para referencia rápida.
    """
    # Cara
    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10
    
    # Brazos y hombros
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    
    # Manos (puntos de referencia básicos)
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    
    # Torso
    LEFT_HIP = 23
    RIGHT_HIP = 24
    
    # Piernas (para referencia, aunque no son el foco)
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32


if __name__ == "__main__":
    """
    Test básico del detector de pose.
    """
    print("=" * 60)
    print("TEST DEL DETECTOR DE POSE")
    print("=" * 60)
    print("Este módulo debe ser usado junto con camera_handler.py")
    print("Ejecuta main.py para ver la detección en acción")