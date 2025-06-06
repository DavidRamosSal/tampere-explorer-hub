import json
import os
from calculate_score import calculate_score

# Load your saved event list
with open('./mock_data/mvp_data/events_full_list.json', 'r', encoding='utf-8') as f:
    events_data = json.load(f)

# Access the list of events
events = events_data['pages']


# Sample Mock Resource (optional for now)
sample_resource = {
    'location': {
        'lat': 61.498150,
        'lng': 23.760953
    }
}

# Optional data (set to None for now)
weather_data = None
traffic_data = None
demographics_data = None
transport_data = None

# Prepare a list to store results
scored_events = []

# Test scoring
for event in events:
    try:
        # Extract first date from event.event.dates
        if event.get('event') and event['event'].get('dates'):
            start_date = event['event']['dates'][0]['start']
        else:
            start_date = event['event']['start']  # fallback if no dates list

        # Extract event location
        event_location = {
            'lat': event['locations'][0]['lat'],
            'lng': event['locations'][0]['lng']
        }

        # Prepare event_data for scoring
        event_data = {
            'name': event.get('name', 'No Name'),
            'startDate': start_date,
            'location': event_location,
            'categories': event.get('categories', []),
            'globalContentCategories': event.get('globalContentCategories', []),
            'ages': event.get('ages', [])
        }

        score = calculate_score(
            event_data=event_data,
            resource_data=sample_resource,
            weather_data=weather_data,
            traffic_data=traffic_data,
            demographics_data=demographics_data,
            transport_data=transport_data
        )

        scored_events.append({
            'name': event_data['name'],
            'startDate': start_date,
            'location': event_location,
            'globalContentCategories': event_data['globalContentCategories'],
            'ages': event_data['ages'],
            'score': score
        })

    except (IndexError, KeyError, TypeError) as e:
        print(f"Skipping event due to missing data: {e}")

# Sort events by score descending
scored_events = sorted(scored_events, key=lambda x: x['score'], reverse=True)

# Save the scored events to a temp folder
output_path = './temp/scored_events.json'

# Make sure temp directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(scored_events, f, indent=4, ensure_ascii=False)

print(f"\n✅ Scored events saved successfully to {output_path}")