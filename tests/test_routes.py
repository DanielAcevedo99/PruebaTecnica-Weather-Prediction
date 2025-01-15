def test_get_weather_by_day(client):
    with client.application.app_context():
        from app import db
        from sqlalchemy import text

        with db.engine.connect() as connection:
            connection.execute(text("TRUNCATE TABLE weather_conditions RESTART IDENTITY CASCADE"))
            connection.execute(
                text("INSERT INTO weather_conditions (day, condition) VALUES (1, 'normal')")
            )

    response = client.get("/api/weather/1")
    assert response.status_code == 200
    assert response.json == {"day": 1, "condition": "normal"}

    response = client.get("/api/weather/999")
    print("Response JSON:", response.json)  
    assert response.status_code == 404
    assert response.json == {"error": "Day not found"}


def test_get_weather_stats(client):
    with client.application.app_context():
        from app import db
        from sqlalchemy import text

        with db.engine.connect() as connection:
            connection.execute(text("TRUNCATE TABLE weather_conditions RESTART IDENTITY CASCADE"))
            connection.execute(
                text("INSERT INTO weather_conditions (day, condition) VALUES (2, 'rain')")
            )
        connection.execute(
            text("INSERT INTO weather_conditions (day, condition) VALUES (3, 'normal')")
            )


    response = client.get("/api/weather/stats")
    assert response.status_code == 200

    data = response.json
    assert "stats" in data
    assert "max_rain_day" in data
    assert data["max_rain_day"] == 2  
