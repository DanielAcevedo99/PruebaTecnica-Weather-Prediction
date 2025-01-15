import math

# Constantes de los planetas, incluyen distancia al sol, velocidad angular y dirección (1 para horario, -1 para antihorario)
PLANETS = {
    "Ferengi": {"distance": 500, "velocity": 1, "direction": 1},  
    "Vulcano": {"distance": 1000, "velocity": 5, "direction": -1},  
    "Betazoide": {"distance": 2000, "velocity": 3, "direction": 1}, 
}

# Convierte grados a radianes (necesario para cálculos trigonométricos)
def degrees_to_radians(degrees):
    return degrees * math.pi / 180

# Calcula la posición de un planeta en coordenadas cartesianas (x, y) para un día específico
def get_planet_position(planet, day):
    distance = PLANETS[planet]["distance"]
    velocity = PLANETS[planet]["velocity"]
    direction = PLANETS[planet]["direction"]

    # Calcula el ángulo actual del planeta respecto al eje x
    angle = (velocity * day * direction) % 360  
    radians = degrees_to_radians(angle)
    # Convierte el ángulo y la distancia en coordenadas cartesianas
    x = distance * math.cos(radians)
    y = distance * math.sin(radians)
    return x, y

# Verifica si tres puntos (planetas) son colineales
def are_collinear(p1, p2, p3, tol=1e-9):
    det = p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])
    return math.isclose(det, 0, abs_tol=tol)

# Calcula el área del triángulo formado por tres puntos
def calculate_triangle_area(p1, p2, p3):
    return abs(p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) / 2

# Determina si el sol (0, 0) está dentro del triángulo formado por tres planetas
def is_sun_inside(p1, p2, p3):
    sun = (0, 0)  
    area_total = calculate_triangle_area(p1, p2, p3)
    area1 = calculate_triangle_area(sun, p2, p3)
    area2 = calculate_triangle_area(p1, sun, p3)
    area3 = calculate_triangle_area(p1, p2, sun)
    return math.isclose(area_total, area1 + area2 + area3, abs_tol=1e-9)

# Predice las condiciones meteorológicas para un día específico
def predict_weather(day):
    p1 = get_planet_position("Ferengi", day)
    p2 = get_planet_position("Vulcano", day)
    p3 = get_planet_position("Betazoide", day)

    print(f"Day {day}: Ferengi={p1}, Vulcano={p2}, Betazoide={p3}")

    if are_collinear(p1, p2, p3):  
        if are_collinear(p1, p2, (0, 0)): 
            print(f"Day {day}: Drought conditions detected")
            return "drought"  
        else: 
            print(f"Day {day}: Optimal conditions detected")
            return "optimal"  
    elif is_sun_inside(p1, p2, p3): 
        print(f"Day {day}: Rain conditions detected")
        return "rain"  
    else:  
        print(f"Day {day}: Normal conditions detected")
        return "normal"  

# Simula el clima para un rango de días y devuelve los resultados
def simulate_weather(days=3650):
    weather_data = []
    for day in range(1, days + 1):
        condition = predict_weather(day)
        weather_data.append({"day": day, "condition": condition})
    return weather_data

# Guarda los datos simulados en la base de datos
def save_to_database(data, db):
    with db.engine.connect() as connection:
        connection.execute("DELETE FROM weather_conditions") 
        for record in data:
            connection.execute(
                "INSERT INTO weather_conditions (day, condition) VALUES (:day, :condition)",
                {"day": record["day"], "condition": record["condition"]},
            )
    print("Weather data saved to database successfully.")
