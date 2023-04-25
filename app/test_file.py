import requests
import json

def main():

    #get token
    url = 'http://127.0.0.1:5000/.login'
    data = '{"username":"mmmax21", "password":"dsci551"}'
    r = requests.post(url,data= data)
    global token
    token = json.loads(r.text)['access_token']


    #clean()
    #create a database & collection test
    url = "http://127.0.0.1:5000/.create_collection/test"
    global headers
    headers = {"Authorization": "Bearer " + token }
    requests.post(url, headers = headers)




    # # #test case1 -- put
    # file_name = "test"
    # data = '{"create_time":1999, "title":"w","content":"cc","author":"dd"}'
    # command = ""
    # correct("post", post_test(file_name, data))
    # correct("get", get_test(file_name,command))
    # #
    # # # special case: get with invalid address
    # # file_name = "dwakdjkalwjda"
    # # url = 'http://127.0.0.1:5000/' + file_name +'.json'
    # # mess = requests.get(url, headers= headers)
    # # print(mess.status_code)
    #
    # #special case: post
    # file_name = "test"
    # data = '{"create_time":1988,  "title":"w","content":"cc","author":"dd"}'
    # correct("post", post_test(file_name, data))
    #
    # file_name = "test"
    # data = '{"create_time":1949,  "title":"w","content":"cc","author":"dd"}'
    # correct("post", post_test(file_name, data))
    #
    # #set name as index
    # indexUrl = "http://127.0.0.1:5000/" + ".create_index/" + "test/" + "create_time"
    # requests.post(indexUrl, headers=headers)
    #
    # #special case: orderBy
    # file_name = "test"
    # command = '?orderBy="create_time"&limitToFirst=1'
    # correct("orderBy", get_test(file_name, command))

    #create_time
    import time

    # Get the current time
    current_time = time.localtime()

    # Format the current time as a string
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)

    # item1 = {"author": "wen"}
    # item2 = {"title": "shikuaiqian"}
    # item3 = {"content": "no cn"}
    # item4 = {"create_time": formatted_time}
    # title = "lng"
    # data = {title: [[item1, item2, item3, item4]]}
    # json_data = json.dumps(data)
    # correct("put", put_test("test", json_data))
    #
    # #specail case: patch
    # file_name = "test"
    #
    # item1 = {"author":"sdd" }
    # item2 = {"title": "dwg"}
    # item3 = {"content":"abc"}
    # item4 = {"create_time":formatted_time}
    # title = "dwg"
    # # Create data dictionary with author key and array value
    # data = {title: [[item1, item2,item3, item4]]}
    #
    #
    # json_data = json.dumps(data)
    # correct("patch", patch_test(file_name, json_data))
    #
    # item1 = {"author": "sawanohiroyuki"}
    # data = [item1, item2, item3,item4]
    # # json_data = json.dumps(data)
    # #correct("patch", patch_test(file_name, json_data))
    #
    # url = "http://127.0.0.1:5000/test/" +title + ".json"
    # res = requests.get(url, headers = headers)
    # res = json.loads(res.text)
    #
    # lastNum = int(list(res)[-1])
    # key = str(lastNum + 1)
    #
    # big_lst =[]
    # for k,v in res.items():
    #     lst =[]
    #     for k2,v2 in v.items():
    #         lst.append(v2)
    #     big_lst.append(lst)
    # big_lst.append(data)
    # print(big_lst)
    # newDict = {key:data}
    # json_data = json.dumps(newDict)
    # requests.patch(url, json_data, headers =headers)
    #
    #
    # #we want to test if we add the 3rd element
    # item1 = {"author": "yagao"}
    # data = [item1, item2, item3, item4]
    # #get from dwg
    # url = "http://127.0.0.1:5000/test/" + title + ".json"
    # res = requests.get(url, headers=headers)
    # res = json.loads(res.text)
    # print("res:")
    # print(res.items())
    #
    # lastNum = int(list(res)[-1])
    # key = str(lastNum + 1)
    #
    # #patch
    # newDict = {key: data}
    # json_data = json.dumps(newDict)
    # requests.patch(url, json_data, headers=headers)


    # #set name as index
    # indexUrl = "http://127.0.0.1:5000/" + ".create_index/" + "test/0/3/" + "create_time"
    # requests.post(indexUrl, headers=headers)
    # indexUrl = "http://127.0.0.1:5000/" + ".create_index/" + "test/1/3/" + "create_time"
    # requests.post(indexUrl, headers=headers)
    # indexUrl = "http://127.0.0.1:5000/" + ".create_index/" + "test/2/3/" + "create_time"
    # requests.post(indexUrl, headers=headers)

    time1 = '2022-04-24 17:44:29'
    time2 = '2021-04-24 17:44:29'
    time3 = '2023-04-24 17:44:29'
    item1 = {"author": "sdd"}
    item2 = {"title": "dwg"}
    item3 = {"content": "abc"}
    item4 = {"create_time": time1}
    # Create data dictionary with author key and array value
    data = [item1, item2, item3, item4]
    #data = {"author": "sdd","title": "dwg","content": "abc","create_time": time1}
    #correct("post", patch_test(file_name, json_data))
    json_data = json.dumps(data)
    file_name = "Order"

    correct("post", post_test(file_name, json_data))

    item4 = {"create_time": time2}
    data= [item1, item2, item3, item4]
    #data = {"author": "sdd", "title": "dwg", "content": "abc", "create_time": time2}
    json_data = json.dumps(data)
    correct("post", post_test(file_name, json_data))
    item4 = {"create_time": time3}
    data = [item1, item2, item3, item4]
    #data = {"author": "sdd", "title": "dwg", "content": "abc", "create_time": time3}
    json_data = json.dumps(data)
    correct("post", post_test(file_name, json_data))



    #special case: orderBy
    indexUrl = "http://127.0.0.1:5000/" + ".create_index/" + "test/3/" + "create_time"
    requests.post(indexUrl, headers=headers)


    file_name = "test"
    command = '?orderBy="3/create_time"&limitToFirst=100'
    #url = 'http://127.0.0.1:5000/test.json?orderBy="3/create_time"&limitToFirst=1'
    correct("orderBy", get_test(file_name, command))

    item1 = {"author": "Max"}
    item2 = {"title": "test"}
    item3 = {"content": "no con"}
    item4 = {"create_time": '2022-04-24 17:44:29'}
    title = "test"
    data = {title: [[item1, item2, item3, item4]]}
    json_data1 = json.dumps(data)

    url4 = "http://127.0.0.1:5000/Publish/" + title + ".json"
    requests.patch(url4, json_data1, headers=headers)

    url2 = "http://127.0.0.1:5000/Email.json"
    email = "louxiaomax@gmailcom"

    url6 = "http://127.0.0.1:5000/Order.json?orderBy='3/create_time'&limitToFirst=1000"
    res=requests.get(url6, headers=headers)
    print(res.status_code == 500)
    # email = "llxxo@utlo"
    # code = "sdwja"
    # data = {email:code}
    # json_data1 = json.dumps(data).replace(" ","")
    #
    # requests.patch(url2, data= json_data1, headers=headers)
    #
    # json_data2 = '{"llx":"sdwja"}'
    # correct("patch", patch_test("test", json_data2))
    # correct("put", put_test("put", json_data2))



    # # special case: get with valid address
    # url = 'http://127.0.0.1:5000/' + "test/Ma" + '.json'
    # mess = requests.get(url, headers=headers)
    # print(json.loads(mess.text) == {})
    #
    # #test case2 -- post
    # file_name = "test"
    # data = '{"Max": "daddy"}'
    # correct("post", post_test(file_name, data))
    #
    # #test case3 -- patch 1 (there exists)
    # file_name = "test"
    # data = '{"Max": 23333}'
    # correct("patch", patch_test(file_name, data))
    #
    # #test case4 -- patch 2 (key not exists in parent menu)
    # file_name = "test/subtest"
    # data = '{"yxj":23331}'
    # correct("patch", patch_test(file_name, data))
    # correct("get", get_test(file_name,command))
    #
    # #test case5 -- patch 3 (key exist )
    # file_name = "test/subtest/ssubtest"
    # data = '{"lcc":123455}'
    # correct("patch", patch_test(file_name, data))
    # correct("get", get_test(file_name,command))
    #
    # #test case6 -- delete ssubtest
    # file_name = "test/subtest/ssubtest"
    # correct("delete", delete_test(file_name))
    # correct("get", get_test("test/subtest",command))
    #
    # #test case7 -- put a list in subtest
    # file_name = "test/subtest"
    # data = '{"school":["usc","ucla","stanford"]}'
    # correct("put", put_test(file_name,data))
    # correct("get", get_test(file_name,command))
    #
    # #test case8 -- put a list in usc
    # file_name = "test/subtest/school/0"
    # data = '{"color":["blue","red","yellow"]}'
    # correct("put", put_test(file_name, data))
    # correct("get", get_test(file_name,command))
    #
    # #test case9 -- delete one element in usc
    # file_name = "test/subtest/school/0/color/1"
    # correct("delete", delete_test(file_name))
    # correct("get", get_test("test/subtest/school/0/color", command))
    #
    # #test case10 -- patch yellow to a list of three colors
    # file_name = "test/subtest/school/0/color/2"
    # data = '{"yellow": ["light y","dark y"]}'
    # correct("patch", patch_test(file_name, data))
    # correct("get", get_test("test/subtest/school/0/color", command))
    #
    # #test case11 -- post new color in yellow
    # file_name = "test/subtest/school/0/color/2"
    # data = '{"yellow": ["light y","dark y"]}'
    # correct("post", post_test(file_name, data))
    #
    # #test case12 -- delete the whole usc
    # file_name = "test/subtest/school/0"
    # correct("delete", delete_test(file_name))
    # correct("get", get_test("test/subtest/school",command))
    #
    # #test case13 -- add elements in usc by patch
    # file_name = "test/subtest/school/usc"
    # data = '{"students":[{"name":"yxj", "id":12},{"name":"lx", "major":"ads", "hobbies":["cook",{"sports":["esport","basketball"]}]}]}'
    # correct("patch", patch_test(file_name, data))
    # correct("get", get_test(file_name,command))
    #
    # #test case14 -- delete hobbies
    # file_name = "test/subtest/school/usc/students/1/hobbies"
    # correct("delete", delete_test(file_name))
    # correct("get", get_test("test/subtest/school/usc/students/1", command))
    #
    # #test case15 -- tried path that does not exist, nothing change
    # file_name = "test/subtest/school/usc/students/1/hobbies"
    # correct("delete", delete_test(file_name))
    # correct("get", get_test("test/subtest/school/usc/students/1", command))
    #
    # # test case15 -- delete with wrong path
    # file_name = "test/subtest/school2/usc/students/"
    # correct("delete", delete_test(file_name))
    #
    # # test case16 -- patch with wrong path -- it works
    # file_name = "test/subtest/school2/usc2/students2/"
    # data = '{"worngpatcj":444}'
    # correct("patch", patch_test(file_name,data))
    #
    # #test case 17 -- put with wrong path  -- it works
    # file_name = "test/subtest/school2/usc8/students8/"
    # data = '{"wrongput":444}'
    # correct("put", put_test(file_name, data))
    #
    # #test case 18 -- post with wrong path  -- it works
    # file_name = "test/subtest/school2/usc9/students9/"
    # data = '{"wrongpost":444}'
    # correct("put", post_test(file_name, data))
    #
    # #test case 19 -- patch with invalid path -- it is detected
    # file_name = "test/.w"
    # data = '{"ppp":444}'
    # correct("patch", patch_test(file_name, data))
    #
    # # test case 20 -- put with invalid path -- it is detected
    # file_name = "test/.w"
    # data = '{"ppp":444}'
    # correct("put", put_test(file_name, data))
    #
    # # test case 21 -- post with invalid path  -- it works
    # file_name = "test/.w"
    # data = '{"wrongpost":444}'
    # #correct("post", post_test(file_name, data)) -- in mongo it is good, but not work in firebase
    #
    # # test case 22 -- delete with invalid path  -- it works
    # file_name = "test/.w"
    # #correct("delete", delete_test(file_name)) -- in mongo it is good, but not work in firebase
    #
    # # test case 23 -- get with invalid path  -- it works
    # correct("get", get_test("test/.w", command))

    # # # test case 24 -- get with right path
    # correct("get", get_test("test/subtest/school", command))
    #
    # #test case 25 -- get with wrong path
    # correct("get", get_test("test/subtest/school8", command))
    #
    # # #look into details
    # # url1 = "http://127.0.0.1:5000/" + "test/subtest/school8" + ".json"
    # # res1 = requests.get(url1, headers=headers)
    # # #res1 = json.loads(res1.text)
    # # print("response from mongo is: " + str(res1))

    #------- ORDERBY/ limitToFirst/ limitToLast/ equalTo/ startAt/ endAt ----
    # print("-------------------Test ORDERBY/ limitToFirst/ limitToLast/ equalTo/ startAt/ endAt")
    # print()
    # print()
    # file_name = "test/ob"
    # name = '["iphone","samsung","vivio","oppo","xiaomi"]'
    # correct("put", put_test(file_name, name))
    #
    # name = ["iphone","samsung","vivio","oppo","xiaomi"]
    # quantity =  [10, 60, 44, 20, 100]
    # price = [9999, 8888, 3333, 4422, 3888]
    #
    # file_name = "test/ob/0"
    # data1 = '{"name":"iphone" , "quantity": 10, "price":9999}'
    # data2 = '{"name":"samsung" , "quantity": 60, "price":8888}'
    # data3 = '{"name":"vivo" , "quantity": 44, "price":3333}'
    # data4 = '{"name":"oppo" , "quantity": 20, "price":4422}'
    # data5 = '{"name":"xiaomi" , "quantity": 100, "price":3888}'
    #
    # correct("patch", patch_test("test/ob/0",data1))
    # correct("patch", patch_test("test/ob/1", data2))
    # correct("patch", patch_test("test/ob/2", data3))
    # correct("patch", patch_test("test/ob/3", data4))
    # correct("patch", patch_test("test/ob/4", data5))
    #
    # #OrderBy1 -- on price
    # #e.g.     ‘….user.json?orderBy="$key"&startAt="102"&print=pretty’
    #
    # #set up price as index
    # indexUrl = "http://127.0.0.1:5000/" + ".create_index/" +"test/" + "price"
    # requests.post(indexUrl,headers = headers)
    #
    # file_name = "test/ob"
    # command ='?orderBy="price"&limitToLast=1'
    # correct("orderBy", get_test(file_name, command)) #should be iphone
    #
    #
    # #OrderBy2 -- on name
    # # set name as index
    # indexUrl = "http://127.0.0.1:5000/" + ".create_index/" + "test/" + "name"
    # requests.post(indexUrl, headers=headers)
    #
    # command = '?orderBy="name"&limitToFirst=1'
    # correct("orderBy", get_test(file_name, command)) #should be iphone

    # # OrderBy3 -- key not exist -- index not defined
    # command = '?orderBy="na"&limitToFirst=1'
    # correct("orderBy", get_test(file_name, command))  # should be iphone
    #
    # # OrderBy4 -- key exits but not labeled as index-- index not defined
    # command = '?orderBy="quantity"&limitToFirst=1'
    # correct("orderBy", get_test(file_name, command))  # should be iphone

    # #startAt & endAt
    # command = '?orderBy="name"&startAt="x"&endAt="z"'
    # correct("startAt", get_test(file_name, command))  # should be xiaomi,vivi
    #
    # #startAt
    # command = '?orderBy="price"&startAt=7000'
    # correct("startAt", get_test(file_name, command))  # should be samsung,iphone
    #
    # #startAt
    # command = '?orderBy="price"&startAt=10000&endAt=9000'
    # correct("startAt", get_test(file_name, command))  # should be null
    #
    # # startAt
    # command = '?orderBy="price"&startAt=10000&endAt=13000'
    # correct("startAt", get_test(file_name, command))  # should be null
    #
    # # # startAt
    # # command = '?orderBy="price"&startAt=-10'
    # # correct("startAt", get_test(file_name, command))  # should be null
    # # #
    # # # endAt
    # # command = '?orderBy="price"&startAt=10&endAt=18.8'
    # # correct("endAt", get_test(file_name, command))  # should be null
    #
    # #endtAt
    # command = '?orderBy="price"&startAt=7000&endAt=9000'
    # correct("endAt", get_test(file_name, command))  # should be samsung
    #
    #
    #
    # #equalTo
    # command = '?orderBy="price"&equalTo=8888'
    # correct("startAt", get_test(file_name, command))  # should be samsung
    #
    # # equalTo
    # command = '?orderBy="quantity"&equalTo=20'
    # correct("equalTo", get_test(file_name, command))  # should be samsung
    #
    # #equalTo
    # command = '?orderBy="name"&equalTo="vivo"'
    # correct("equalTo", get_test(file_name, command))  # should be vivo
    #
    # #equalTo
    # command = '?orderBy="name"&equalTo="vivwwwo"'
    # correct("equalTo", get_test(file_name, command))  # should be null
    #
    # #limitToFirst
    # command = '?orderBy="name"&limitToFirst=2'
    # correct("limitToFirst", get_test(file_name, command))  # should be
    #
    # # limitToFirst
    # command = '?orderBy="name"&limitToFirst=-1'
    # correct("limitToFirst", get_test(file_name, command))  # should be
    #
    # # set quantity as index
    # indexUrl = "http://127.0.0.1:5000/" + ".create_index/" + "test/" + "quantity"
    # requests.post(indexUrl, headers=headers)
    #
    # # limitToFirst
    # command = '?orderBy="quantity"&limitToFirst=1'
    # correct("limitToFirst", get_test(file_name, command))  # should be
    #
    # # limitToFirst
    # command = '?orderBy="quantity"&limitToFirst=20'
    # correct("limitToFirst", get_test(file_name, command))  # should be
    #
    # # limitToLast
    # command = '?orderBy="name"&limitToLast=2'
    # correct("limitToLast", get_test(file_name, command))  # should be
    #
    # # limitToLast
    # command = '?orderBy="quantity"&limitToLast=1'
    # correct("limitToLast", get_test(file_name, command))  # should be
    #
    # # limitToLast
    # command = '?orderBy="quantity"&limitToLast=-1'
    # correct("limitToLast", get_test(file_name, command))  # should be error
    #
    # # limitToLast
    # command = '?orderBy="quantity"&limitToLast=20'
    # correct("limitToLast", get_test(file_name, command))  # should be error


    #clean()





def get_test(file_name, command =None):
    url1 = "http://127.0.0.1:5000/" + file_name + ".json" + command
    res1 = requests.get(url1, headers=headers)
    res1 = json.loads(res1.text)
    print("response from mongo is: " + str(res1))

    url2 = "https://cloudcomputing1-f0a9c-default-rtdb.firebaseio.com/" + file_name + ".json" + command
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