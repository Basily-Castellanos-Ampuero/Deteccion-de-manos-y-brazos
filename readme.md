# GUÍA RÁPIDA DEL PROYECTO
## Detección de Pose y Manos en Tiempo Real

---

# PARTE 1: INSTALACIÓN DESDE CERO

## Paso 0: Requisitos Previos

Antes de empezar, necesitas:
- Una computadora con Windows 10/11, Linux o Mac
- Conexión a internet (solo para instalación)
- Una webcam (integrada o USB)
- 30 minutos de tiempo

---

## Paso 1: Verificar o Instalar Python

### Windows

1. **Verificar si tienes Python:**
   ```
   Abrir CMD (Win + R, escribir "cmd", Enter)
   Escribir: python --version
   ```

2. **Si NO tienes Python o la versión es menor a 3.10:**
   - Ir a: https://www.python.org/downloads/
   - Descargar Python 3.10 o 3.11
   - Ejecutar instalador
   - IMPORTANTE: Marcar "Add Python to PATH"
   - Clic en "Install Now"

3. **Verificar instalación:**
   ```
   Abrir CMD nuevamente
   Escribir: python --version
   Debe mostrar: Python 3.10.x o Python 3.11.x
   ```

### Linux (Ubuntu/Debian)

```bash
# Verificar Python
python3 --version

# Si no tienes Python 3.10/3.11, instalar:
sudo apt update
sudo apt install python3.10 python3-pip python3-venv

# Instalar dependencias del sistema
sudo apt install libgl1-mesa-glx
```

### Mac

```bash
# Verificar Python
python3 --version

# Si no tienes Python 3.10/3.11, instalar con Homebrew:
brew install python@3.10
```

---

## Paso 2: Descargar el Proyecto

1. **Descargar el archivo ZIP del proyecto**
2. **Extraer en una ubicación fácil de encontrar**
   - Ejemplo Windows: `C:\Users\TuUsuario\Documents\pose_detection_project`
   - Ejemplo Linux/Mac: `~/Documents/pose_detection_project`

3. **Verificar que tienes esta estructura:**
   ```
   pose_detection_project/
   ├── src/
   ├── utils/
   ├── install.bat
   ├── run.bat
   ├── requirements.txt
   └── ... (otros archivos)
   ```

---

## Paso 3: Instalación Automática (RECOMENDADO)

### Windows

1. **Abrir la carpeta del proyecto**
2. **Doble clic en `install.bat`**
3. **Esperar 2-5 minutos** (descarga e instala todo automáticamente)
4. **Verás mensajes como:**
   ```
   [OK] Python encontrado
   Creando entorno virtual...
   Instalando dependencias...
   INSTALACION COMPLETADA CON EXITO
   ```

### Linux/Mac

1. **Abrir Terminal**
2. **Navegar al proyecto:**
   ```bash
   cd ~/Documents/pose_detection_project
   ```
3. **Dar permisos:**
   ```bash
   chmod +x install.sh run.sh
   ```
4. **Ejecutar instalador:**
   ```bash
   ./install.sh
   ```
5. **Esperar a que termine**

---

## Paso 4: Instalación Manual (Si la automática falla)

### Windows

```cmd
# 1. Abrir CMD en la carpeta del proyecto
cd C:\Users\TuUsuario\Documents\pose_detection_project

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
venv\Scripts\activate

# 4. Actualizar pip
python -m pip install --upgrade pip

# 5. Instalar dependencias
pip install -r requirements.txt

# Esperar 2-3 minutos
```

### Linux/Mac

```bash
# 1. Navegar al proyecto
cd ~/Documents/pose_detection_project

# 2. Crear entorno virtual
python3 -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate

# 4. Actualizar pip
pip install --upgrade pip

# 5. Instalar dependencias
pip install -r requirements.txt
```

---

## Paso 5: Primera Ejecución

### Windows

**Opción A: Con script (más fácil)**
```
Doble clic en: run.bat
```

**Opción B: Manual**
```cmd
# 1. Abrir CMD en la carpeta del proyecto
cd C:\Users\TuUsuario\Documents\pose_detection_project

# 2. Activar entorno virtual
venv\Scripts\activate

# 3. Ejecutar
python start.py
```

