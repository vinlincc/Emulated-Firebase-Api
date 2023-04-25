
import requests
import json
from test_file import correct,post_test

def main():
    # get token
    url = 'http://127.0.0.1:5000/.login'
    data = '{"username":"mmmax21", "password":"dsci551"}'
    r = requests.post(url, data=data)
    global token
    token = json.loads(r.text)['access_token']

    # clean()
    # create a database & collection test
    url = "http://127.0.0.1:5000/.create_collection/test"
    global headers
    headers = {"Authorization": "Bearer " + token}
    requests.post(url, headers=headers)

    time1 = '2022-04-24 17:44:29'
    time2 = '2021-04-24 17:44:29'
    time3 = '2023-04-24 17:44:29'
    item1 = {"author": "sdd"}
    item2 = {"title": "dwg"}
    item3 = {"content": "abc"}
    item4 = {"create_time": time1}
    # Create data dictionary with author key and array value
    data = [item1, item2, item3, item4]
    # data = {"author": "sdd","title": "dwg","content": "abc","create_time": time1}
    # correct("post", patch_test(file_name, json_data))
    json_data = json.dumps(data)
    file_name = "Order"

    correct("post", post_test(file_name, json_data))

    item4 = {"create_time": time2}
    data = [item1, item2, item3, item4]
    # data = {"author": "sdd", "title": "dwg", "content": "abc", "create_time": time2}
    json_data = json.dumps(data)
    correct("post", post_test(file_name, json_data))
    item4 = {"create_time": time3}
    data = [item1, item2, item3, item4]
    # data = {"author": "sdd", "title": "dwg", "content": "abc", "create_time": time3}
    json_data = json.dumps(data)
    correct("post", post_test(file_name, json_data))

main()