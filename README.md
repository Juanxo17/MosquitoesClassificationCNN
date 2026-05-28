# Sistema de Vigilancia Entomológica (MosqVision AI)

El **Sistema de Vigilancia Entomológica** es una plataforma end-to-end basada en Visión Computacional con Deep Learning, diseñada para automatizar y agilizar la clasificación taxonómica de mosquitos vectores de enfermedades (Aedes, Anopheles y Culex). 

Este proyecto fue desarrollado como entrega final para la materia de *Visión Computacional con Deep Learning* y aborda directamente el problema logístico de los retrasos en cercos epidemiológicos, permitiendo que operarios de campo realicen inferencias precisas mediante un módulo de integración clínica ligero.

## El Problema y la Solución
**El problema:** Las confirmaciones taxonómicas de los vectores del Dengue y la Malaria suelen requerir la recolección presencial del espécimen y su transporte a microscopía centralizada. Esto retrasa enormemente la declaración de cercos epidemiológicos locales.

**La solución mediante Visión Computacional:** Nuestro pipeline permite reducir esa brecha trasladando el diagnóstico a una arquitectura de Red Neuronal Convolucional (CNN) Regularizada (~99.6% accuracy local). El sistema procesa lotes fotográficos y entrega instantáneamente un reporte del vector y su potencial patógeno de forma remota.

## Diseño del Pipeline del Sistema

1. **Entrada de datos:** Captura fotográfica del espécimen proporcionada mediante la interfaz web (Frontend). Puede ser inferencia individual o masiva (Lote).
2. **Preprocesamiento (Backend FastAPI):**
   - Recepción multipart y conversión de bytes.
   - Redimensionamiento paramétrico estricto (128x128 píxeles).
   - Normalización de espectro de luz para estandarizar las entradas frente a variaciones de iluminación.
3. **Inferencia (ML PyTorch):** 
   - La matriz normalizada es consumida por el modelo en producción (CNN Regularizada).
4. **Respuesta Epidemiológica:** El núcleo de lógica clínica empareja la especie detectada con su patógeno (Aedes -> Dengue/Zika | Anopheles -> Malaria) y retorna la recomendación de acción operativa.
5. **Panel Analítico:** Presentación visual con categorización y semaforización de riesgo.

## Análisis Crítico de Resultados
Durante el desarrollo se realizó un modelado iterativo y registro de experimentos (MLflow):
- SVM manual con descriptores HOG (94.6% de accuracy en prueba).
- CNN de arquitectura Base (99.3% de accuracy, con sobreajuste agudo evidenciado en métricas de entrenamiento).
- **CNN Regularizada (99.6% de accuracy, modelo final para producción).**

Si bien el modelo tiene un *accuracy* alto sobre el conjunto de prueba aislado, al procesar imágenes no controladas (entorno de campo con fondos heterogéneos) evidencia pérdida de precisión (particularmente sub-clasificando Anopheles). Esto evidencia directamente un fuerte **sesgo de dominio**: el dataset de entrenamiento (MosqVision-3K) está compuesto en gran medida por fotografías macro con higiene clínica y fondos controlados. En contraste, el entorno real presenta alta oclusión, suciedad y varianza lumínica extrema. Un escalamiento futuro obligará a introducir técnicas de *Domain Adaptation*, segmentación de sujeto focal, y recolección de muestras *in-the-wild* para robustecer la extracción de características frente al ruido.

## Ejecución del Proyecto

1. Instalar las dependencias requeridas ubicadas en el archivo requirements.
`ash
pip install -r requirements.txt
`

2. Ejecutar el servidor Uvicorn apuntando al backend principal.
`ash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
`

3. Acceder al sistema localmente a través de un navegador web en la ruta de archivos estáticos:
http://localhost:8000/static/index.html

---
**Asignatura:** Visión Computacional con Deep Learning
**Docente:** Nicolas Llanos Neuta
**Estudiante:** Juan Felipe Plata Barbosa
