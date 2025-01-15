import sys
import os
from sqlalchemy import text
from app import db, create_app
from app.services import predict_weather

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = create_app()
app.app_context().push()
def populate_weather_conditions():
    data = []  
    for day in range(1, 3651):  
        condition = predict_weather(day)
        data.append({"day": day, "condition": condition})
        print(f"Day {day}: {condition}")  
    
    save_to_database(data)

def save_to_database(data):
    with db.engine.begin() as connection:  
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS weather_conditions (
                day INT PRIMARY KEY,
                condition VARCHAR(20) NOT NULL
            );
        """))

        for record in data:
            connection.execute(text("""
                INSERT INTO weather_conditions (day, condition)
                VALUES (:day, :condition)
                ON CONFLICT (day) DO NOTHING;
            """), {"day": record["day"], "condition": record["condition"]})

if __name__ == "__main__":
    populate_weather_conditions()
