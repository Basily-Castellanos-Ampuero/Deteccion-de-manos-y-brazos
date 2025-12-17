"""
Configuraciones globales para la aplicación de detección de pose.
Todos los parámetros ajustables del sistema están centralizados aquí.
"""

# ============================================================================
# CONFIGURACIÓN DE CÁMARA
# ============================================================================
CAMERA_INDEX = 0                    # Índice de la cámara (0 = cámara predeterminada)

# ==== PERFILES DE RESOLUCIÓN ====
# Descomenta el perfil que quieras usar:

# Perfil 1: SD 4:3 (Máximo rendimiento, ~30 FPS en cualquier PC)
# CAMERA_WIDTH = 640
# CAMERA_HEIGHT = 480

# Perfil 2: HD 16:9 (Recomendado, ~25-30 FPS en PC moderna)
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

# Perfil 3: Full HD 16:9 (Máxima calidad, requiere PC potente, ~15-20 FPS)
# CAMERA_WIDTH = 1920
# CAMERA_HEIGHT = 1080

# Perfil 4: SD 16:9 (Balance para PCs antiguas)
# CAMERA_WIDTH = 854
# CAMERA_HEIGHT = 480

CAMERA_FPS = 30                     # Frames por segundo objetivo

# ============================================================================
# CONFIGURACIÓN DE DETECCIÓN DE POSE
# ============================================================================
POSE_DETECTION_CONFIDENCE = 0.5     # Confianza mínima para detectar pose (0.0 - 1.0)
POSE_TRACKING_CONFIDENCE = 0.5      # Confianza mínima para tracking (0.0 - 1.0)
POSE_MODEL_COMPLEXITY = 1           # Complejidad del modelo (0=lite, 1=full, 2=heavy)
ENABLE_POSE_DETECTION = True        # Activar/desactivar detección de pose

# ============================================================================
# CONFIGURACIÓN DE DETECCIÓN DE MANOS
# ============================================================================
HAND_DETECTION_CONFIDENCE = 0.5     # Confianza mínima para detectar manos
HAND_TRACKING_CONFIDENCE = 0.5      # Confianza mínima para tracking de manos
HAND_MODEL_COMPLEXITY = 1           # Complejidad del modelo (0 o 1)
MAX_NUM_HANDS = 2                   # Número máximo de manos a detectar
ENABLE_HAND_DETECTION = True        # Activar/desactivar detección de manos

# ============================================================================
# CONFIGURACIÓN DE VISUALIZACIÓN
# ============================================================================
# Modo espejo (flip horizontal)
MIRROR_MODE = True                  # True = modo espejo (más intuitivo)

# Colores en formato BGR (Blue, Green, Red) para OpenCV
SKELETON_COLOR = (0, 255, 0)        # Verde para el esqueleto de pose
HAND_COLOR = (255, 0, 0)            # Azul para conexiones de manos
LANDMARK_COLOR = (0, 0, 255)        # Rojo para puntos de referencia

# Grosor de líneas y tamaño de puntos
LINE_THICKNESS = 2                  # Grosor de las líneas del esqueleto
LANDMARK_RADIUS = 5                 # Radio de los círculos de landmarks

# Transparencia y overlays
SHOW_LANDMARKS = True               # Mostrar puntos de referencia
SHOW_CONNECTIONS = True             # Mostrar conexiones entre puntos
DRAW_DETECTION_BOX = False          # Dibujar caja de detección (opcional)

# ============================================================================
# CONFIGURACIÓN DE INTERFAZ
# ============================================================================
WINDOW_NAME = "capturador de brazos y manos"
SHOW_FPS = True                     # Mostrar FPS en pantalla
SHOW_INSTRUCTIONS = True            # Mostrar instrucciones en pantalla
TEXT_COLOR = (255, 255, 255)        # Blanco para texto
TEXT_SCALE = 0.6                    # Escala del texto
TEXT_THICKNESS = 2                  # Grosor del texto

# ============================================================================
# CONFIGURACIÓN DE RENDIMIENTO
# ============================================================================
ENABLE_GPU = False                  # Usar GPU si está disponible (MediaPipe)
SMOOTH_LANDMARKS = True             # Suavizar movimiento de landmarks
REFINE_FACE_LANDMARKS = False       # Refinar landmarks faciales (no necesario)

# ============================================================================
# TECLAS DE CONTROL
# ============================================================================
KEY_QUIT_ESC = 27                   # Código ASCII de ESC
KEY_QUIT_Q = ord('q')               # Tecla 'q' para salir
KEY_SCREENSHOT = ord('s')           # Tecla 's' para captura
KEY_PAUSE = ord('p')                # Tecla 'p' para pausar
KEY_TOGGLE_HANDS = ord('h')         # Tecla 'h' para toggle manos
KEY_TOGGLE_POSE = ord('b')          # Tecla 'b' para toggle pose (body)
KEY_TOGGLE_MIRROR = ord('m')        # Tecla 'm' para toggle modo espejo

# ============================================================================
# CONFIGURACIÓN DE DEPURACIÓN
# ============================================================================
DEBUG_MODE = False                  # Modo de depuración (más información en consola)
SHOW_PROCESSING_TIME = False        # Mostrar tiempo de procesamiento por frame
LOG_LEVEL = "INFO"                  # Nivel de logging: DEBUG, INFO, WARNING, ERROR