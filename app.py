from fastapi import FastAPI
import uvicorn
import json
import psycopg2
from pydantic import BaseModel
import sys
from config import config

app = FastAPI(debug=True)

# https://www.postgresqltutorial.com/postgresql-python/connect/ : refernce for db connectivity
params = config()

# connect to the PostgreSQL server
# print('Connecting to the PostgreSQL database...')
con = psycopg2.connect(**params)

# create a cursor
cur = con.cursor()


class Item(BaseModel):

    key: str
    place_name: str
    admin_name1: str
    latitude: float
    longitude: float
    accuracy: int


@app.get('/')
async def root():
    return "Hello , This is a Test project."

# Get api - /get_location : Given lat,lng ... it will fetch pin code, address, city as a json response.


@app.get('/get_location/{latitude_v}/{longitude_v}')
async def get_location(latitude_v: float, longitude_v: float):

    try:

        # cur = con.cursor()

        query = "Select key,place_name,admin_name1 from Public.location where latitude = (%s) and longitude = (%s);"
        input_data = (latitude_v, longitude_v)
        cur.execute(query, input_data)
        data = cur.fetchall()
        # cur.close()

        return {"Details:": data}

    except psycopg2.DatabaseError as error:
        print(error)

# Post api - /post_location : Post lat,lng of any location with pin code+address+city. This api will add new pin code in db.


@app.post('/post_location/')
async def post_location(item: Item):

    # cur = con.cursor()
    try:

        query = "Insert into Public.location values(%s,%s,%s,%s,%s,%s);"
        input_data = (item.key, item.place_name, item.admin_name1,
                      item.latitude, item.longitude, item.accuracy)
        cur.execute(query, input_data)
        con.commit()
        # cur.close()
        return "Query Executed"

    except psycopg2.DatabaseError as error:
        print(error)

# Get api - / get_using_postgres : using postgres "earthdistance" to compute all points in 5km radius


@app.get('/get_using_postgres/{latitude_v}/{longitude_v}')
async def get_using_postgres(latitude_v: float, longitude_v: float):

    # cur = con.cursor()
    try:

        query = '''select key from (
                           select key, earth_distance(
                               ll_to_earth(a.latitude, a.longitude),
                               ll_to_earth(p.latpoint, p.longpoint)
                               ) / 1000 as distance
                    from location a
                    join (   /* these are the query parameters */
                             select  (%s)  AS latpoint,  (%s)AS longpoint
                          ) AS p ON 1=1

                    ) as s
                    where distance <= 5
                    order by distance;'''

        input_data = (latitude_v, longitude_v)
        cur.execute(query, input_data)
        data = cur.fetchall()
        # cur.close()

        return {"Pincodes within the radius of 5 KM:": data}

    except psycopg2.DatabaseError as error:
        print(error)
# Get api - / get_using_self :/get_using_self - Implement the mathematical computation yourself
# https://www.plumislandmedia.net/mysql/haversine-mysql-nearest-loc/ refernce for formula

@app.get('/get_using_self/{latitude_v}/{longitude_v}')
async def get_using_self(latitude_v: float, longitude_v: float):

    # cur = con.cursor()
    try:

        query = '''
        select key from (
        select z.key,
            p.distance_unit * DEGREES(ACOS(GREATEST(1.0, COS(RADIANS(p.latpoint)) * COS(RADIANS(z.latitude))
             * COS(RADIANS(p.longpoint - z.longitude)) + SIN(RADIANS(p.latpoint)) * SIN(RADIANS(z.latitude))))) AS distance
        from location AS z
        join (   /* these are the query parameters */
            select  (%s) AS latpoint,  (%s) AS longpoint,
                    5 AS radius,      111.045 AS distance_unit
            ) AS p ON 1=1
        where z.latitude
            between p.latpoint  - (p.radius / p.distance_unit)
                and p.latpoint  + (p.radius / p.distance_unit)
        and z.longitude
            between p.longpoint - (p.radius / (p.distance_unit * COS(RADIANS(p.latpoint))))
                and p.longpoint + (p.radius / (p.distance_unit * COS(RADIANS(p.latpoint))))
         ) as s
        where distance <= 5
        order by distance
     '''
        input_data = (latitude_v, longitude_v)
        cur.execute(query, input_data)
        data = cur.fetchall()
        # cur.close()

        return {"Pincodes within the radius of 5 KM:": data}

    except psycopg2.DatabaseError as error:
        print(error)


if __name__ == "main":
    uvicorn.run(app, host="127.0.0.1")
