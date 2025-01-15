Weather Predictor App

Instalación
1. Clonar el repositorio

2. Instalar las dependencias:
pip install -r requirements.txt

3. Configurar la base de datos
Iniciar PostgreSQL y crear la base de datos:
CREATE DATABASE weather_db;
Asegúrarse que las credenciales de la base de datos sean correctas en app/__init__.py.

4. Simular y almacenar datos meteorológicos
Ejecuta el script para generar datos meteorológicos de 10 años:
python populate_db.py

5. Iniciar la aplicación
Ejecuta el servidor Flask:
python app.py

6. Endpoints principales

GET /api/weather/<day>: Condición meteorológica para un día específico.

GET /api/weather/stats: Estadísticas generales.

GET /api/weather/analysis: Análisis de períodos de sequía, lluvia y condiciones óptimas.
