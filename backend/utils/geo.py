import json
from psycopg2 import connect

def get_ipv4_networks_for_bbox(bbox):
    try:
        connection = connect(
            host="127.0.0.1",
            database='postgres',
            port='5432')

        cursor = connection.cursor()
        # print(bbox)
        cursor.execute(f"select st_asgeojson(geometry) from ipv4geo where st_within(geometry, ST_MakeEnvelope({bbox['_southWest']['lng']}, {bbox['_southWest']['lat']}, {bbox['_northEast']['lng']}, {bbox['_northEast']['lat']}, 4326))")
        items = cursor.fetchmany(100)
        return json.dumps(items)
    except Exception as e:
        print("EXCEPTION", e)
    finally:
        if connection:
            cursor.close()
            connection.close()
    return "None Found"

    