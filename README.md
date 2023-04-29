# dsci551

## Setup

The following setup is under MacOS. If you are using another operating system, please search on the internet or contact us.

### 1. Python Virtual Environment

Python is assumed to be installed before this procedure.

Open your terminal, input command:

```bash
python -m venv venv
```

And run command:

```bash
source venv/bin/activate
```

Run pip install related packages:

```bash
pip install -r requirements.txt
```

### 2. Secret Key

A secret key is necessary in this project. Input command:

```bash
export JWT_SECRET_KEY="6cfb8684b95028909c82dcea7244cb04f009f0a07dde210f71e00b97f663a144"
```

Or use your own secret key.

### 3. MongoDB

MongoDB is assumed to be installed, and MongoDB replica set should be properly set up. In the following instructions, we set up a MongoDB replica set locally.

#### a. Kill the possible local mongo process that uses the port 27017, please use the PID that runs the process

```bash
sudo lsof -i:27017
sudo kill PID
```

#### b. Create resources directories for replica set (please use your own path)

```bash
sudo mkdir -p /your/path/to/rs1
sudo mkdir -p /your/path/to/rs2
sudo mkdir -p /your/path/to/rs3
sudo chmod 755 /your/path/to/rs*
```

#### c. Start 3 mongo processes

The terminal tool screen is assumed to be installed before this procedure.

```bash
screen -S mongodb1
sudo mongod --port 27017 --dbpath /your/path/to/rs1 --replSet myReplicaSet --bind_ip localhost
ctrl-a d (leave the screen session)
screen -S mongodb2
sudo mongod --port 27018 --dbpath /your/path/to/rs2 --replSet myReplicaSet --bind_ip localhost
ctrl-a d (leave the screen session)
screen -S mongodb3
sudo mongod --port 27019 --dbpath /your/path/to/rs3 --replSet myReplicaSet --bind_ip localhost
ctrl-a d (leave the screen session)
```

#### d. Start replica set in mongosh

```bash
mongosh --port 27017
```

Inside the mongosh:

```javascript
rs.initiate({ _id: "myReplicaSet", members: [ { _id: 0, host: "localhost:27017" }] })
rs.add("localhost:27018")
rs.add("localhost:27019")
```

You can check the health status for each port with `rs.status()`.

## Start the Emulated Firebase (locally)
Go to the project directory, and activate the virtual environment.
```bash
source venv/bin/activate
```
Start the flask app:
```bash
python main.py
```
Now the flask app should be running on http://127.0.0.1:5000

## User Registration, Create Collection, Index and Listener (POST methods)
To enable users to manage their data separately and securely, we have user registration and user login api.
```bash
curl -X POST 'localhost:5000/.register' -d '{"username":"dsci551","password":"123"}' 
```
It will return {"result":"User created"}
```bash
curl -X POST 'localhost:5000/.login' -d '{"username":"dsci551","password":"123"}' 
```
It will return {"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MjczMDI3NSwianRpIjoiNzNhN2E2NmYtMDk2ZC00NzhlLTllOTQtOGIxMDk1NDNmNGIyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRzY2k1NTEiLCJuYmYiOjE2ODI3MzAyNzV9.PoatX68cG3WAF5DoT2JMnmwxTGykXOyepUUPiBLqxHo"}
You should always inlcude a header -H "Authorization: Bearer {token}" for any operations other than register and login.
Take creating a collection as an example:
```bash
curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MjczMDI3NSwianRpIjoiNzNhN2E2NmYtMDk2ZC00NzhlLTllOTQtOGIxMDk1NDNmNGIyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRzY2k1NTEiLCJuYmYiOjE2ODI3MzAyNzV9.PoatX68cG3WAF5DoT2JMnmwxTGykXOyepUUPiBLqxHo" http://localhost:5000/.create_collection/dsci551
```
For following curl command I will use -H "Authorization: Bearer {token}" to save space.
For creating index (index is used to support filtering):
```bash
curl -X POST -h "Authorization: Bearer {token}" http://localhost:5000/.create_index/dsci551?byValue=1
```
For creating listener (listener is used for real-time synchronization):
```bash
curl -X POST -h "Authorization: Bearer {token}" http://localhost:5000/.create_listener/dsci551
```

