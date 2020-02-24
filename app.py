from fastapi import FastAPI
import uvicorn
import json
import psycopg2
from pydantic import BaseModel
import sys

app = FastAPI(debug=True)

print(sys.version)

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

        return {"pincode": data[0], "address:": data[1], "city:": data[2]}

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


if __name__ == "main":
    uvicorn.run(app, host="127.0.0.1")
