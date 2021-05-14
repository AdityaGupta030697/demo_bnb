# demo_bnb
Application similar to Airbnb

To setup MongoDB using docker:
```console
# 1. Install docker

# 2. Search for mongo docker image
aditya@desktop:~$ docker search mongodb

# 3. Pull mongo image
aditya@desktop:~$ docker pull mongo

# 4. Run the image in detach mode
# map the container's port 27017 to host's 27017
# Mongodb listens on 27017 by default
aditya@desktop:~$ docker run -d -p 27017:27017 mongo

# 5. Connect to the container
# e4818988049c is the container id
aditya@desktop:~$ docker exec -it e4818988049c /bin/bash

# 6. Connect to MongoDB
root@e4818988049c:/# mongo
>
```
