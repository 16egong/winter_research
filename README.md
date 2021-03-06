# winter_research
Chat UI for research project

## Requirements
- docker
- docker compose
- mt-server.tar

## Installation
```bash
git clone <repository>
cd winter_research
```

## Setup
- Open config.py
- For each trial configure the trial number and the type i.e.
```bash
TRIAL_NUM = 2
TYPE = "control"
```
Switch to the **combined** branch to run control, keys, no_keys trials
```bash
git status
```
Make sure there are no changes to commit, if there are, either remove them or commit them
```bash
git checkout combined
```

## Docker
If this is the first time running or there are changes to the docker file, or yaml file, run the command below
```bash
docker-compose build
```

Use the command below to start the machine translation server container and the flask server container together
```bash
docker-compose up
```

(Optional) Use the command below to stop containers and remove containers, networks, volumes, and images created by up
```bash
docker-compose down
```

(Optional) Check the permissions of the database and potentially change them 
```bash
chmod 764 trial_1_0.db
```



### Local
From your local computer, you can access the the site

- user 1: http://0.0.0.0:5000/1 
- user 2: http://0.0.0.0:5000/2
- user 3: http://0.0.0.0:5000/3
- user 4: http://0.0.0.0:5000/4
- Observe as user 1: http://0.0.0.0:5000/12
- Observe as user 3: http://0.0.0.0:5000/34


### Amazon EC2 Instance
From your terminal where the hci_research.pem key is
```bash
ssh -i <permissions_file.pem> ec2-user@ec2-34-236-57-52.compute-1.amazonaws.com
```

- user 1: http://34.236.57.52:5000/1 
- user 2: http://34.236.57.52:5000/2
- user 3: http://34.236.57.52:5000/3
- user 4: http://34.236.57.52:5000/4
- Observe as user 1: http://34.236.57.52:5000/12
- Observe as user 3: http://34.236.57.52:5000/34

## Collecting Data
At the file path of hci_research.pem secure copy over the data
```bash
scp -i "hci_research.pem" ec2-user@ec2-34-236-57-52.compute-1.amazonaws.com:~/winter_research/data/trial_1_control.db .
```
In terminal
```bash
cd /data
>sqlite3 trial_1_control.db
sqlite> .tables
```
You should see posts, notes, record as the tables
```bash
sqlite> .headers on
sqlite> .mode csv
sqlite> .output trial_{trial_num}_{trial_type}_posts.csv
sqlite> SELECT * FROM posts;
sqlite> .quit
```

```bash
cd /data
>sqlite3 trial_1_control.db
sqlite> .headers on
sqlite> .mode csv
sqlite> .output trial_{trial_num}_{trial_type}_notes_.csv
sqlite> SELECT * FROM notes;
sqlite> .quit
```

```bash
cd /data
>sqlite3 trial_1_control.db
sqlite> .headers on
sqlite> .mode csv
sqlite> .output trial_{trial_num}_{trial_type}_record_.csv
sqlite> SELECT * FROM record;
sqlite> .quit
```

You can open this in google docs without any encoding issues.
Open split_csv.ipynb
Run cells
