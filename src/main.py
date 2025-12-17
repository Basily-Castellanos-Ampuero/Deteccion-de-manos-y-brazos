"""
Aplicación principal de detección de pose y manos.
Coordina todos los componentes y maneja el loop principal.
"""

import cv2
import sys
import time
from datetime import datetime
import os

# Importar módulos propios
import config
from camera_handler import CameraHandler
from pose_detector import PoseDetector
from hand_detector import HandDetector
from skeleton_renderer import SkeletonRenderer

# Importar utilidades
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.drawing_utils import save_screenshot


class PoseDetectionApp:
    """
    Aplicación principal de detección de pose y manos.
    Coordina todos los componentes y maneja el ciclo de vida.
    """
    
    def __init__(self):
        """
        Inicializa la aplicación y todos sus componentes.
        """
        print("=" * 60)
        print("aplicacion de deteccion de brazos y manos")
        print("=" * 60)
        
        # Componentes principales
        self.camera = None
        self.pose_detector = None
        self.hand_detector = None
        self.renderer = None
        
        # Estado de la aplicación
        self.is_running = False
        self.is_paused = False
        self.frame_count = 0
        self.fps = 0.0
        self.fps_history = []
        
        # Control de tiempo para FPS
        self.prev_time = 0
        self.current_time = 0
        
        # Estado de detección
        self.pose_detected = False
        self.hands_detected = 0
        
        # Directorio para screenshots
        self.screenshot_dir = os.path.join(
            os.path.dirname(__file__), '..', 'screenshots'
        )
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        print(" Aplicación inicializada")
    
    def initialize_components(self) -> bool:
        """
        Inicializa todos los componentes necesarios.
        
        Returns:
            bool: True si todos los componentes se inicializaron correctamente
        """
        print("\n Inicializando componentes...")
        
        try:
            # Inicializar cámara
            print("   • Inicializando cámara...")
            self.camera = CameraHandler()
            if not self.camera.initialize():
                print("    Error: No se pudo inicializar la cámara")
                return False
            print(f"    Cámara inicializada: {self.camera.get_frame_dimensions()}")
            
            # Inicializar detector de pose
            if config.ENABLE_POSE_DETECTION:
                print("   • Inicializando detector de pose...")
                self.pose_detector = PoseDetector()
                print("    Detector de pose listo")
            else:
                print("     Detector de pose desactivado")
            
            # Inicializar detector de manos
            if config.ENABLE_HAND_DETECTION:
                print("   • Inicializando detector de manos...")
                self.hand_detector = HandDetector()
                print("    Detector de manos listo")
            else:
                print("     Detector de manos desactivado")
            
            # Inicializar renderizador
            print("   • Inicializando renderizador...")
            self.renderer = SkeletonRenderer()
            print("    Renderizador listo")
            
            print("\n Todos los componentes inicializados correctamente")
            return True
            
        except Exception as e:
            print(f"\nError al inicializar componentes: {str(e)}")
            return False
    
    def process_frame(self, frame):
        """
        Procesa un frame: detecta pose y manos, y renderiza el resultado.
        
        Args:
            frame: Frame de video a procesar
        
        Returns:
            Frame procesado con visualizaciones
        """
        # Aplicar modo espejo si está habilitado
        if config.MIRROR_MODE:
            frame = cv2.flip(frame, 1)  # 1 = flip horizontal
        
        # Resetear estado de detección
        self.pose_detected = False
        self.hands_detected = 0
        
        pose_landmarks = None
        hand_landmarks = None
        
        # Detectar pose
        if config.ENABLE_POSE_DETECTION and self.pose_detector:
            self.pose_detected = self.pose_detector.detect(frame)
            if self.pose_detected:
                pose_landmarks = self.pose_detector.get_landmarks()
        
        # Detectar manos
        if config.ENABLE_HAND_DETECTION and self.hand_detector:
            hands_found = self.hand_detector.detect(frame)
            if hands_found:
                self.hands_detected = self.hand_detector.get_num_hands_detected()
                hand_landmarks = self.hand_detector.get_hands_landmarks()
        
        # Renderizar esqueleto combinado
        if pose_landmarks or hand_landmarks:
            frame = self.renderer.draw_combined_skeleton(
                frame, pose_landmarks, hand_landmarks
            )
        
        # Añadir overlay con información
        frame = self.renderer.add_overlay(
            frame,
            pose_detected=self.pose_detected,
            hands_detected=self.hands_detected,
            fps=self.fps
        )
        
        return frame
    
    def calculate_fps(self):
        """
        Calcula los FPS actuales.
        """
        self.current_time = time.time()
        
        if self.prev_time != 0:
            time_diff = self.current_time - self.prev_time
            if time_diff > 0:
                self.fps = 1.0 / time_diff
                self.fps_history.append(self.fps)
                
                # Mantener solo los últimos 30 valores
                if len(self.fps_history) > 30:
                    self.fps_history.pop(0)
        
        self.prev_time = self.current_time
    
    def handle_key_events(self, key: int) -> bool:
        """
        Maneja los eventos de teclado.
        
        Args:
            key: Código de la tecla presionada
        
        Returns:
            bool: False si se debe salir de la aplicación
        """
        # Salir (ESC o Q)
        if key == config.KEY_QUIT_ESC or key == config.KEY_QUIT_Q:
            print("\n Saliendo de la aplicación...")
            return False
        
        # Capturar screenshot (S)
        elif key == config.KEY_SCREENSHOT:
            self.capture_screenshot()
        
        # Pausar/Reanudar (P)
        elif key == config.KEY_PAUSE:
            self.is_paused = not self.is_paused
            status = "PAUSADO" if self.is_paused else "REANUDADO"
            print(f"{status}")
        
        # Toggle detector de manos (H)
        elif key == config.KEY_TOGGLE_HANDS:
            config.ENABLE_HAND_DETECTION = not config.ENABLE_HAND_DETECTION
            status = "activado" if config.ENABLE_HAND_DETECTION else "desactivado"
            print(f"  Detector de manos {status}")
        
        # Toggle detector de pose (B)
        elif key == config.KEY_TOGGLE_POSE:
            config.ENABLE_POSE_DETECTION = not config.ENABLE_POSE_DETECTION
            status = "activado" if config.ENABLE_POSE_DETECTION else "desactivado"
            print(f"Detector de pose {status}")
        
        # Toggle modo espejo (M)
        elif key == config.KEY_TOGGLE_MIRROR:
            config.MIRROR_MODE = not config.MIRROR_MODE
            status = "activado" if config.MIRROR_MODE else "desactivado"
            print(f" Modo espejo {status}")
        
        return True
    
    def capture_screenshot(self):
        """
        Captura y guarda un screenshot del frame actual.
        """
        if not hasattr(self, 'last_frame') or self.last_frame is None:
            print("⚠️  No hay frame disponible para capturar")
            return
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        
        # Guardar screenshot
        if save_screenshot(self.last_frame, filepath):
            print(f" Screenshot guardado: {filename}")
        else:
            print(" Error al guardar screenshot")
    
    def print_instructions(self):
        """
        Imprime las instrucciones de uso en la consola.
        """
        print("\n" + "=" * 60)
        print("  CONTROLES")
        print("=" * 60)
        print("  ESC o Q  - Salir de la aplicación")
        print("  S        - Capturar screenshot")
        print("  P        - Pausar/Reanudar")
        print("  H        - Activar/Desactivar detección de manos")
        print("  B        - Activar/Desactivar detección de pose (Body)")
        print("  M        - Activar/Desactivar modo espejo (Mirror)")
        print("=" * 60)
        print("\n Presiona cualquier tecla para iniciar...")
        input()
    
    def run(self):
        """
        Ejecuta el loop principal de la aplicación.
        """
        # Inicializar componentes
        if not self.initialize_components():
            print("❌ Error: No se pudieron inicializar los componentes")
            return
        
        # Mostrar instrucciones
        self.print_instructions()
        
        # Iniciar aplicación
        self.is_running = True
        print("\n Iniciando detección...")
        print("   (La ventana se abrirá en breve)")
        
        # Frame para guardar último frame (para screenshots)
        self.last_frame = None
        
        try:
            while self.is_running:
                # Leer frame de la cámara
                success, frame = self.camera.read_frame()
                
                if not success:
                    print("  Error al leer frame de la cámara")
                    break
                
                # Calcular FPS
                self.calculate_fps()
                
                # Procesar frame si no está pausado
                if not self.is_paused:
                    frame = self.process_frame(frame)
                    self.frame_count += 1
                else:
                    # Mostrar texto de pausa
                    cv2.putText(frame, "PAUSADO - Presiona P para continuar",
                              (50, frame.shape[0] // 2),
                              cv2.FONT_HERSHEY_SIMPLEX, 1,
                              (0, 0, 255), 3)
                
                # Guardar frame actual
                self.last_frame = frame.copy()
                
                # Mostrar frame
                cv2.imshow(config.WINDOW_NAME, frame)
                
                # Manejar eventos de teclado (esperar 1ms)
                key = cv2.waitKey(1) & 0xFF
                if key != 255:  # Si se presionó alguna tecla
                    if not self.handle_key_events(key):
                        break
                
                # Mostrar estadísticas cada 100 frames
                if config.DEBUG_MODE and self.frame_count % 100 == 0:
                    print(f"Frame: {self.frame_count} | FPS: {self.fps:.1f} | "
                          f"Pose: {'✓' if self.pose_detected else '✗'} | "
                          f"Manos: {self.hands_detected}")
        
        except KeyboardInterrupt:
            print("\n Interrupción por teclado (Ctrl+C)")
        
        except Exception as e:
            print(f"\n Error durante la ejecución: {str(e)}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """
        Limpia y libera todos los recursos.
        """
        print("\nLimpiando recursos...")
        
        # Cerrar ventanas
        cv2.destroyAllWindows()
        
        # Liberar cámara
        if self.camera:
            self.camera.release()
            print("   Cámara liberada")
        
        # Liberar detectores
        if self.pose_detector:
            self.pose_detector.close()
            print("   Detector de pose cerrado")
        
        if self.hand_detector:
            self.hand_detector.close()
            print("   Detector de manos cerrado")
        
        # Mostrar estadísticas finales
        print("\n" + "=" * 60)
        print("ESTADÍSTICAS FINALES")
        print("=" * 60)
        print(f"  Frames procesados: {self.frame_count}")
        if self.fps_history:
            avg_fps = sum(self.fps_history) / len(self.fps_history)
            print(f"  FPS promedio: {avg_fps:.2f}")
        print("=" * 60)
        
        print("\nAplicación finalizada correctamente")


def main():
    """
    Función principal de entrada.
    """
    try:
        app = PoseDetectionApp()
        app.run()
    except Exception as e:
        print(f"\nError fatal: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()