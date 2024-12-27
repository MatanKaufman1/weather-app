import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, Response, jsonify
from weather_utility import WeatherUtility
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

def get_client():
    return boto3.client(
        's3',
        region_name='us-east-1'
    )

@app.route('/sky', methods=['GET'])
def download_file():
    s3 = get_client()
    try:
        file = s3.get_object(Bucket='matan-s3', Key='sky.jpeg')
        return Response(
            file['Body'].read(),
            headers={"Content-Disposition": "attachment;filename=sky.jpeg"}
        )
    except ClientError as e:
        return jsonify({"error": str(e)}), 500



dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('weather-db')

@app.route('/save-data', methods=['POST'])
def save_weather_data():
    city = request.form.get('city')
    date = request.form.get('date')
    forecast_data_str = request.form.get('forecast_data')

    # Check for missing city, date, or forecast data
    if not city or not date or not forecast_data_str:
        return jsonify({"error": "Missing city, date, or forecast data"}), 400

    # Check specifically for an empty city name
    if not city.strip():
        return jsonify({"error": "Please enter city name"}), 400

    try:
        # If forecast_data is JSON-like, parse it
        forecast_data = json.loads(forecast_data_str)

        if 'weather_days' not in forecast_data:
            return jsonify({"error": "Missing weather_days in forecast_data"}), 400

        # Prepare the data to be saved
        weather_data = {
            'city': city,              # Partition Key
            'date': date,              # Sort Key
            'forecast': forecast_data['weather_days']  # The data to save
        }

        # Save the data to DynamoDB
        table.put_item(Item=weather_data)

        return jsonify({"message": "Data saved successfully"}), 200

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in forecast_data"}), 400
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ClientError as e:
        return jsonify({"error": str(e)}), 500


@app.route('/tel-aviv', methods=['GET'])
def tel_aviv():
    weather_utility = WeatherUtility()
    city = request.args.get('city', 'tel aviv')
    location = weather_utility.get_location(city)

    api_response = weather_utility.get_weather_data(location)
    processed_weather_data = weather_utility.process_weather_data(api_response)
    weather_days = weather_utility.calculate_weather(processed_weather_data)


    weather_data = {
        'city': city,  # Partition Key
        'date': str(datetime.today().date()),  # Sort Key
        'forecast': weather_days  # The data to save
    }

    # Save the data to DynamoDB
    table.put_item(Item=weather_data)
    return jsonify({"message": "Data saved successfully"}), 200

"""
@app.errorhandler(404)
def not_found_error(_):
    return render_template('404.html'), 404
"""
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