### Linux/Mac

**Opción A: Con script**
```bash
./run.sh
```

**Opción B: Manual**
```bash
# 1. Navegar al proyecto
cd ~/Documents/pose_detection_project

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Ejecutar
python start.py
```

---

## Paso 6: Verificar que Funciona

Deberías ver:
```
========================================
APLICACIÓN DE DETECCIÓN DE POSE Y MANOS
========================================
✓ Aplicación inicializada

Inicializando componentes...
  ✓ Cámara inicializada: (1280, 720)
  ✓ Detector de pose listo
  ✓ Detector de manos listo
  ✓ Renderizador listo

CONTROLES
========================================
  ESC o Q  - Salir
  S        - Screenshot
  P        - Pausar
  H        - Toggle manos
  B        - Toggle pose
  M        - Toggle espejo
========================================

Presiona Enter para iniciar...
```

**Presiona Enter y la ventana con tu cámara se abrirá**

---

## Problemas Comunes en la Instalación

### Error: "python no se reconoce como comando"
**Solución:** Python no está en el PATH
```
Reinstalar Python marcando "Add Python to PATH"
O agregar manualmente: C:\Python310 al PATH del sistema
```

### Error: "No se pudo abrir la cámara"
**Solución:**
```
1. Cerrar Zoom, Teams, Skype
2. Verificar que la cámara funciona en otra app
3. Probar cambiar CAMERA_INDEX en src/config.py
```

### Error: "pip: comando no encontrado"
**Solución:**
```
python -m pip install --upgrade pip
O en Linux/Mac: python3 -m pip install --upgrade pip
```

### La instalación se queda trabada
**Solución:**
```
Ctrl+C para cancelar
Verificar conexión a internet
Intentar de nuevo
```

---

# PARTE 2: QUÉ ES Y CÓMO FUNCIONA

## ¿Qué hace esta aplicación?

Es un programa que usa tu cámara web para:
1. **Detectar tu cuerpo** - Identifica 33 puntos como hombros, codos, muñecas
2. **Detectar tus manos** - Identifica 21 puntos por mano (dedos, nudillos)
3. **Dibujar un esqueleto** - Muestra líneas conectando los puntos sobre el video
4. **Todo en tiempo real** - 25-30 imágenes por segundo

---

## Tecnologías Usadas

### 1. Python 3.10/3.11
**Qué es:** Lenguaje de programación
**Para qué:** Base de toda la aplicación

### 2. OpenCV (opencv-python)
**Qué es:** Biblioteca de visión por computadora
**Para qué:** 
- Capturar video de la cámara
- Mostrar la ventana
- Dibujar líneas y círculos

### 3. MediaPipe
**Qué es:** Framework de Google con inteligencia artificial
**Para qué:**
- Detectar dónde está tu cuerpo
- Detectar dónde están tus manos
- Usa modelos de aprendizaje automático

### 4. NumPy
**Qué es:** Biblioteca matemática
**Para qué:** Operaciones con imágenes (son matrices de números)

---

## Cómo Funciona (Simplificado)

```
1. CAPTURA
   Cámara → Toma una foto (frame)
   
2. PROCESAMIENTO
   Frame → Se convierte a formato RGB
   Frame → Se analiza con inteligencia artificial
   
3. DETECCIÓN
   IA encuentra:
   - 33 puntos del cuerpo
   - Hasta 42 puntos de manos (21 por mano)
   
4. DIBUJO
   Se dibujan:
   - Líneas verdes conectando puntos del cuerpo
   - Líneas azules conectando puntos de manos
   - Círculos rojos en cada punto
   
5. MOSTRAR
   Frame final → Se muestra en ventana
   
6. REPETIR
   Este proceso ocurre 25-30 veces por segundo
```

---

## Algoritmos Principales

### BlazePose (Detección de Cuerpo)

**Cómo funciona:**
1. **Paso 1:** Encuentra dónde hay una persona en la imagen
2. **Paso 2:** Enfoca esa región y encuentra los 33 puntos exactos

