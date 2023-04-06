import json

import requests
import json

def main():

    #get token
    url = 'http://127.0.0.1:5000/.login'
    data = '{"username":"mmmax21", "password":"dsci551"}'
    r = requests.post(url,data= data)
    global token
    token = json.loads(r.text)['access_token']

    #create a database & collection test
    url = "http://127.0.0.1:5000/.create_collection/test"
    global headers
    headers = {"Authorization": "Bearer " + token }
    requests.post(url, headers = headers)

    # #test case1 -- put
    file_name = "test"
    data = '{"Max": "daddy"}'
    correct("put", put_test(file_name, data))
    correct("get", get_test(file_name))

    #test case2 -- post
    file_name = "test"
    data = '{"Max": "daddy"}'
    correct("post", post_test(file_name, data))

    #test case3 -- patch 1 (there exists)
    file_name = "test"
    data = '{"Max": 23333}'
    correct("patch", patch_test(file_name, data))

    #test case4 -- patch 2 (key not exists in parent menu)
    file_name = "test/subtest"
    data = '{"yxj":23331}'
    correct("patch", patch_test(file_name, data))
    correct("get", get_test(file_name))

    #test case5 -- patch 3 (key exist )
    file_name = "test/subtest/ssubtest"
    data = '{"lcc":123455}'
    correct("patch", patch_test(file_name, data))
    correct("get", get_test(file_name))

    #test case6 -- delete ssubtest
    file_name = "test/subtest/ssubtest"
    correct("delete", delete_test(file_name))
    correct("get", get_test("test/subtest"))

    #test case7 -- put a list in subtest
    file_name = "test/subtest"
    data = '{"school":["usc","ucla","stanford"]}'
    correct("put", put_test(file_name,data))
    correct("get", get_test(file_name))

    #test case8 -- put a list in usc
    file_name = "test/subtest/school/0"
    data = '{"color":["blue","red","yellow"]}'
    correct("put", put_test(file_name, data))
    correct("get", get_test(file_name))

    #test case9 -- delete one element in usc
    file_name = "test/subtest/school/0/color/1"
    correct("delete", delete_test(file_name))
    correct("get", get_test("test/subtest/school/0/color"))

    #test case10 -- patch yellow to a list of three colors
    file_name = "test/subtest/school/0/color/2"
    data = '{"yellow": ["light y","dark y"]}'
    correct("patch", patch_test(file_name, data))
    correct("get", get_test("test/subtest/school/0/color"))

    #test case11 -- post new color in yellow
    file_name = "test/subtest/school/0/color/2"
    data = '{"yellow": ["light y","dark y"]}'
    correct("post", post_test(file_name, data))

    #test case12 -- delete the whole usc
    file_name = "test/subtest/school/0"
    correct("delete", delete_test(file_name))
    correct("get", get_test("test/subtest/school"))

    #test case13 -- add elements in usc by patch
    file_name = "test/subtest/school/usc"
    data = '{"students":[{"name":"yxj", "id":12},{"name":"lx", "major":"ads", "hobbies":["cook",{"sports":["esport","basketball"]}]}]}'
    correct("patch", patch_test(file_name, data))
    correct("get", get_test(file_name))

    #test case14 -- delete hobbies
    file_name = "test/subtest/school/usc/students/1/hobbies"
    correct("delete", delete_test(file_name))
    correct("get", get_test("test/subtest/school/usc/students/1"))

    #test case15 -- tried path that does not exist, nothing change
    file_name = "test/subtest/school/usc/students/1/hobbies"
    correct("delete", delete_test(file_name))
    correct("get", get_test("test/subtest/school/usc/students/1"))

    # test case15 -- delete with wrong path
    file_name = "test/subtest/school2/usc/students/"
    correct("delete", delete_test(file_name))




    # test case16 -- patch with wrong path -- it works
    file_name = "test/subtest/school2/usc2/students2/"
    data = '{"worngpatcj":444}'
    correct("patch", patch_test(file_name,data))

    #test case 17 -- put with wrong path  -- it works
    file_name = "test/subtest/school2/usc8/students8/"
    data = '{"wrongput":444}'
    correct("put", put_test(file_name, data))

    #test case 18 -- post with wrong path  -- it works
    file_name = "test/subtest/school2/usc9/students9/"
    data = '{"wrongpost":444}'
    correct("put", post_test(file_name, data))

    #test case 19 -- patch with invalid path -- it is detected
    file_name = "test/.w"
    data = '{"ppp":444}'
    correct("patch", patch_test(file_name, data))

    # test case 20 -- put with invalid path -- it is detected
    file_name = "test/.w"
    data = '{"ppp":444}'
    correct("put", put_test(file_name, data))

    # test case 21 -- post with invalid path  -- it works
    file_name = "test/.w"
    data = '{"wrongpost":444}'
    #correct("post", post_test(file_name, data)) -- in mongo it is good, but not work in firebase

    # test case 22 -- delete with invalid path  -- it works
    file_name = "test/.w"
    #correct("delete", delete_test(file_name)) -- in mongo it is good, but not work in firebase

    # test case 23 -- get with invalid path  -- it works
    correct("get", get_test("test/.w"))

    # test case 24 -- get with right path
    correct("get", get_test("test/subtest/school"))

    #test case 25 -- get with wrong path
    #correct("get", get_test("test/subtest/school8"))

    #look into details
    url1 = "http://127.0.0.1:5000/" + "test/subtest/school8" + ".json"
    res1 = requests.get(url1, headers=headers)
    #res1 = json.loads(res1.text)
    print("response from mongo is: " + str(res1))

    #clean()




