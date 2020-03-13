# winter_research
Chat UI for research project

## Installation
```bash
git clone <repository>
cd winter_research
```
### Docker
```bash
cd docker
docker build . --tag winter
cd ..
```
Check the permissions of the database and potentially change them 
```bash
chmod 764 trial_1_0.db
```
Start the docker container
```bash
./start_script <container_name> <port_number> (i.e. ./start_script research 1111)
```
### Requirements.txt
```bash
cd docker 
python3 -m pip install -r requirements.txt
cd ..
```
## Setup
- Open config.py
- For each trial configure the trial number and the type i.e.
```bash
TRIAL_NUM = 2
TYPE = "control" #switch between control, no_keys, or keys
```
## Start up server
### Locally
In the terminal
```bash
python -m winter
```
- user 1: http://0.0.0.0/1 
- user 2: http://0.0.0.0/2
- user 3: http://0.0.0.0/3
- user 4: http://0.0.0.0/4
### Amazon EC2 Instance
From your terminal where the hci_research.pem key is
```bash
ssh -i "hci_research.pem" ec2-user@ec2-34-236-57-52.compute-1.amazonaws.com
```
Start the docker container
```bash
./start_script <container_name> <port_number> (i.e. ./start_script research 1111)
```
Refer to Setup
```bash
python -m winter
```
- user 1: http://34.236.57.52/1 
- user 2: http://34.236.57.52/2
- user 3: http://34.236.57.52/3
- user 4: http://34.236.57.52/4

## Collecting Data
In terminal
```bash
cd /data
>sqlite3 trial_1_control.db
sqlite> .tables
```
You should see posts and notes as the two tables
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
Open split_csv.ipynb
Run cells
