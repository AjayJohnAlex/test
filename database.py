import psycopg2
import json

# connect to database
con = psycopg2.connect(

    host="localhost",
    database="test",
    user="ajay",
    password="Postgres@ajay844")

# json file
with open("pincode.json") as f:

    location = json.loads(f.read())

# cursor
cur = con.cursor()
cur.execute(
    "copy PUBLIC.\"location\" from '/home/ajay/FASTAPI/pincode.csv' DELIMITER ',' CSV HEADER ;")
cur.commit()
con.close()
