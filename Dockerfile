FROM python:3.10-slim

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copiar requirements primero para mejor cacheo de capas
COPY covid_app/requirements.txt /app/requirements.txt

# Instalar dependencias del sistema y Python
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY covid_app/ /app/covid_app/
COPY models/ /app/models/

# Cambiar ownership de archivos al usuario appuser
RUN chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Exponer el puerto correcto
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/ || exit 1

# Comando para ejecutar la aplicación
CMD ["uvicorn", "covid_app.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
