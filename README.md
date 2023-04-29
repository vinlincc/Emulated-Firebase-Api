# WEB APP: DSCI551 Forum

## Setup

**1. Python Virtual Environment**

Part 1 is assumed to run successfully in your computer before running part 2 as some parts of part 2 are based on part 1. Besides, all the command is run on the MacOS, if your operation system is Windows, pleaase download git bash to run the following command!

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

**2. Start up the server**
change your working directory into 1
```bash
cd 1
python main.py  #CRUD server starts up, make sure 5066 port is not occupied
```
change your working directory into 2
```bash
cd ../2
python app.py  #WEB APP server starts up, make sure 5000 port is not occupied
```

**3. Use DSCI551-Forum**
open your browser and open the following url:
```bash
http://localhost:5000
```

**4. About synchronize function**

What you write in the terminal will immediately show up in interface, which is our synchronize function.
For example, you can use terminal or Mongodb Compass to add a new post and this post will immediately appear on the web without refreshing the browser.
