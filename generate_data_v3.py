import csv
import random
from datetime import datetime, timedelta

# --- 1. DEFINE ROAD SEGMENTS (from v2) ---
ROAD_SEGMENTS = {
    "NH-9": {
        "id": "segment_nh9",
        "base_speeds": {"rush": 25, "day": 60, "night": 80},
        "weekend_modifier": 1.1
    },
    "GT-Road": {
        "id": "segment_gt_road",
        "base_speeds": {"rush": 15, "day": 35, "night": 50},
        "weekend_modifier": 1.0
    },
    "Indirapuram-Road": {
        "id": "segment_indirapuram",
        "base_speeds": {"rush": 10, "day": 25, "night": 40},
        "weekend_modifier": 1.2
    }
}

# --- 2. NEW: DEFINE WEATHER CONDITIONS & THEIR IMPACT ---
# We define weather types, their probability (weights), and their impact on speed (modifier).
# For Ghaziabad, 'Clear' and 'Haze' are most common. 'Rain' is less common. 'Fog' is rare.
WEATHER_CONDITIONS = {
    'Clear': {'weight': 50, 'modifier': 1.0},  # No impact
    'Clouds': {'weight': 20, 'modifier': 0.95},  # Slight slowdown
    'Haze': {'weight': 15, 'modifier': 0.9},  # Noticeable slowdown
    'Rain': {'weight': 10, 'modifier': 0.7},  # Significant slowdown
    'Fog': {'weight': 5, 'modifier': 0.5}  # Major slowdown
}

# --- 3. CONFIGURE SCRIPT ---
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime.now()
OUTPUT_FILE = 'historical_traffic_data_v3.csv'  # New filename for our v3 data


# --- 4. HELPER FUNCTIONS ---

def get_base_speed(hour, road_profile):
    """ Determines base speed based on time and road profile. """
    rush_hour_speed = random.uniform(road_profile["base_speeds"]["rush"] * 0.8,
                                     road_profile["base_speeds"]["rush"] * 1.2)
    day_speed = random.uniform(road_profile["base_speeds"]["day"] * 0.9, road_profile["base_speeds"]["day"] * 1.1)
    night_speed = random.uniform(road_profile["base_speeds"]["night"] * 0.9, road_profile["base_speeds"]["night"] * 1.1)

    if 7 <= hour < 10 or 17 <= hour < 20:
        return rush_hour_speed
    elif 10 <= hour < 17:
        return day_speed
    else:
        return night_speed


def get_random_weather():
    """ Selects a random weather condition based on the defined weights. """
    conditions = list(WEATHER_CONDITIONS.keys())
    weights = [WEATHER_CONDITIONS[c]['weight'] for c in conditions]
    return random.choices(conditions, weights=weights, k=1)[0]


# --- 5. MAIN DATA GENERATION LOGIC ---

def generate_data():
    """ Generates new, weather-aware simulated traffic data. """
    print(f"Generating new weather-aware data and saving to '{OUTPUT_FILE}'...")

    # Add the new 'weather' column to our header
    header = ['timestamp', 'road_segment_id', 'weather', 'average_speed_kph', 'day_of_week', 'hour_of_day']

    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        current_date = START_DATE
        while current_date <= END_DATE:
            for hour in range(24):
                # For each hour, we'll have one weather condition for the whole area
                current_weather = get_random_weather()
                weather_modifier = WEATHER_CONDITIONS[current_weather]['modifier']

                for road_name, road_profile in ROAD_SEGMENTS.items():
                    timestamp = current_date.replace(hour=hour)
                    day_of_week = timestamp.weekday()

                    base_speed = get_base_speed(hour, road_profile)
                    weekday_modifier = road_profile["weekend_modifier"] if day_of_week >= 5 else 1.0
                    random_noise = random.uniform(0.9, 1.1)

                    # Apply the new weather modifier to our speed calculation
                    final_speed = base_speed * weekday_modifier * weather_modifier * random_noise
                    final_speed = max(5, min(120, final_speed))

                    writer.writerow([
                        timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        road_profile['id'],
                        current_weather,  # Add the weather condition to the row
                        round(final_speed, 2),
                        day_of_week,
                        hour
                    ])

            current_date += timedelta(days=1)

    print(f"Successfully generated new weather-aware data!")


if __name__ == '__main__':
    generate_data()
