import folium
from folium.plugins import MarkerCluster
from math import radians, sin, cos, sqrt, atan2
import itertools

# Haversine formula to calculate the distance between two points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Data
data = [
    [1, 23.8728568, 90.3984184, "Uttara Branch"],
    [2, 23.8513998, 90.3944536, "City Bank Airport"],
    [3, 23.8330429, 90.4092871, "City Bank Nikunja"],
    [4, 23.8679743, 90.3840879, "City Bank Beside Uttara Diagnostic"],
    [5, 23.8248293, 90.3551134, "City Bank Mirpur 12"],
    [6, 23.827149, 90.4106238, "City Bank Le Meridien"],
    [7, 23.8629078, 90.3816318, "City Bank Shaheed Sarani"],
    [8, 23.8673789, 90.429412, "City Bank Narayanganj"],
    [9, 23.8248938, 90.3549467, "City Bank Pallabi"],
    [10, 23.813316, 90.4147498, "City Bank JFP"]
]

# Calculate distances and store in a multidimensional list
distances = []
for location1 in data:
    row = []
    for location2 in data:
        lat1, lon1 = location1[1], location1[2]
        lat2, lon2 = location2[1], location2[2]
        distance = haversine(lat1, lon1, lat2, lon2)
        row.append(distance)
    distances.append(row)

def tsp(distances):
    num_locations = len(distances)
    all_locations = set(range(num_locations))
    start_location = 0

    # Generate all possible permutations of locations to visit
    permutations = itertools.permutations(all_locations - {start_location})

    min_distance = float('inf')
    optimal_route = None

    for permutation in permutations:
        route = [start_location] + list(permutation) + [start_location]
        distance = sum(distances[route[i]][route[i+1]] for i in range(num_locations))

        if distance < min_distance:
            min_distance = distance
            optimal_route = route

    return optimal_route, min_distance

# Usage:
optimal_route, min_distance = tsp(distances)

# Create a base map
m = folium.Map(location=[23.8728568, 90.3984184], zoom_start=12)

# Add markers for each location
marker_cluster = MarkerCluster().add_to(m)
for location in data:
    folium.Marker(
        location=[location[1], location[2]],
        popup=location[3],
        icon=folium.Icon(icon="cloud"),
    ).add_to(marker_cluster)

# Draw lines for the optimal route
for i in range(len(optimal_route) - 1):
    folium.PolyLine(
        locations=[
            [data[optimal_route[i]][1], data[optimal_route[i]][2]],
            [data[optimal_route[i + 1]][1], data[optimal_route[i + 1]][2]]
        ],
        color="blue",
        weight=2.5,
        opacity=1
    ).add_to(m)

# Save the map to an HTML file
m.save("tsp_map.html")