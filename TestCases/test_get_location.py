# from fastapi import FastAPI
# import uvicorn
# import json
# import sqlalchemy
# import psycopg2
# from pydantic import BaseModel
import requests

url = 'http://127.0.0.1:8000/get_location/?latitude=28.6333&longitude=77.2167'


# class test_getLocation():

response = requests.get(url)

print(response.content)