def get_test(file_name):
    url1 = "http://127.0.0.1:5000/" + file_name + ".json"
    res1 = requests.get(url1, headers=headers)
    res1 = json.loads(res1.text)
    print("response from mongo is: " + str(res1))

    url2 = "https://cloudcomputing1-f0a9c-default-rtdb.firebaseio.com/" + file_name + ".json"
    res2 = requests.get(url2)
    res2 = json.loads(res2.text)
    res2 = input_data_transform(res2)
    print("response from firebase is: " + str(res2))

    return res1 == res2

def put_test(file_name,data):
    url1 = "http://127.0.0.1:5000/" + file_name + ".json"
    res1 = requests.put(url1, data, headers=headers)
    res1 = json.loads(res1.text).get('data')
    print("response from mongo is: " + str(res1))

    url2 = "https://cloudcomputing1-f0a9c-default-rtdb.firebaseio.com/" + file_name + ".json"
    res2 = requests.put(url2, data)
    res2 = json.loads(res2.text)
    res2 = input_data_transform(res2)
    print("response from firebase is: " +str(res2))

    return res1 == res2

def patch_test(file_name,data):
    url1 = "http://127.0.0.1:5000/" + file_name + ".json"
    res1 = requests.patch(url1, data, headers=headers)
    res1 = json.loads(res1.text).get('data')
    print("response from mongo is: " + str(res1))

    url2 = "https://cloudcomputing1-f0a9c-default-rtdb.firebaseio.com/" + file_name + ".json"
    res2 = requests.patch(url2, data)
    res2 = json.loads(res2.text)
    res2 = input_data_transform(res2)
    print("response from firebase is: " +str(res2))

    return res1 == res2

def post_test(file_name, data):
    url1 = "http://127.0.0.1:5000/" + file_name + ".json"
    res1 = requests.post(url1, data, headers=headers)
    res1 = json.loads(res1.text).get('data')
    print("response from mongo is: " + str(res1))

    url2 = "https://cloudcomputing1-f0a9c-default-rtdb.firebaseio.com/" + file_name + ".json"
    res2 = requests.post(url2, data)
    name = json.loads(res2.text).get('name')
    new_url2 = "https://cloudcomputing1-f0a9c-default-rtdb.firebaseio.com/" + file_name + "/" + name + ".json"
    res2 = requests.get(new_url2)
    res2 = json.loads(res2.text)
    res2 = input_data_transform(res2)
    print("response from firebase is: " +str(res2))

    return res1 == res2

def delete_test(file_name):
    url1 = "http://127.0.0.1:5000/" + file_name + ".json"
    res1 = requests.delete(url1, headers=headers)
    res1 = json.loads(res1.text)
    print("response from mongo is: " + str(res1))

    url2 = "https://cloudcomputing1-f0a9c-default-rtdb.firebaseio.com/" + file_name + ".json"
    res2 = requests.delete(url2)
    res2 = json.loads(res2.text)
    print("response from firebase is: " + str(res2))

    #if delete successflly, res2 will be null but res1 will be different
    #detect if res1 return good news
    if res1.get('message').split(" ")[-1] == "successfully":
        res1 = None
    return res1 == res2

def correct(method, result):
    if result == True:
        print(f"Method {method} is correct")
    else:
        print(f"***** Method {method} has problem ******")

def input_data_transform(input_data):
    if isinstance(input_data, list):
        return {str(i):input_data_transform(n) for i, n in enumerate(input_data) if n is not None}
    if isinstance(input_data, dict):
        return {k:input_data_transform(v) for k, v in input_data.items() }
    return input_data

def clean():
    #clean all the tables
    url1 = "http://127.0.0.1:5000/.json"
    headers = {"Authorization": "Bearer " + token}
    requests.delete(url1, headers=headers)

    url2 = "https://cloudcomputing1-f0a9c-default-rtdb.firebaseio.com/.json"
    requests.delete(url2)

main()