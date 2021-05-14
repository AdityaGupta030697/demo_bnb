```text
_ .-') _    ('-. _   .-')                     .-. .-')      .-') _.-. .-')   
( (  OO) ) _(  OO( '.( OO )_                   \  ( OO )    ( OO ) \  ( OO )  
 \     .'_(,------,--.   ,--..-'),-----.        ;-----.\,--./ ,--,' ;-----.\  
 ,`'--..._)|  .---|   `.'   ( OO'  .-.  '       | .-.  ||   \ |  |\ | .-.  |  
 |  |  \  '|  |   |         /   |  | |  |       | '-' /_|    \|  | )| '-' /_) 
 |  |   ' (|  '--.|  |'.'|  \_) |  |\|  |       | .-. `.|  .     |/ | .-. `.  
 |  |   / :|  .--'|  |   |  | \ |  | |  |       | |  \  |  |\    |  | |  \  | 
 |  '--'  /|  `---|  |   |  |  `'  '-'  '       | '--'  |  | \   |  | '--'  / 
 `-------' `------`--'   `--'    `-----'        `------'`--'  `--'  `------'  
```

# demo_bnb
Application similar to Airbnb

#### Functionalities:
- Create Account 
- Login
- Add/Search Rooms 
- Update/Check room availability

To setup MongoDB using docker:
```console
# 1. Install docker

# 2. Search for mongo docker image
aditya@desktop:~$ docker search mongodb

# 3. Pull mongo image
aditya@desktop:~$ docker pull mongo

# 4. Run the image in detach mode
# map the container port 27017 to 27017 of host
# Mongodb listens on 27017 by default
aditya@desktop:~$ docker run -d -p 27017:27017 mongo

# 5. Connect to the container
# e4818988049c is the container id
aditya@desktop:~$ docker exec -it e4818988049c /bin/bash

# 6. Connect to MongoDB
root@e4818988049c:/# mongo
>
```
