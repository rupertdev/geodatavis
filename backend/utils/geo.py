import json
import os
from psycopg2 import connect
from shapely.geometry import box


def get_ipv4_networks_for_bbox(bbox):
    try:
        return_points = []
        connection = connect(
            host=os.environ.get('POSTGRES_DB_HOST', 'localhost'),
            database=os.environ.get('POSTGRES_DB_DATABASE', 'postgres'),
            user=os.environ.get('POSTGRES_DB_USER', 'postgres'),
            password=os.environ.get('POSTGRES_DB_PASSWORD'),
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
    return []


def get_grid_size(area):
    return max(.000001, min(area / 2000, 5))


def get_accuracy_radius(area):
    return 10 if area < 500 else 500
