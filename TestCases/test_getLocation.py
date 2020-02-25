from starlette.testclient import TestClient

from .app import app

client = TestClient(app)

# Get api - /get_location : Given lat,lng ... it will fetch pin code, address, city as a json response.


def test_getlocation():
    response = client.get("/get_location/28.6333/77.2167")
    assert response.status_code == 200
    assert response.json() == {
        "Details:": [
            [
                "IN/110001",
                "Connaught Place",
                "New Delhi"
            ]
        ]
    }

# Post api - /post_location : Post lat,lng of any location with pin code+address+city. This api will add new pin code in db.


def test_postlocation():

    response = client.post(
        "/post_location/",
        headers={"accept": "application/json",
                 "Content-Type": "application/json"},
        json={"key": "IN/110030", "place_name": "Mehrauli", "admin_name1": "New Delhi",
              "latitude": 28.522, "longitude": 78.102, "accuracy": 0},
    )
    assert response.status_code == 200
    assert response.json() == "Query Executed"

# Checking the results of using the different methods have been done through requests response data.

# Get api - / get_using_postgres using postgres "earthdistance" to compute all points in 5km radius


def test_getUsingPostgres():
    response = client.get("/get_using_postgres/28.6833/77.25")
    assert response.status_code == 200
    assert response.json() == {
        "Pincodes within the radius of 5 KM:": [
            [
                "IN/110007"
            ],
            [
                "IN/110003"
            ],
            [
                "IN/110004"
            ],
            [
                "IN/110006"
            ],
            [
                "IN/110008"
            ]
        ]
    }

# Get api - / get_using_self :/get_using_self - Implement the mathematical computation yourself


def test_getUsingSelf():
    response = client.get("/get_using_self/28.6833/77.25")
    assert response.status_code == 200
    assert response.json() == {
        "Pincodes within the radius of 5 KM:": [
            [
                "IN/110003"
            ],
            [
                "IN/110004"
            ],
            [
                "IN/110005"
            ],
            [
                "IN/110006"
            ],
            [
                "IN/110007"
            ],
            [
                "IN/110008"
            ]
        ]
    }
