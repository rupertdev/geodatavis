import json
from psycopg2 import connect
from shapely.geometry import box
def get_ipv4_networks_for_bbox(bbox):
    try:
        return_points = []
        connection = connect(
            host="ec2-54-225-106-93.compute-1.amazonaws.com",
            database='d4f34fpjsa5fdb',
            user='pebvxguuqlfpsj',
            password='a74ec8102f182e03a6eea9ff9ece26bab6a9c1a227f909287a3997e04694065e',
            port='5432')

        cursor = connection.cursor()

        bounding_box = box(
            bbox['_southWest']['lng'],
            bbox['_southWest']['lat'],
            bbox['_northEast']['lng'],
            bbox['_northEast']['lat'])

        cursor.execute(
            f"""
            SELECT st_astext(st_centroid(st_collect(geometry))), count(network)
            FROM ipv4geo
            WHERE st_within(
                geometry,
                ST_MakeEnvelope(
                    {bbox['_southWest']['lng']},
                    {bbox['_southWest']['lat']},
                    {bbox['_northEast']['lng']},
                    {bbox['_northEast']['lat']}, 4326))
                AND accuracy_radius > {get_accuracy_radius(bounding_box.area)}
            GROUP BY ST_SnapToGrid(geometry, {get_grid_size(bounding_box.area)});""")

        items = cursor.fetchall()

        for item in items:
            latlng = item[0].replace('POINT(', '').replace(')', '').split(' ')
            return_points.append({
                'lat': latlng[1],
                'lng': latlng[0],
                'count': item[1]
            })

        return json.dumps(return_points)
    except Exception as e:
        print("EXCEPTION", e)
    finally:
        if connection:
            cursor.close()
            connection.close()
    return "None Found"

def get_grid_size(area):
    return max(.000001, min(area / 2000, 5))

def get_accuracy_radius(area):
    if area < 500:
        return 10
    else:
        return 500