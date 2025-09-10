# app.py - FINAL "FUTURE PLANNER" VERSION

from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import googlemaps
from datetime import datetime
import requests
import config

app = Flask(__name__)

# --- Initialization ---
print("Loading the final trained AI model v3...")
model = joblib.load('traffic_model_v3.joblib')
print("Model v3 loaded successfully.")

gmaps = googlemaps.Client(key=config.GOOGLE_MAPS_API_KEY_SERVER)
print("Google Maps client initialized.")


# --- Helper Functions (remain the same) ---

def get_live_weather(is_future):
    """ Fetches live weather. If the trip is in the future, it assumes 'Clear'. """
    if is_future:
        print("Future trip, assuming 'Clear' weather.")
        return 'Clear'

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'q': 'Ghaziabad,IN', 'appid': config.OPENWEATHER_API_KEY, 'units': 'metric'}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        main_weather = weather_data['weather'][0]['main']
        print(f"Live weather fetched: {main_weather}")
        if main_weather in ['Rain', 'Drizzle', 'Thunderstorm']:
            return 'Rain'
        elif main_weather in ['Mist', 'Haze', 'Smoke']:
            return 'Haze'
        elif main_weather == 'Fog':
            return 'Fog'
        elif main_weather == 'Clouds':
            return 'Clouds'
        else:
            return 'Clear'
    except requests.exceptions.RequestException:
        return 'Clear'


def classify_route(route_leg):
    try:
        steps = route_leg['steps']
        all_instructions = " ".join([step['html_instructions'] for step in steps])
        if "NH" in all_instructions or "Expressway" in all_instructions:
            return "segment_nh9"
        elif "GT Rd" in all_instructions or "Grand Trunk" in all_instructions:
            return "segment_gt_road"
        else:
            return "segment_indirapuram"
    except (IndexError, KeyError):
        return "segment_indirapuram"


# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html', api_key=config.GOOGLE_MAPS_API_KEY_CLIENT)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        start_point = data['start']
        destination = data['destination']

        # --- KEY CHANGE: Get the departure time from the user ---
        departure_time_str = data.get('departure_time')  # e.g., '2025-09-09T08:00'

        if departure_time_str:
            departure_time = datetime.fromisoformat(departure_time_str)
            is_future_trip = True
        else:
            departure_time = datetime.now()
            is_future_trip = False

        # --- Get multiple routes from Google, now with the correct departure time ---
        directions_result = gmaps.directions(start_point, destination, mode="driving", departure_time=departure_time,
                                             alternatives=True)
        if not directions_result: return jsonify({'error': 'Could not find any routes.'}), 400

        # --- Get weather (live or assumed) ---
        weather_condition = get_live_weather(is_future_trip)

        routes_analysis = []
        for i, route in enumerate(directions_result):
            route_leg = route['legs'][0]
            road_segment_id = classify_route(route_leg)

            # --- Use the selected departure time for the AI prediction ---
            prediction_day = departure_time.weekday()
            prediction_hour = departure_time.hour

            model_features = [prediction_day, prediction_hour, 1 if road_segment_id == 'segment_gt_road' else 0,
                              1 if road_segment_id == 'segment_indirapuram' else 0,
                              1 if road_segment_id == 'segment_nh9' else 0, 1 if weather_condition == 'Clear' else 0,
                              1 if weather_condition == 'Clouds' else 0, 1 if weather_condition == 'Fog' else 0,
                              1 if weather_condition == 'Haze' else 0, 1 if weather_condition == 'Rain' else 0]
            predicted_speed_kph = model.predict(np.array([model_features]))[0]

            distance_km = route_leg['distance']['value'] / 1000
            if predicted_speed_kph < 1: predicted_speed_kph = 1
            custom_duration_hours = distance_km / predicted_speed_kph
            custom_duration_sec = custom_duration_hours * 3600

            # Get Google's prediction (it's called 'duration' for future trips)
            google_duration_text = route_leg.get('duration_in_traffic', route_leg.get('duration', {})).get('text',
                                                                                                           'N/A')

            routes_analysis.append({
                'summary': route.get('summary', f'Route {i + 1}'),
                'google_duration_text': google_duration_text,
                'custom_duration_sec': custom_duration_sec,
                'predicted_speed': round(predicted_speed_kph, 2),
                'polyline': route['overview_polyline']['points']
            })

        best_route_index = min(range(len(routes_analysis)), key=lambda i: routes_analysis[i]['custom_duration_sec'])
        routes_analysis[best_route_index]['recommended'] = True

        start_location = directions_result[0]['legs'][0]['start_location']
        end_location = directions_result[0]['legs'][0]['end_location']

        return jsonify({
            'routes': routes_analysis,
            'live_weather': weather_condition,
            'start_location': start_location,
            'end_location': end_location
        })

    except Exception as e:
        print(f"An error occurred in /predict: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

