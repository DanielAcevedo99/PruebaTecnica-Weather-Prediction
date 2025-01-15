from flask import Blueprint, jsonify
from sqlalchemy import text
from app import db

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather/<int:day>', methods=['GET'])
def get_weather_by_day(day):
    """
    Devuelve la condición meteorológica de un día específico.
    Endpoint: /weather/<day>
    - Si el día existe en la base de datos, devuelve un JSON con la condición meteorológica.
    - Si no, devuelve un mensaje de error.
    """
    query = text("SELECT * FROM weather_conditions WHERE day = :day")
    
    with db.engine.connect() as connection:
        result = connection.execute(query, {"day": day}).mappings().fetchone()  

    if result:
        return jsonify({"day": result['day'], "condition": result['condition']})
    else:
        return jsonify({"error": "Day not found"}), 404


@weather_bp.route('/weather/stats', methods=['GET'])
def get_weather_stats():
    """
    Devuelve estadísticas generales de las condiciones meteorológicas.
    Endpoint: /weather/stats
    - Muestra el conteo de cada tipo de condición meteorológica.
    - Devuelve el último día en el que ocurrió lluvia.
    """
    stats_query = text("""
        SELECT condition, COUNT(*) AS count
        FROM weather_conditions
        GROUP BY condition
    """)

    max_rain_query = text("""
        SELECT day
        FROM weather_conditions
        WHERE condition = 'rain'
        ORDER BY day DESC
        LIMIT 1
    """)

    with db.engine.connect() as connection:
        stats = connection.execute(stats_query).mappings().fetchall()
        max_rain = connection.execute(max_rain_query).mappings().fetchone()

    stats_result = [{"condition": row['condition'], "count": row['count']} for row in stats]

    return jsonify({
        "stats": stats_result,  
        "max_rain_day": max_rain['day'] if max_rain else None  
    })


@weather_bp.route('/weather/analysis', methods=['GET'])
def get_weather_analysis():
    """
    Devuelve un análisis sobre sequías, lluvias y condiciones óptimas.
    Endpoint: /weather/analysis
    - Cuenta los períodos de sequías, lluvias y condiciones óptimas.
    - Devuelve el último día de lluvia.
    """
    drought_query = text("""
        WITH drought_periods AS (
            SELECT day, condition, day - ROW_NUMBER() OVER (ORDER BY day) AS period_group
            FROM weather_conditions
            WHERE condition = 'drought'
        )
        SELECT COUNT(DISTINCT period_group) AS drought_periods
        FROM drought_periods;
    """)

    rain_query = text("""
        WITH rain_periods AS (
            SELECT day, condition, day - ROW_NUMBER() OVER (ORDER BY day) AS period_group
            FROM weather_conditions
            WHERE condition = 'rain'
        )
        SELECT COUNT(DISTINCT period_group) AS rain_periods
        FROM rain_periods;
    """)

    max_rain_query = text("""
        SELECT MAX(day) AS max_rain_day
        FROM weather_conditions
        WHERE condition = 'rain';
    """)

    optimal_query = text("""
        WITH optimal_periods AS (
            SELECT day, condition, day - ROW_NUMBER() OVER (ORDER BY day) AS period_group
            FROM weather_conditions
            WHERE condition = 'optimal'
        )
        SELECT COUNT(DISTINCT period_group) AS optimal_periods
        FROM optimal_periods;
    """)

    with db.engine.connect() as connection:
        drought_result = connection.execute(drought_query).fetchone()
        rain_result = connection.execute(rain_query).fetchone()
        max_rain_result = connection.execute(max_rain_query).fetchone()
        optimal_result = connection.execute(optimal_query).fetchone()

    return jsonify({
        "drought_periods": drought_result[0] if drought_result else 0,  
        "rain_periods": rain_result[0] if rain_result else 0,  
        "max_rain_day": max_rain_result[0] if max_rain_result else None,  
        "optimal_periods": optimal_result[0] if optimal_result else 0  
    })
