from fastapi import FastAPI
import uvicorn
import json
import psycopg2
from pydantic import BaseModel

app = FastAPI(debug=True)


con = psycopg2.connect(
    host="localhost",
    database="test",
    user="ajay",
    password="Postgres@ajay844")


@app.get('/')
async def root():
    return "Hello , This is a Test project."


@app.get('/get_location/')
async def get_location(latitude: float, longitude: float):

    try:

        pincode = []
        address = []
        city = []

        cur = con.cursor()

        query = "Select key,place_name,admin_name1 from Public.location where latitude = latitude and longitude = longitude;"

        cur.execute(query)
        data = cur.fetchall()
        for i in data:
            pincode.append(i[0])
            address.append(i[1])
            city.append(i[2])

        cur.close()

        return {"pincode": pincode[0], "address:": address[0], "city:": city[0]}

    except psycopg2.DatabaseError as error:
        print(error)


@app.post('/post_location')
async def post_location(
        key: str,
        place_name: str,
        admin_name1: str,
        latitude: float,
        longitude: float,
        accuracy: int,):

    try:

        cur = con.cursor()

        query = "Insert into Public.location values(key, place_name, admin_name1, latitude, longitude, accuracy);"

        cur.execute(query)

        cur.close()
        return {"Query updated Successfully."}

    except psycopg2.DatabaseError as error:
        print(error)


if __name__ == "main":
    uvicorn.run(app, host="127.0.0.1")