## CRUD
there are PUT, POST, GET, PATCH, DELETE methods implemented to support same functionalities covered by https://firebase.google.com/docs/reference/rest/database?hl=en
We provide some examples below
### PUT
```bash
curl -H "Authorization: Bearer {token} " -X PUT 'localhost:5000/dsci551.json' -d '{"yxj":{"info":{"address":"620 S Virgil ave"}}}'
```
### POST
```bash
curl -H "Authorization: Bearer {token} " -X POST 'localhost:5000/dsci551.json' -d '{"info":{"address":"620 S Virgil ave"}}'
```
You will get the unique id from the return message.
### GET
```bash
curl -H "Authorization: Bearer {token} " -X GET 'localhost:5000/dsci551/yxj.json'
```
For GET command with orderBy, you need to create related index first except for orderBy="$key". The following command create index for orderBy="$value" when the path is /dsci551
```bash
curl -X POST -h "Authorization: Bearer {token}" http://localhost:5000/.create_index/dsci551?byValue=1
```
### PATCH
```bash
curl -H "Authorization: Bearer {token} " -X PATCH 'localhost:5000/dsci551/yxj/info.json' -d '{"address":"621 S Virgil ave"}'
```
### DELETE
```bash
curl -H "Authorization: Bearer {token} " -X DELETE 'localhost:5000/dsci551/yxj.json'
```
To delete the collection:
```bash
curl -H "Authorization: Bearer {token} " -X DELETE 'localhost:5000/dsci551.json'
```
## Elaborations on .create_collection, .create_index and .create_listener
### .create_collection
The routing for .create_collection is like this '/.create_collection/<collection_name>', the name after .create_collection will be created.
### .create_index
#### Index is not Guaranteed
For .create_index, it is designed to support the orderBy functionality in GET method, however, due to the limit of backend MongoDB, an index will not be guaranteed used to speed up the filtering process.
By looking at how does orderBy works in GET, we can get an idea about what index should be created before filtering.
```bash
curl -H "Authorization: Bearer {token} " -X GET 'localhost:5000/dsci551/william/subjects/DSCI551/HW.json?orderBy="$value"'
```
The corresponding .create_index command is:
```bash
curl -H "Authorization: Bearer {token} " -X POST 'localhost:5000/.create_index/dsci551/subjects/DSCI551/HW?byValue=1'
```
You can also have GET command like:
```bash
curl -H "Authorization: Bearer {token} " -X GET 'localhost:5000/dsci551/william/subjects/DSCI551.json?orderBy="HW'
```
The corresponding index command is:
```bash
curl -H "Authorization: Bearer {token} " -X POST 'localhost:5000/.create_index/dsci551/subjects/DSCI551/HW'
```
The above two examples are for illustrations, it is unlikely that both make sense in the same collection.

#### .create_index Ambiguities 
If you use GET command with orderBy="$value", the path must be /path.json?orderBy="$value", and for .create_index, the path must be /path?byValue=1. There is no ambiguity.
However, for orderBy="subpath", there might be ambiguity in the index creating.
The following two GET command share the same .create_index command.
```bash
 curl -H "Authorization: Bearer {token} " -X GET 'localhost:5000/dsci551/william/subjects/DSCI551.json?orderBy="HW'
```
```bash
  curl -H "Authorization: Bearer {token} " -X GET 'localhost:5000/dsci551/william/subjects.json?orderBy="DSCI551/HW'
```
The .create_index command:
```bash
curl -H "Authorization: Bearer {token} " -X POST 'localhost:5000/.create_index/dsci551/subjects/DSCI551/HW'
```
However, there is no ambiguity for a specific collection. Thus, this should not be a problem in practice.
### .create_listener
Listener is a must for real-time synchronization based on socket, the path format is '/.create_listener/<collection_name>'.
Thus, the listener can be created only on the collection level, there is no way to create a listener specfic to a field.
## How to Setup the Socket to Receive Messages From Listeners
The client uses this emulated Firebase should use socket client, like the one provided by socketio package in python. Make the socket client connects to 'http://localhost:5000'. 



