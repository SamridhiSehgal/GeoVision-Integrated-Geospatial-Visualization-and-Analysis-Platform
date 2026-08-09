import math
def destination_point(lat, lon, distance, bearing):
    """
    Calculate new coordinate from a start point.

    distance: meters
    bearing: degrees
    """

    earth_radius = 6371000

    lat1 = math.radians(lat)
    lon1 = math.radians(lon)

    brng = math.radians(bearing)

    lat2 = math.asin(
        math.sin(lat1) * math.cos(distance / earth_radius)
        + math.cos(lat1) * math.sin(distance / earth_radius) * math.cos(brng)
    )

    lon2 = lon1 + math.atan2(
        math.sin(brng) * math.sin(distance / earth_radius) * math.cos(lat1),
        math.cos(distance / earth_radius) - math.sin(lat1) * math.sin(lat2),
    )

    return (math.degrees(lat2), math.degrees(lon2))


def create_fov_sector(lat, lon, heading, fov, distance, steps=30):

    points = []

    start_angle = heading - fov / 2

    end_angle = heading + fov / 2

    points.append([lat, lon])

    for i in range(steps + 1):

        angle = start_angle + (end_angle - start_angle) * i / steps

        p = destination_point(lat, lon, distance, angle)

        points.append([p[0], p[1]])

    points.append([lat, lon])

    return points
