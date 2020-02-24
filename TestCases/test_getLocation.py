import requests


get_url = "http://127.0.0.1:8000/get_location/?latitude=28.6333&longitude=77.25"

post_url = "http://127.0.0.1:8000/post_location?key=IN%2110030&place_name=Mehrauli&admin_name1=New%20Delhi&latitude=28.522&longitude=78.18&accuracy=0"


def test_getlocation():

    repsonse = requests.get(get_url)
    res = repsonse.content

    assert res == b'{"pincode":"IN/110001","address:":"Connaught Place","city:":"New Delhi"}'
    assert repsonse.status_code == 200


def test_postlocation():
    repsonse = requests.get(post_url)
    res = repsonse.content

    assert repsonse.status_code = 200