**Por qué es rápido:**
- No analiza toda la imagen cada vez
- Solo analiza donde ya sabe que hay una persona
- Usa modelos optimizados (TensorFlow Lite)

**Los 33 puntos detectados:**
```
Cabeza: nariz, ojos, orejas (11 puntos)
Brazos: hombros, codos, muñecas (10 puntos)
Torso: caderas (2 puntos)
Piernas: rodillas, tobillos (10 puntos)
```

### MediaPipe Hands (Detección de Manos)

**Cómo funciona:**
1. **Paso 1:** Detecta la palma de la mano (más fácil que dedos)
2. **Paso 2:** Encuentra los 21 puntos de cada mano

**Los 21 puntos por mano:**
```
1 muñeca
4 puntos × 5 dedos = 20 puntos
Total: 21 puntos por mano
```

---

## Arquitectura del Sistema

```
┌─────────────────┐
│  TU (Usuario)   │
│  Presionas      │
│  teclas         │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   main.py               │
│   (Cerebro del sistema) │
│   Coordina todo         │
└──┬──────────┬───────┬───┘
   │          │       │
   ▼          ▼       ▼
┌─────┐  ┌───────┐  ┌───────┐
│Cámara│ │Pose   │  │Manos  │
│      │ │Detector│  │Detector│
└─────┘  └───────┘  └───────┘
   │          │         │
   │          │         │
   └──────────┴─────────┘
              │
              ▼
      ┌──────────────┐
      │ Renderizador │
      │ (Dibuja)     │
      └──────┬───────┘
             │
             ▼
      ┌──────────────┐
      │   PANTALLA   │
      │  Ves el      │
      │  resultado   │
      └──────────────┘
```

---

## Archivos del Proyecto (Qué hace cada uno)

### Carpeta src/ (código principal)

**main.py** (330 líneas)
- El cerebro del sistema
- Coordina todo
- Maneja el loop principal

**config.py** (160 líneas)
- Todas las configuraciones
- Resolución, colores, sensibilidad
- Cambiar comportamiento sin tocar código

**camera_handler.py** (230 líneas)
- Maneja la cámara
- Captura frames
- Libera recursos

**pose_detector.py** (380 líneas)
- Detecta la pose del cuerpo
- Usa MediaPipe Pose
- Retorna 33 puntos

**hand_detector.py** (380 líneas)
- Detecta las manos
- Usa MediaPipe Hands
- Retorna hasta 42 puntos

**skeleton_renderer.py** (340 líneas)
- Dibuja el esqueleto
- Añade información en pantalla
- Colores y estilos

### Carpeta utils/

**drawing_utils.py** (280 líneas)
- Funciones auxiliares
- Calcular ángulos, distancias
- Guardar screenshots

### Archivos de instalación

**install.bat / install.sh**
- Instala todo automáticamente

**run.bat / run.sh**
- Ejecuta la aplicación

**start.py**
- Launcher alternativo

**requirements.txt**
- Lista de dependencias a instalar

---

# PARTE 3: CÓMO USAR LA APLICACIÓN

## Controles del Teclado

| Tecla | Qué hace | Ejemplo |
|-------|----------|---------|
| **ESC** | Salir de la aplicación | Cierra todo |
| **Q** | Salir de la aplicación | Alternativa a ESC |
| **S** | Tomar screenshot | Guarda imagen en screenshots/ |
| **P** | Pausar/Reanudar | Congela la imagen |
| **H** | Activar/desactivar manos | Ver solo cuerpo |
| **B** | Activar/desactivar cuerpo | Ver solo manos |
| **M** | Modo espejo ON/OFF | Cambiar orientación |

---

## Información en Pantalla

```
┌─────────────────────────────────────────┐
│ FPS: 28.5          Controles:           │
│                    ESC/Q - Salir        │
│                    S - Screenshot       │
│        [VIDEO DE LA CÁMARA]             │
│        [CON ESQUELETO DIBUJADO]         │
│                                         │
│ Pose: ✓  Manos: 2                       │
└─────────────────────────────────────────┘
```

**FPS:** Cuadros por segundo (velocidad)
- 25-30 = Muy bien
- 15-20 = Aceptable
- <10 = Muy lento (reducir resolución)

