import csv
import random
from datetime import datetime, timedelta

# --- 1. DEFINE OUR ROAD SEGMENTS ---
# This is our new "database" of roads. Each road has a unique profile.
ROAD_SEGMENTS = {
    "NH-9": {  # Delhi-Meerut Expressway - A fast highway
        "id": "segment_nh9",
        "base_speeds": {"rush": 25, "day": 60, "night": 80},  # Higher base speed
        "weekend_modifier": 1.1  # Gets slightly faster on weekends
    },
    "GT-Road": {  # Grand Trunk Road - A busy, mixed-use road
        "id": "segment_gt_road",
        "base_speeds": {"rush": 15, "day": 35, "night": 50},  # Slower base speed
        "weekend_modifier": 1.0  # Consistent traffic on weekends
    },
    "Indirapuram-Road": {  # A major internal road in Indirapuram
        "id": "segment_indirapuram",
        "base_speeds": {"rush": 10, "day": 25, "night": 40},  # Lowest base speed
        "weekend_modifier": 1.2  # Gets much faster on weekends as local traffic drops
    }
}

# --- 2. CONFIGURE SCRIPT ---
START_DATE = datetime(2025, 1, 1)  # Let's generate more data for a better model
END_DATE = datetime.now()
OUTPUT_FILE = 'historical_traffic_data_v2.csv'  # New filename to avoid confusion


# --- 3. UPDATED HELPER FUNCTIONS ---

def get_base_speed(hour, road_profile):
    """
    Determines the base speed based on the time AND the specific road's profile.
    """
    rush_hour_speed = random.uniform(road_profile["base_speeds"]["rush"] * 0.8,
                                     road_profile["base_speeds"]["rush"] * 1.2)
    day_speed = random.uniform(road_profile["base_speeds"]["day"] * 0.9, road_profile["base_speeds"]["day"] * 1.1)
    night_speed = random.uniform(road_profile["base_speeds"]["night"] * 0.9, road_profile["base_speeds"]["night"] * 1.1)

    if 7 <= hour < 10 or 17 <= hour < 20:  # Morning and Evening Rush Hour
        return rush_hour_speed
    elif 10 <= hour < 17:  # Daytime
        return day_speed
    else:  # Night time
        return night_speed


# --- 4. MAIN DATA GENERATION LOGIC ---

def generate_data():
    """
    Generates new, location-aware simulated traffic data.
    """
    print(f"Generating new location-aware data and saving to '{OUTPUT_FILE}'...")

    header = ['timestamp', 'road_segment_id', 'average_speed_kph', 'day_of_week', 'hour_of_day']

    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        current_date = START_DATE
        while current_date <= END_DATE:
            for hour in range(24):
                # Iterate through our new road segments dictionary
                for road_name, road_profile in ROAD_SEGMENTS.items():
                    timestamp = current_date.replace(hour=hour)
                    day_of_week = timestamp.weekday()

                    base_speed = get_base_speed(hour, road_profile)

                    # Apply weekend modifier if it's a weekend (5=Sat, 6=Sun)
                    weekday_modifier = road_profile["weekend_modifier"] if day_of_week >= 5 else 1.0

                    random_noise = random.uniform(0.9, 1.1)  # Add some final noise
                    final_speed = base_speed * weekday_modifier * random_noise
                    final_speed = max(5, min(120, final_speed))

                    writer.writerow([
                        timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        road_profile['id'],  # Use the specific road ID
                        round(final_speed, 2),
                        day_of_week,
                        hour
                    ])

            current_date += timedelta(days=1)

    print(f"Successfully generated new data!")


if __name__ == '__main__':
    generate_data()