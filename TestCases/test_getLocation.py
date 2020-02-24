# from starlette.testclient import TestClient

# from .app import app

# client = TestClient(app)


# def test_getlocation():
#     response = client.get("/post_location/")
#     assert response.status_code == 200
#     assert response.json() == {"pincode": ["IN/144101", "Patara", "Punjab"], "address:": [
#         "IN/144102", "Adampur Doaba", "Punjab"], "city:": ["IN/144103", "Adampur A D", "Punjab"]}


# def test_postlocation():

#     response = client.post(
#         "/post_location/",
#         headers={"accept": "application/json",
#                  "Content-Type": "application/json"},
#         json={"key": "IN/110030", "place_name": "Mehrauli", "admin_name1": "New Delhi",
#               "latitude": 28.522, "longitude": 78.102, "accuracy": 0},
#     )
#     assert response.status_code == 200
#     assert response.json() == "Query Executed"