**Pose: ✓ (verde)** = Detecta tu cuerpo
**Pose: ✗ (rojo)** = No detecta tu cuerpo

**Manos: 0** = No detecta manos
**Manos: 1** = Detecta una mano
**Manos: 2** = Detecta ambas manos

---

## Colores del Esqueleto

**Líneas verdes** = Conexiones del cuerpo
**Líneas azules** = Conexiones de las manos
**Círculos rojos** = Puntos detectados

---

## Tips para Mejor Detección

### Iluminación
- Luz frontal (de frente a ti)
- Evitar contraluz (ventana atrás)
- Iluminación uniforme

### Fondo
- Simple y limpio
- Evitar muchos objetos
- Sin otras personas

### Distancia
- **Para pose:** 1.5 - 2.5 metros de la cámara
- **Para manos:** 0.5 - 1.5 metros de la cámara

### Ropa
- Evitar ropa del mismo color que tu piel
- Manga corta para mejor detección de brazos
- Colores con contraste

### Posición
- Estar centrado en la cámara
- Cuerpo completo visible (para pose)
- Manos dentro del cuadro (para manos)

---

# PARTE 4: CONFIGURACIÓN PERSONALIZADA

## Archivo config.py

Ubicación: `src/config.py`

### Cambiar Resolución de Cámara

Abre `src/config.py` y busca:

```python
# Resolución actual (HD 16:9)
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
```

**Opciones:**

```python
# Máximo rendimiento (4:3)
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Balance (16:9) - ACTUAL
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

# Máxima calidad (16:9)
CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080
```

### Cambiar Colores

```python
# Formato: (Azul, Verde, Rojo)

# Esqueleto del cuerpo
SKELETON_COLOR = (0, 255, 0)    # Verde

# Manos
HAND_COLOR = (255, 0, 0)        # Azul

# Puntos
LANDMARK_COLOR = (0, 0, 255)    # Rojo
```

**Otros colores:**
```python
(0, 0, 255)     # Rojo
(255, 0, 0)     # Azul
(0, 255, 0)     # Verde
(255, 255, 0)   # Cian
(255, 0, 255)   # Magenta
(0, 255, 255)   # Amarillo
(255, 255, 255) # Blanco
```

### Optimizar para PC Lenta

```python
# Reducir resolución
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Modelo más simple
POSE_MODEL_COMPLEXITY = 0
HAND_MODEL_COMPLEXITY = 0

# Detectar solo 1 mano
MAX_NUM_HANDS = 1

# Menor sensibilidad
POSE_DETECTION_CONFIDENCE = 0.4
HAND_DETECTION_CONFIDENCE = 0.4
```

### Modo Espejo

```python
# True = como espejo (más intuitivo)
# False = vista real de cámara
MIRROR_MODE = True
```

---

# PARTE 5: SOLUCIÓN DE PROBLEMAS RÁPIDA

## Problema: Cámara no abre

```
1. Cerrar Zoom, Teams, Skype, Discord
2. Verificar que la cámara funciona en otra app
3. En config.py cambiar:
   CAMERA_INDEX = 0  # Probar 0, 1, 2
```

## Problema: FPS muy bajo (<10)

```
En config.py:

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
POSE_MODEL_COMPLEXITY = 0
MAX_NUM_HANDS = 1
```

## Problema: No detecta bien

```
- Mejorar iluminación (luz de frente)
- Fondo más simple
- Distancia correcta (1.5-2m)
- Activar suavizado:
  SMOOTH_LANDMARKS = True
```

## Problema: Error "ModuleNotFoundError"

```
Activar entorno virtual:

Windows: venv\Scripts\activate
Linux/Mac: source venv/bin/activate

Reinstalar: pip install -r requirements.txt
```

## Problema: Ventana no aparece

```
Windows: Alt+Tab para buscar ventana
Linux: sudo apt install libgl1-mesa-glx
```

---

# PARTE 6: PARA LA EXPOSICIÓN

## Presentación de 10 Minutos

### Minuto 1: Introducción
"Hemos creado una aplicación que detecta el movimiento del cuerpo y manos en tiempo real usando inteligencia artificial"

