"""
Módulo para el manejo de la cámara web.
Gestiona la captura de video, configuración y liberación de recursos.
"""

import cv2
import sys
from typing import Optional, Tuple
import config


class CameraHandler:
    """
    Clase para gestionar la captura de video desde la cámara web.
    """
    
    def __init__(self, camera_index: int = None, width: int = None, height: int = None):
        """
        Inicializa el manejador de cámara.
        
        Args:
            camera_index: Índice de la cámara (0 por defecto)
            width: Ancho de captura en píxeles
            height: Alto de captura en píxeles
        """
        self.camera_index = camera_index if camera_index is not None else config.CAMERA_INDEX
        self.width = width if width is not None else config.CAMERA_WIDTH
        self.height = height if height is not None else config.CAMERA_HEIGHT
        self.fps = config.CAMERA_FPS
        
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_opened = False
        
        if config.DEBUG_MODE:
            print(f"[CameraHandler] Inicializando con índice: {self.camera_index}")
            print(f"[CameraHandler] Resolución objetivo: {self.width}x{self.height}")
    
    def initialize(self) -> bool:
        """
        Inicializa la cámara web y configura sus parámetros.
        
        Returns:
            bool: True si la inicialización fue exitosa, False en caso contrario
        """
        try:
            # Intentar abrir la cámara
            self.cap = cv2.VideoCapture(self.camera_index)
            
            if not self.cap.isOpened():
                print(f"Error: No se pudo abrir la cámara con índice {self.camera_index}")
                return False
            
            # Configurar resolución
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Verificar resolución real
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            
            if config.DEBUG_MODE:
                print(f"Camara inicializada correctamente")
                print(f"   Resolución real: {actual_width}x{actual_height}")
                print(f"   FPS: {actual_fps}")
            
            self.is_opened = True
            return True
            
        except Exception as e:
            print(f"Error al inicializar la cámara: {str(e)}")
            return False
    
    def read_frame(self) -> Tuple[bool, Optional[cv2.Mat]]:
        """
        Lee un frame de la cámara.
        
        Returns:
            Tuple[bool, Optional[cv2.Mat]]: 
                - success: True si se leyó correctamente
                - frame: Imagen capturada (None si falló)
        """
        if not self.is_opened or self.cap is None:
            print("Advertencia: La cámara no está inicializada")
            return False, None
        
        success, frame = self.cap.read()
        
        if not success:
            print("Advertencia: No se pudo leer el frame")
            return False, None
        
        return True, frame
    
    def get_frame_dimensions(self) -> Tuple[int, int]:
        """
        Obtiene las dimensiones del frame actual.
        
        Returns:
            Tuple[int, int]: (width, height)
        """
        if self.cap is None:
            return 0, 0
        
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height
    
    def get_fps(self) -> int:
        """
        Obtiene los FPS de la cámara.
        
        Returns:
            int: FPS de la cámara
        """
        if self.cap is None:
            return 0
        
        return int(self.cap.get(cv2.CAP_PROP_FPS))
    
    def is_camera_opened(self) -> bool:
        """
        Verifica si la cámara está abierta y funcionando.
        
        Returns:
            bool: True si la cámara está abierta
        """
        return self.is_opened and self.cap is not None and self.cap.isOpened()
    
    def release(self):
        """
        Libera los recursos de la cámara.
        """
        if self.cap is not None:
            self.cap.release()
            self.is_opened = False
            
            if config.DEBUG_MODE:
                print("[CameraHandler] Cámara liberada")
    
    def __enter__(self):
        """
        Soporte para context manager (with statement).
        """
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Limpieza automática al salir del context manager.
        """
        self.release()
    
    def __del__(self):
        """
        Destructor para asegurar que se liberen recursos.
        """
        self.release()


def test_camera(camera_index: int = 0, duration_seconds: int = 5):
    """
    Función de prueba para verificar que la cámara funciona correctamente.
    
    Args:
        camera_index: Índice de la cámara a probar
        duration_seconds: Duración de la prueba en segundos
    """
    print(f"Probando cámara con índice {camera_index}...")
    print(f"   La ventana se cerrará automáticamente en {duration_seconds} segundos")
    print("   O presiona 'q' para salir antes")
    
    camera = CameraHandler(camera_index=camera_index)
    
    if not camera.initialize():
        print("Error: No se pudo inicializar la cámara")
        return
    
    print("camara inicializada correctamente")
    print(f"   Dimensiones: {camera.get_frame_dimensions()}")
    print(f"   FPS: {camera.get_fps()}")
    
    frame_count = 0
    max_frames = duration_seconds * 30  # Aproximado
    
    while frame_count < max_frames:
        success, frame = camera.read_frame()
        
        if not success:
            print("Error al leer frame")
            break
        
        # Agregar información al frame
        cv2.putText(frame, f"Frame: {frame_count}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "Presiona 'q' para salir", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow("Test de Cámara", frame)
        
        # Esperar 1ms y verificar si se presionó 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Test interrumpido por el usuario")
            break
        
        frame_count += 1
    
    camera.release()
    cv2.destroyAllWindows()
    print(f"Test completado. Frames capturados: {frame_count}")


if __name__ == "__main__":
    """
    Ejecutar test de cámara si se ejecuta este archivo directamente.
    """
    print("=" * 60)
    print("TEST DE CÁMARA WEB")
    print("=" * 60)
    test_camera(camera_index=0, duration_seconds=5)