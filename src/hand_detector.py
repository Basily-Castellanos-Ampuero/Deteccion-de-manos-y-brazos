"""
Módulo para la detección de manos usando MediaPipe.
Detecta hasta 2 manos con 21 puntos de referencia cada una.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, List, Tuple, Dict
import config


class HandDetector:
    """
    Clase para detectar manos usando MediaPipe Hands.
    Puede detectar hasta 2 manos simultáneamente con 21 landmarks cada una.
    """
    
    def __init__(self):
        """
        Inicializa el detector de manos con MediaPipe.
        """
        # Inicializar MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Crear el objeto Hands con configuraciones
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,  # False para video en tiempo real
            max_num_hands=config.MAX_NUM_HANDS,
            model_complexity=config.HAND_MODEL_COMPLEXITY,
            min_detection_confidence=config.HAND_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.HAND_TRACKING_CONFIDENCE
        )
        
        self.results = None
        self.multi_hand_landmarks = None
        self.multi_handedness = None
        
        if config.DEBUG_MODE:
            print("[HandDetector] Inicializado correctamente")
            print(f"   Máximo de manos: {config.MAX_NUM_HANDS}")
            print(f"   Complejidad del modelo: {config.HAND_MODEL_COMPLEXITY}")
            print(f"   Confianza de detección: {config.HAND_DETECTION_CONFIDENCE}")
    
    def detect(self, frame: np.ndarray) -> bool:
        """
        Detecta manos en un frame.
        
        Args:
            frame: Frame de video en formato BGR (OpenCV)
        
        Returns:
            bool: True si se detectó al menos una mano, False en caso contrario
        """
        if frame is None:
            return False
        
        # Convertir BGR a RGB (MediaPipe usa RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Mejorar rendimiento marcando la imagen como no escribible
        frame_rgb.flags.writeable = False
        
        # Procesar el frame
        self.results = self.hands.process(frame_rgb)
        
        # Restaurar flag
        frame_rgb.flags.writeable = True
        
        # Verificar si se detectaron manos
        if self.results.multi_hand_landmarks:
            self.multi_hand_landmarks = self.results.multi_hand_landmarks
            self.multi_handedness = self.results.multi_handedness
            return True
        else:
            self.multi_hand_landmarks = None
            self.multi_handedness = None
            return False
    
    def get_num_hands_detected(self) -> int:
        """
        Obtiene el número de manos detectadas.
        
        Returns:
            int: Número de manos detectadas (0-2)
        """
        if self.multi_hand_landmarks is None:
            return 0
        return len(self.multi_hand_landmarks)
    
    def get_hands_landmarks(self) -> Optional[List]:
        """
        Obtiene los landmarks de todas las manos detectadas.
        
        Returns:
            Lista de landmarks por mano o None
        """
        return self.multi_hand_landmarks
    
    def get_hand_coordinates(self, hand_index: int, 
                           frame_shape: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Convierte landmarks de una mano específica a coordenadas de píxeles.
        
        Args:
            hand_index: Índice de la mano (0 o 1)
            frame_shape: (height, width) del frame
        
        Returns:
            Lista de tuplas (x, y) con coordenadas en píxeles, o None
        """
        if self.multi_hand_landmarks is None or hand_index >= len(self.multi_hand_landmarks):
            return None
        
        height, width = frame_shape[:2]
        coordinates = []
        
        hand_landmarks = self.multi_hand_landmarks[hand_index]
        
        for landmark in hand_landmarks.landmark:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            coordinates.append((x, y))
        
        return coordinates
    
    def get_hand_label(self, hand_index: int) -> Optional[str]:
        """
        Obtiene la etiqueta de la mano (Left o Right).
        
        Args:
            hand_index: Índice de la mano (0 o 1)
        
        Returns:
            'Left', 'Right' o None
        """
        if self.multi_handedness is None or hand_index >= len(self.multi_handedness):
            return None
        
        # MediaPipe devuelve la lateralidad desde la perspectiva de la persona
        # no desde la perspectiva de la cámara
        handedness = self.multi_handedness[hand_index]
        return handedness.classification[0].label
    
    def get_hand_confidence(self, hand_index: int) -> float:
        """
        Obtiene la confianza de detección de una mano específica.
        
        Args:
            hand_index: Índice de la mano (0 o 1)
        
        Returns:
            float: Confianza (0.0 - 1.0)
        """
        if self.multi_handedness is None or hand_index >= len(self.multi_handedness):
            return 0.0
        
        handedness = self.multi_handedness[hand_index]
        return handedness.classification[0].score
    
    def get_all_hands_info(self, frame_shape: Tuple[int, int]) -> List[Dict]:
        """
        Obtiene información completa de todas las manos detectadas.
        
        Args:
            frame_shape: (height, width) del frame
        
        Returns:
            Lista de diccionarios con información de cada mano
        """
        if self.multi_hand_landmarks is None:
            return []
        
        hands_info = []
        
        for i in range(len(self.multi_hand_landmarks)):
            hand_info = {
                'index': i,
                'label': self.get_hand_label(i),
                'confidence': self.get_hand_confidence(i),
                'coordinates': self.get_hand_coordinates(i, frame_shape),
                'landmarks': self.multi_hand_landmarks[i]
            }
            hands_info.append(hand_info)
        
        return hands_info
    
    def get_finger_tips(self, hand_index: int, 
                       frame_shape: Tuple[int, int]) -> Optional[Dict[str, Tuple[int, int]]]:
        """
        Obtiene las coordenadas de las puntas de los dedos de una mano.
        
        Args:
            hand_index: Índice de la mano (0 o 1)
            frame_shape: (height, width) del frame
        
        Returns:
            Diccionario con coordenadas de cada punta de dedo o None
        """
        coordinates = self.get_hand_coordinates(hand_index, frame_shape)
        
        if coordinates is None:
            return None
        
        # Índices de las puntas de los dedos en MediaPipe Hands
        finger_tips = {
            'thumb': coordinates[HandLandmarks.THUMB_TIP],
            'index': coordinates[HandLandmarks.INDEX_FINGER_TIP],
            'middle': coordinates[HandLandmarks.MIDDLE_FINGER_TIP],
            'ring': coordinates[HandLandmarks.RING_FINGER_TIP],
            'pinky': coordinates[HandLandmarks.PINKY_TIP]
        }
        
        return finger_tips
    
    def draw_landmarks(self, frame: np.ndarray,
                      draw_connections: bool = True) -> np.ndarray:
        """
        Dibuja los landmarks de las manos en el frame.
        
        Args:
            frame: Frame donde dibujar
            draw_connections: Si dibujar las conexiones entre landmarks
        
        Returns:
            Frame con los landmarks dibujados
        """
        if self.multi_hand_landmarks is None:
            return frame
        
        # Dibujar cada mano detectada
        for hand_landmarks in self.multi_hand_landmarks:
            if draw_connections and config.SHOW_CONNECTIONS:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
            elif config.SHOW_LANDMARKS:
                # Dibujar solo los landmarks sin conexiones
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    None,  # Sin conexiones
                    self.mp_drawing_styles.get_default_hand_landmarks_style()
                )
        
        return frame
    
    def draw_hand_info(self, frame: np.ndarray, 
                      hand_index: int,
                      position: Tuple[int, int] = (10, 30)) -> np.ndarray:
        """
        Dibuja información de una mano en el frame.
        
        Args:
            frame: Frame donde dibujar
            hand_index: Índice de la mano
            position: Posición (x, y) donde dibujar el texto
        
        Returns:
            Frame con la información dibujada
        """
        label = self.get_hand_label(hand_index)
        confidence = self.get_hand_confidence(hand_index)
        
        if label is None:
            return frame
        
        text = f"Hand {hand_index + 1}: {label} ({confidence:.2f})"
        cv2.putText(frame, text, position,
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                   config.TEXT_COLOR, config.TEXT_THICKNESS)
        
        return frame
    
    def close(self):
        """
        Libera recursos del detector.
        """
        if self.hands:
            self.hands.close()
            if config.DEBUG_MODE:
                print("[HandDetector] Recursos liberados")
    
    def __del__(self):
        """
        Destructor para asegurar liberación de recursos.
        """
        self.close()


