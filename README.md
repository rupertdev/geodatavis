IP Address Geo Data Visualization

Setup:
1. Create a Postgres Database
2. Install PostGIS with `CREATE EXTENSION postgis;`
3. Create a table for the IPv4 geo data with:
```sql
CREATE TABLE ipv4geo(
network text,
geoname_id int,
registered_country_geoname_id int,
represented_country_geoname_id int,
is_anonymous_proxy BOOLEAN,
is_satellite_provider BOOLEAN,
postal_code int,
latitude float8,
longitude float8,
accuracy_radius int,

PRIMARY KEY(network)
)
```
4. Create geography column with `SELECT AddGeometryColumn('ipv4geo', 'geometry', 4326, 'POINT', 2);`
5. Copy in data from CSV file with 
```
COPY ipv4geo
FROM '/Users/rupert/projects/geodatavis/data/GeoLite2-City-Blocks-IPv4.csv'
CSV DELIMITER ',' HEADER;
```
6. Create a spacial index with `CREATE INDEX geometry_gix ON ipv4geo USING GIST (geometry);`
7. Vacuum the table to make sure the index is used to its full advantage `VACUUM ipv4geo;`
