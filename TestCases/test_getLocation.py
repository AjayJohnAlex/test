import requests
import json


get_url = "http://127.0.0.1:8000/get_location/31.3654/75.7531"

post_url = "http://127.0.0.1:8000/post_location/"
post_body = {"key": "IN/110030", "place_name": "Mehrauli", "admin_name1": "New Delhi",
             "latitude": 28.522, "longitude": 78.102, "accuracy": 0}
# post_body = json.loads(body)


def test_getlocation(get_url):

    repsonse = requests.get(get_url)
    res = repsonse.content

    assert res == b'{"pincode":["IN/144101","Patara","Punjab"],"address:":["IN/144102","Adampur Doaba","Punjab"],"city:":["IN/144103","Adampur A D","Punjab"]}'


def test_postlocation(post_url, post_body):

    repsonse = requests.post(post_url, post_body)
    print(repsonse.content)
    assert repsonse.status_code == 200


# test_getlocation(get_url)
# test_postlocation(post_url, post_body)
