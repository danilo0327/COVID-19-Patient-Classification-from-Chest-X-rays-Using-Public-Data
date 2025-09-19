# COVID-19 Patient Classification from Chest X-rays

Aplicación FastAPI para clasificar pacientes con COVID-19, Opacidad Pulmonar, Neumonía Viral o Normal a partir de rayos X del tórax usando modelos de deep learning.

## 🏥 Características

- **Clasificación automática** de rayos X en 4 categorías:
  - COVID-19
  - Opacidad Pulmonar (Lung Opacity)
  - Neumonía Viral (Viral Pneumonia)
  - Normal
- **API REST** con FastAPI
- **Interfaz web** para subir imágenes
- **Modelo ResNet18** entrenado con PyTorch
- **Documentación automática** en `/docs`

## 📋 Requisitos

### Dependencias del Sistema
- Python 3.10+
- pip
- Git

### Dependencias de Python
Ver `covid_app/requirements.txt` para la lista completa de dependencias.

## 🚀 Instalación Local

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd COVID-19-Patient-Classification-from-Chest-X-rays-Using-Public-Data
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r covid_app/requirements.txt
```

### 4. Ejecutar la aplicación
```bash
cd covid_app
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

La aplicación estará disponible en: `http://localhost:8001`

## 🌐 Despliegue en la Nube

### Opción 1: AWS Elastic Beanstalk (Recomendado)

#### Preparación:
1. **Crear archivo de entrada**:
```bash
# Crear application.py en el directorio raíz
echo 'from covid_app.app.main import app
application = app' > application.py
```

2. **Crear configuración EB**:
```bash
mkdir .ebextensions
```

Crear `.ebextensions/python.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: application.py
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
  aws:elasticbeanstalk:container:python:staticfiles:
    "/static": "covid_app/app/static"
```

3. **Copiar requirements.txt**:
```bash
cp covid_app/requirements.txt requirements.txt
```

#### Despliegue:
1. **Crear archivo ZIP**:
```bash
# Windows PowerShell
Compress-Archive -Path "covid_app", "models", "application.py", ".ebextensions", "requirements.txt" -DestinationPath "covid-app.zip" -Force

# Linux/Mac
zip -r covid-app.zip covid_app/ models/ application.py .ebextensions/ requirements.txt
```

2. **Subir a AWS Elastic Beanstalk**:
   - Ve a la consola de AWS Elastic Beanstalk
   - Crea una nueva aplicación
   - Selecciona "Python" como plataforma
   - Sube el archivo `covid-app.zip`
   - Configura el entorno

### Opción 2: AWS App Runner

#### Requisitos:
- Docker instalado
- Dockerfile (ya incluido)

#### Pasos:
1. **Construir imagen Docker**:
```bash
docker build -t covid-app .
```

2. **Subir a ECR**:
```bash
# Crear repositorio ECR
aws ecr create-repository --repository-name covid-app

# Etiquetar imagen
docker tag covid-app:latest <account-id>.dkr.ecr.<region>.amazonaws.com/covid-app:latest

# Subir imagen
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/covid-app:latest
```

3. **Configurar App Runner**:
   - Ve a AWS App Runner
   - Crea un nuevo servicio
   - Selecciona "Container registry"
   - Configura la imagen de ECR

### Opción 3: Heroku

#### Preparación:
1. **Crear Procfile**:
```
web: uvicorn covid_app.app.main:app --host 0.0.0.0 --port $PORT
```

2. **Crear runtime.txt**:
```
python-3.10.12
```

#### Despliegue:
```bash
# Instalar Heroku CLI
# Crear aplicación
heroku create tu-app-covid

# Configurar variables de entorno
heroku config:set PYTHONPATH=/app

# Desplegar
git push heroku main
```

### Opción 4: Google Cloud Run

#### Preparación:
1. **Crear Dockerfile** (ya incluido)
2. **Configurar gcloud**:
```bash
gcloud auth configure-docker
```

#### Despliegue:
```bash
# Construir y subir imagen
gcloud builds submit --tag gcr.io/PROJECT-ID/covid-app

# Desplegar
gcloud run deploy --image gcr.io/PROJECT-ID/covid-app --platform managed --region us-central1 --allow-unauthenticated
```

### Opción 5: Azure Container Instances

#### Despliegue:
```bash
# Construir imagen
docker build -t covid-app .

# Subir a Azure Container Registry
az acr build --registry <registry-name> --image covid-app .

# Desplegar
az container create --resource-group <resource-group> --name covid-app --image <registry-name>.azurecr.io/covid-app --ports 8001 --dns-name-label covid-app
```

## 🔧 Configuración

