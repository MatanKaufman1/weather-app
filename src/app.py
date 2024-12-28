from flask import Flask, render_template, request, Response, jsonify
from weather_utility import WeatherUtility


app = Flask(__name__)

def get_client():
    return boto3.client(
        's3',
        region_name='us-east-1'
    )

@app.route('/', methods=['GET'])
def weather():
    weather_utility = WeatherUtility()
    city = request.args.get('city', 'Haifa')

    if not city.strip() or len(city) <= 0:
        return render_template("weather.html", error="Please enter city name")

    location = weather_utility.get_location(city)
    if location is None:
        return render_template('weather.html', error="Location not found", data=None, location=None)

    api_response = weather_utility.get_weather_data(location)
    processed_weather_data = weather_utility.process_weather_data(api_response)
    weather_days = weather_utility.calculate_weather(processed_weather_data)

    data = {
        "city_name": city,
        "weather_days": weather_days
    }

    return render_template('weather.html', data=data, location=location)


if __name__ == '__main__':
    app.run(debug=True)