### Minutos 2-4: Demostración
- Ejecutar la aplicación
- Mostrar detección de cuerpo
- Mostrar detección de manos
- Probar controles (P, S, H, B)

### Minutos 5-7: Tecnologías
- Python 3.10
- OpenCV (captura video)
- MediaPipe (inteligencia artificial de Google)
- 25-30 FPS en tiempo real

### Minuto 8: Aplicaciones
- Entrenamiento físico
- Rehabilitación
- Análisis de movimiento
- Juegos y aplicaciones interactivas

### Minutos 9-10: Resultados y Conclusiones
- Funciona en tiempo real
- 33 puntos de cuerpo + 42 de manos
- Código modular (2,000+ líneas)
- Fácil de instalar y usar

---

## Script de Demostración

**Antes de empezar:**
```
"Voy a mostrar la aplicación funcionando en vivo"
```

**Ejecutar:**
```
python start.py
[Esperar a que se abra]
```

**Mostrar cuerpo:**
```
"Aquí ven en verde el esqueleto de mi cuerpo"
[Mover brazos, agacharse]
"Detecta 33 puntos en tiempo real"
```

**Mostrar manos:**
```
"Las líneas azules son mis manos"
[Mover dedos, hacer gestos]
"21 puntos por mano, hasta 2 manos"
```

**Mostrar controles:**
```
"Presiono P para pausar..."
[Pausa]
"S para tomar una foto..."
[Screenshot]
"M para cambiar modo espejo..."
[Toggle]
```

**Cerrar:**
```
"Y ESC para salir"
[Salir]
```

---

## Preguntas Frecuentes

**¿Funciona sin internet?**
Sí, totalmente offline

**¿Detecta múltiples personas?**
No, solo una persona

**¿Se pueden grabar videos?**
Screenshots sí, video es mejora futura

**¿Qué tan preciso es?**
95%+ en buenas condiciones

**¿Funciona en PC antigua?**
Sí, reduciendo resolución

**¿Cuánto tardó el desarrollo?**
[Adaptar] Investigación + 2,000 líneas de código

---

## Puntos Fuertes a Destacar

1. Funciona en tiempo real (25-30 FPS)
2. Usa tecnología de Google (MediaPipe)
3. Fácil de instalar (scripts automáticos)
4. Código bien organizado (modular)
5. Múltiples aplicaciones prácticas
6. Documentación completa

---

# RESUMEN EJECUTIVO

## Qué Instalar

```
Python 3.10 o 3.11
opencv-python==4.8.1.78
mediapipe==0.10.9
numpy==1.24.3
```

## Cómo Instalar

```
Windows: Doble clic en install.bat
Linux/Mac: ./install.sh
```

## Cómo Ejecutar

```
Windows: Doble clic en run.bat
Linux/Mac: ./run.sh
O: python start.py
```

## Qué Hace

```
Detecta:
- 33 puntos del cuerpo
- 21 puntos por mano (hasta 2 manos)
- En tiempo real (25-30 FPS)
- Dibuja esqueleto sobre video
```

## Tecnologías

```
Python + OpenCV + MediaPipe + NumPy
Algoritmos: BlazePose + MediaPipe Hands
Framework: TensorFlow Lite
```

## Aplicaciones

```
- Fitness y entrenamiento
- Rehabilitación física
- Análisis de movimiento
- Interfaces gestuales
```

---

# COMANDOS DE REFERENCIA RÁPIDA

## Instalación

```bash
# Verificar Python
python --version

# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
# Opción 1
python start.py

# Opción 2
python src/main.py

# Opción 3 (Windows)
run.bat

# Opción 3 (Linux/Mac)
./run.sh
```

## Verificar Instalación

```python
import cv2
import mediapipe as mp
import numpy as np

print(f"OpenCV: {cv2.__version__}")
print(f"MediaPipe: {mp.__version__}")
print(f"NumPy: {np.__version__}")
```

---

**FIN DE LA GUÍA RÁPIDA**

Para más detalles, consulta los otros documentos:
- DOCUMENTACION_TECNICA_COMPLETA.md (versión extendida)
- README.md (información general)
- TECHNICAL_INFO.md (detalles técnicos avanzados)
