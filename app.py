from fastapi import FastAPI
import uvicorn
import json
import psycopg2
from pydantic import BaseModel
import sys

app = FastAPI(debug=True)

con = psycopg2.connect(
    host="localhost",
    database="test",
    user="ajay",
    password="Postgres@ajay844")


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


@app.get('/get_location/{latitude_v}/{longitude_v}')
async def get_location(latitude_v: float, longitude_v: float):

    try:

        cur = con.cursor()

        query = "Select key,place_name,admin_name1 from Public.location where latitude = (%s) and longitude = (%s);"
        input_data = (latitude_v, longitude_v)
        cur.execute(query, input_data)
        data = cur.fetchall()
        cur.close()

        return {"Details:": data}

    except psycopg2.DatabaseError as error:
        print(error)


@app.post('/post_location/')
async def post_location(item: Item):

    cur = con.cursor()

    query = "Insert into Public.location values(%s,%s,%s,%s,%s,%s);"
    input_data = (item.key, item.place_name, item.admin_name1,
                  item.latitude, item.longitude, item.accuracy)
    cur.execute(query, input_data)
    con.commit()
    cur.close()
    return "Query Executed"


@app.get('/get_using_postgres/{latitude_v}/{longitude_v}')
async def get_using_postgres(latitude_v: float, longitude_v: float):

    cur = con.cursor()

    query = '''select key from location a,
                lateral (
                  select place_name,latitude, longitude from location where latitude = (%s) and longitude = (%s)
                        ) as hr_jax
                where a.place_name <> hr_jax.place_name and
                earth_distance(
                        ll_to_earth(a.latitude, a.longitude),
                        ll_to_earth(hr_jax.latitude, hr_jax.longitude)
                                )/1000 < 5
                order by key;'''

    input_data = (latitude_v, longitude_v)
    cur.execute(query, input_data)
    data = cur.fetchall()
    cur.close()

    return {"Pincodes within the radius of 5 KM:": data}


if __name__ == "main":
    uvicorn.run(app, host="127.0.0.1")
