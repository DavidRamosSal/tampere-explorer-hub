from geopy.distance import geodesic

def is_weekend_or_evening(date_str):
    from datetime import datetime
    dt = datetime.fromisoformat(date_str.replace('Z', ''))
    # Check if Saturday or Sunday
    if dt.weekday() in (5, 6):
        return True
    # Check if after 5 PM
    if dt.hour >= 17:
        return True
    return False

def calculate_distance(loc1, loc2):
    """
    Calculate distance between two lat/lon points.
    loc1, loc2: {'lat': float, 'lng': float}
    Returns distance in km.
    """
    point1 = (loc1['lat'], loc1['lng'])
    point2 = (loc2['lat'], loc2['lng'])
    return geodesic(point1, point2).kilometers

# Define keywords that suggest festival or market events
festival_market_keywords = {
    "festival",
    "market",
    "fair",
    "food and beverage",
    "seasonal events"
}

def is_festival_or_market(event):
    categories = event.get("globalContentCategories", [])
    # Lowercase and match
    return any(cat.lower() in festival_market_keywords for cat in categories)

def calculate_score(
    event_data,
    resource_data=None,
    weather_data=None,
    traffic_data=None,
    demographics_data=None,
    transport_data=None
):
    """
    Calculate score for an event-location combination based on provided data.

    Mandatory:
      - event_data
      - resource_data (booking spot info)

    Optional:
      - weather_data
      - traffic_data
      - demographics_data
      - transport_data

    Returns:
      Score (int)
    """
    score = 0

    # Event Type - Mandatory
    if is_festival_or_market(event_data):
        score += 40

    # Event Date/Time - Mandatory
    if is_weekend_or_evening(event_data['startDate']):
        score += 20

    # Distance to Booking Spot - Mandatory
    distance = calculate_distance(event_data['location'], resource_data['location'])
    if distance < 1.5:
        score += 40

    # Weather Condition - Optional
    if weather_data:
        if weather_data.get('rain', 0) == 0 and 15 <= weather_data.get('temperature', 0) <= 22:
            score += 30

    # Historic Foot Traffic - Optional
    if traffic_data:
        if traffic_data.get('daily_average', 0) > 10000:
            score += 30

    # Demographics Fit - Optional
    if demographics_data:
        if demographics_data.get('age_group') in ['Families', 'Students']:
            score += 10

    # Public Transport Access - Optional
    if transport_data:
        if transport_data.get('nearest_stop_distance', 10000) < 500:
            score += 20

    return score
