import requests
import json
import time

def header_getter():
    url = 'http://127.0.0.1:5000/.login'
    data = '{"username":"mmmax21", "password":"dsci551"}'
    r = requests.post(url, data=data)
    token = json.loads(r.text)['access_token']
    headers = {"Authorization": "Bearer " + token}
    return headers

def collection_creator(table, headers):
    url = "http://127.0.0.1:5000/.create_collection/" + table
    requests.post(url, headers=headers)

def input_transform(input):
    return input.replace(".","")

def password_getter(email):
    if email != None:
        email = input_transform(email)
        url1 = "http://127.0.0.1:5000/User/" + email + ".json"
        headers = header_getter()
        res = requests.get(url1, headers = headers)
        user_password = res.text
        return user_password
    else:
        return

def add_account(email, user_password):
    url1 = "http://127.0.0.1:5000/User.json"
    headers = header_getter()
    email = input_transform(email)
    data = {email: user_password}
    json_data = json.dumps(data).replace(" ","")
    requests.patch(url1, json_data, headers = headers)

def add_email(email, code):
    url2 = "http://127.0.0.1:5000/Email.json"
    headers = header_getter()
    email = input_transform(email)
    data = {email:code}
    json_data = json.dumps(data).replace(" ","")
    requests.patch(url2, json_data, headers=headers)

def codeFromDB(email):
    email = input_transform(email)
    url3 = 'http://127.0.0.1:5000/Email/'+ email + '.json'
    headers = header_getter()
    res = requests.get(url3, headers = headers)
    code = res.text
    return code

def deletefromEmail(email):
    email = input_transform(email)
    url3 = "http://127.0.0.1:5000/Email/" +email + ".json"
    headers = header_getter()
    requests.delete(url3, headers = headers)

def question_saver(title,content,author):
    title = input_transform(title)
    content = input_transform(content)
    author = input_transform(author)
    url3 = "http://127.0.0.1:5000/Publish/" + ".json"
    headers = header_getter()
    create_time = time.strftime('%Y-%m-%d %H:%M', time.localtime())

    item1 = {"author": author}
    item2 = {"title": title}
    item3 = {"content": content}
    item4 = {"create_time": create_time}
    data = {title: [[item1, item2,item3, item4]]}
    json_data1 = json.dumps(data)

    #check if the title already exists
    url4 = "http://127.0.0.1:5000/Publish/" + title+ ".json"
    res = requests.get(url4, headers = headers)
    res = json.loads(res.text)

    if res != {}:
        lastNum = int(list(res)[-1])
        key = str(lastNum + 1)
        newDict = {key: data}
        json_data2 = json.dumps(newDict)
        requests.patch(url4, json_data2, headers=headers)
    else:
        requests.patch(url3,json_data1,headers=headers)

    #store the question in ordertable
    url5 = "http://127.0.0.1:5000/Order/" +".json"
    data = [item1, item2,item3, item4]
    json_data3 = json.dumps(data)
    requests.post(url5,json_data3,headers=headers)

    return data

def get_question(title):
    title = input_transform(title)
    url3 = "http://127.0.0.1:5000/Publish/" + title + ".json"
    headers = header_getter()
    res = requests.get(url3, headers = headers)
    question = json.loads(res.text)
    return question

def get_question_from_order(): #//get all questions
    url6 = "http://127.0.0.1:5000/Order.json?orderBy='3/create_time'&limitToFirst=1000"
    #url6 = "http://127.0.0.1:5000/Order.json?orderBy='3/create_time'"

    headers = header_getter()
    res = requests.get(url6, headers=headers)
    question = list(json.loads(res.text).values())

    return question



