# WEB APP: DSCI551 Forum

Setup

1. Python Virtual Environment
Python is assumed to be installed before this procedure.

Open your terminal, input command:

python -m venv venv
And run command:

source venv/bin/activate
Run pip install related packages:

pip install -r requirements.txt
2. Secret Key
A secret key is necessary in this project. Input command:

export JWT_SECRET_KEY="6cfb8684b95028909c82dcea7244cb04f009f0a07dde210f71e00b97f663a144"
Or use your own secret key.

3. MongoDB
MongoDB is assumed to be installed, and MongoDB replica set should be properly set up. In the following instructions, we set up a MongoDB replica set locally.

a. Kill the possible local mongo process that uses the port 27017, please use the PID that runs the process
sudo lsof -i:27017
sudo kill PID
b. Create resources directories for replica set (please use your own path)
sudo mkdir -p /your/path/to/rs1
sudo mkdir -p /your/path/to/rs2
sudo mkdir -p /your/path/to/rs3
sudo chmod 755 /your/path/to/rs*
c. Start 3 mongo processes
The terminal tool screen is assumed to be installed before this procedure.

screen -S mongodb1
sudo mongod --port 27017 --dbpath /your/path/to/rs1 --replSet myReplicaSet --bind_ip localhost
ctrl-a d (leave the screen session)
screen -S mongodb2
sudo mongod --port 27018 --dbpath /your/path/to/rs2 --replSet myReplicaSet --bind_ip localhost
ctrl-a d (leave the screen session)
screen -S mongodb3
sudo mongod --port 27019 --dbpath /your/path/to/rs3 --replSet myReplicaSet --bind_ip localhost
ctrl-a d (leave the screen session)
d. Start replica set in mongosh
mongosh --port 27017
Inside the mongosh:

rs.initiate({ _id: "myReplicaSet", members: [ { _id: 0, host: "localhost:27017" }] })
rs.add("localhost:27018")
rs.add("localhost:27019")
You can check the health status for each port with rs.status().
