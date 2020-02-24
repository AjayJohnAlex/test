from fastapi import FastAPI
import uvicorn
import json
import sqlalchemy
import psycopg2
from pydantic import BaseModel

app = FastAPI(debug=True)

with open("pincode.json") as f:

    location = json.loads(f.read())


con = psycopg2.connect(
    host="localhost",
    database="test",
    user="ajay",
    password="Postgres@ajay844")


cur = con.cursor()

# class Item(BaseModel):
#     key: str = None
#     place_name: str = None
#     admin_name1: str = None
#     latitude: float = None
#     longitude: float = None
#     accuracy: int = None


@app.get('/')
async def root():
    return "Hello , This is a Test project."


@app.get('/get_location/')
async def get_location(latitude: float, longitude: float,):

    pincode = [i['key'] for i in location if i['latitude']
               == latitude and i['longitude'] == longitude]
    address = [i['place_name'] for i in location if i['latitude']
               == latitude and i['longitude'] == longitude]
    city = [i['admin_name1'] for i in location if i['latitude']
            == latitude and i['longitude'] == longitude]

    return {"pincode": pincode, "address:": address, "city:": city}


@app.post('/post_location/')
async def post_location(q_key: str,
                        q_place_name: str,
                        q_admin_name1: str,
                        q_latitude: float,
                        q_longitude: float,
                        q_accuracy: int):

    # cur.execute("Insert into Public.location (key, place_name, admin_name1, latitude, longitude, accuracy) values('IN/110030', 'Mehrauli', 'New Delhi', 28.5222, 77.1803, 0);")


    cur.execute("Insert into Public.location(key, place_name, admin_name1, latitude, longitude, accuracy) values('q_key', 'q_place_name', 'q_admin_name1', q_latitude, q_longitude, q_accuracy);")

    cur.commit()

    # data_dict = data.dict()
    return "Record Enter in database"

if __name__ == "main":
    uvicorn.run(app, host="127.0.0.1")