### Variables de Entorno
- `PORT`: Puerto de la aplicación (default: 8001)
- `PYTHONPATH`: Ruta de Python para imports
- `LOG_LEVEL`: Nivel de logging (default: INFO)

### Archivos de Configuración
- `covid_app/app/config.py`: Configuración principal
- `covid_app/app/model/`: Modelos de machine learning
- `covid_app/app/static/`: Archivos estáticos
- `covid_app/app/templates/`: Templates HTML

## 📊 Uso de la API

### Endpoints Disponibles

#### 1. Página Principal
```
GET /
```
Interfaz web para subir imágenes.

#### 2. Health Check
```
GET /api/v1/health
```
Verificar estado de la aplicación.

#### 3. Predicción (JSON)
```
POST /api/v1/predict
Content-Type: multipart/form-data
Body: file (imagen)
```

#### 4. Predicción (HTML)
```
POST /api/v1/predict_html
Content-Type: multipart/form-data
Body: file (imagen)
```

#### 5. Documentación
```
GET /docs
```
Documentación interactiva de la API.

### Ejemplo de Uso con cURL

```bash
# Health check
curl -X GET "http://localhost:8001/api/v1/health"

# Predicción
curl -X POST "http://localhost:8001/api/v1/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@imagen.png"
```

## 🧪 Testing

### Ejecutar Tests
```bash
cd covid_app
pytest app/tests/
```

### Test de la API
```bash
# Test básico
curl -X GET "http://localhost:8001/api/v1/health"

# Test con imagen
curl -X POST "http://localhost:8001/api/v1/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data/raw/COVID/images/COVID-1.png"
```

## 📁 Estructura del Proyecto

```
COVID-19-Patient-Classification-from-Chest-X-rays-Using-Public-Data/
├── covid_app/
│   ├── app/
│   │   ├── api.py              # Endpoints de la API
│   │   ├── config.py           # Configuración
│   │   ├── main.py             # Aplicación principal
│   │   ├── model/              # Modelos ML
│   │   ├── schemas/            # Esquemas Pydantic
│   │   ├── static/             # Archivos estáticos
│   │   ├── templates/          # Templates HTML
│   │   └── tests/              # Tests
│   ├── requirements.txt        # Dependencias
│   └── Procfile               # Configuración Heroku
├── data/                      # Datos de entrenamiento
├── models/                    # Modelos entrenados
├── notebooks/                 # Jupyter notebooks
├── scripts/                   # Scripts de utilidad
├── Dockerfile                 # Configuración Docker
├── amplify.yml               # Configuración AWS Amplify
└── README.md                 # Este archivo
```

## 🐳 Docker

### Construir imagen
```bash
docker build -t covid-app .
```

### Ejecutar contenedor
```bash
docker run -p 8001:8001 covid-app
```

### Ejecutar con volúmenes
```bash
docker run -p 8001:8001 -v $(pwd)/data:/app/data covid-app
```

## 🔍 Troubleshooting

### Problemas Comunes

#### 1. Error de importación
```
ModuleNotFoundError: No module named 'covid_app'
```
**Solución**: Verificar que `PYTHONPATH` esté configurado correctamente.

#### 2. Error de modelo
```
FileNotFoundError: model_V02.pt
```
**Solución**: Verificar que el archivo del modelo esté en `covid_app/app/model/`.

#### 3. Error de puerto
```
Address already in use
```
**Solución**: Cambiar el puerto o matar el proceso que lo está usando.

#### 4. Error de dependencias
```
ImportError: No module named 'torch'
```
**Solución**: Instalar todas las dependencias con `pip install -r requirements.txt`.

### Logs y Debugging

#### Ver logs de la aplicación
```bash
# Local
uvicorn app.main:app --log-level debug

# Docker
docker logs <container-id>

# AWS Elastic Beanstalk
eb logs
```

#### Verificar estado de la aplicación
```bash
curl -X GET "http://localhost:8001/api/v1/health"
```

## 📈 Monitoreo

### Métricas Recomendadas
- Tiempo de respuesta de la API
- Uso de CPU y memoria
- Número de predicciones por minuto
- Tasa de error

### Herramientas de Monitoreo
- AWS CloudWatch (para AWS)
- Google Cloud Monitoring (para GCP)
- Azure Monitor (para Azure)
- Prometheus + Grafana (para cualquier plataforma)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Si tienes problemas o preguntas:
1. Revisa la sección de Troubleshooting
2. Busca en los Issues del repositorio
3. Crea un nuevo Issue con detalles del problema

## 🙏 Agradecimientos

- Dataset de rayos X de COVID-19
- PyTorch y FastAPI por las excelentes librerías
- Comunidad de desarrolladores de ML

---

**Nota**: Esta aplicación es para fines educativos y de investigación. No debe usarse como único método de diagnóstico médico.