class HandLandmarks:
    """
    Clase con constantes para los índices de landmarks de MediaPipe Hands.
    Cada mano tiene 21 landmarks organizados por dedo.
    """
    # Muñeca
    WRIST = 0
    
    # Pulgar (Thumb)
    THUMB_CMC = 1      # Carpo-metacarpiano
    THUMB_MCP = 2      # Metacarpo-falángico
    THUMB_IP = 3       # Interfalángico
    THUMB_TIP = 4      # Punta
    
    # Índice (Index Finger)
    INDEX_FINGER_MCP = 5
    INDEX_FINGER_PIP = 6
    INDEX_FINGER_DIP = 7
    INDEX_FINGER_TIP = 8
    
    # Medio (Middle Finger)
    MIDDLE_FINGER_MCP = 9
    MIDDLE_FINGER_PIP = 10
    MIDDLE_FINGER_DIP = 11
    MIDDLE_FINGER_TIP = 12
    
    # Anular (Ring Finger)
    RING_FINGER_MCP = 13
    RING_FINGER_PIP = 14
    RING_FINGER_DIP = 15
    RING_FINGER_TIP = 16
    
    # Meñique (Pinky)
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20


if __name__ == "__main__":
    """
    Test básico del detector de manos.
    """
    print("=" * 60)
    print("TEST DEL DETECTOR DE MANOS")
    print("=" * 60)
    print("Este módulo debe ser usado junto con camera_handler.py")
    print("Ejecuta main.py para ver la detección en acción")