# Sistema de Vigilancia Entomológica (MosqVision AI)

El **Sistema de Vigilancia Entomológica** es una plataforma end-to-end basada en Visión Computacional con Deep Learning, diseñada para automatizar y agilizar la clasificación taxonómica de mosquitos vectores de enfermedades (Aedes, Anopheles y Culex). 

Este proyecto fue desarrollado como entrega final para la materia de *Visión Computacional con Deep Learning* y aborda directamente el problema logístico de los retrasos en cercos epidemiológicos, permitiendo que operarios de campo realicen inferencias precisas mediante un módulo de integración clínica ligero.

## 🎯 El Problema y la Solución
**El problema:** Las confirmaciones taxonómicas de los vectores del Dengue y la Malaria suelen requerir la recolección presencial del espécimen y su transporte a microscopía centralizada. Esto retrasa enormemente la declaración de cercos epidemiológicos locales.

**La solución mediante Visión Computacional:** Nuestro pipeline permite reducir esa brecha trasladando el diagnóstico a una arquitectura de Red Neuronal Convolucional (CNN) Regularizada (~99.6% accuracy local). El sistema procesa lotes fotográficos y entrega instantáneamente un reporte del vector y su potencial patógeno de forma remota.

---

## 🛠️ Diseño del Pipeline del Sistema

1. **Entrada de datos (Operario):** Captura fotográfica del espécimen mediante el *Frontend*. Puede ser inferencia individual o masiva (Lote).
2. **Preprocesamiento (Backend FastAPI):**
   - Recepción multipart y conversión de bytes.
   - Redimensionamiento paramétrico estricto (`128x128 píxeles`).
   - Normalización de espectro de luz para combatir la alta entropía visual del campo.
3. **Inferencia (ML PyTorch):** 
   - La matriz normalizada es consumida por el modelo ganador `cnn_regularized.pth`.
   - Se procesan funciones de activación `Dropout` para lidiar con oclusiones ambientales.
4. **Respuesta Epidemiólogica:** El núcleo de lógica clínica empareja la clase con su patógeno (*Aedes* -> Dengue/Zika | *Anopheles* -> Malaria) y retorna una acción operativa crítica.
5. **Dashboard Analítico:** Presentación visual con badges de priorización.

---

## 🚀 Guía de Instalación y Despliegue (Local)

### 1. Requisitos Previos
- Python 3.9 o superior.
- Git.

### 2. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

### 3. Crear el entorno virtual e instalar dependencias
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate
# En Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
```

### 4. Levantar la API
```bash
python -m uvicorn backend.main:app --reload
```
Ingresa a `http://localhost:8000/static/index.html` en tu navegador para ver la Interfaz Gráfica.

---

##  Guía de Despliegue Paso a Paso (Render.com)
Este proyecto está optimizado para desplegarse fácilmente en servicios gratuitos como **Render**:

1. Crea un repositorio en [GitHub](https://github.com/) (puede ser privado o público).
2. Sube esta carpeta al repositorio (gracias al archivo `.gitignore` configurado, los datasets pesados no se subirán, ahorrando espacio).
3. Entra a [Render](https://render.com/), crea una cuenta y da clic en **New > Web Service**.
4. Vincula tu cuenta de GitHub y selecciona el repositorio que acabas de subir.
5. Configura los siguientes parámetros en Render:
   - **Language:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6. Haz clic en **Create Web Service**. ¡Espera unos minutos y tendrás una URL pública para compartir tu proyecto en la sustentación!

---

##  El Modelo: Resultados Cuestionables frente al Mundo Real
Durante el desarrollo se realizó un modelado escalonado utilizando MLflow. Se construyeron:
- SVM manual con descriptores HOG (94.6%).
- CNN Base pura (99.3%, con grave sobreajuste).
- **CNN Regularizada (99.6%, modelo victorioso y en producción).**

**Análisis Crítico:** 
Si bien el modelo tiene un *accuracy* impecable de laboratorio, al enfrentarse a imágenes crudas del entorno abierto (internet), evidencia confusión (especialmente hacia el vector *Anopheles*). 
Esto demuestra un **sesgo de dominio natural**: `MosqVision-3K` posée fotografías con higiene clínica de fondo blanco; mientras que el mundo de despliegue sufre variaciones extremas de fondo (piel, selva, texturas de ropa). Por ende, el trabajo a futuro exige estrictamente el re-entrenamiento del pipeline incorporando _data augmentation_ basada en ambientes asimétricos verdaderos en conjunción con redes de segmentación tipo YOLO.

---
**Desarrollado para:** Visión Computacional con Deep Learning
**Autor:** Juan Felipe Plata Barbosa