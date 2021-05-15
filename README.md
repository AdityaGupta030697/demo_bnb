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

### Functionalities:

#### Intro:
![](src/demo_images/intro.JPG?raw=true)

#### Host:
1. Registration
![Registration](src/demo_images/host_registration.JPG?raw=true "Registration")
2. Login
![Login](src/demo_images/host_login.JPG?raw=true "Login")
3. Room Registration
![Room Registration](src/demo_images/host_room_registration.JPG?raw=true "Room Registration")
4. Update Room Availability
![Room Availability](src/demo_images/host_update_room_availability.JPG?raw=true "Update Room Availability")

#### Guest:
1. Registration
![Registration](src/demo_images/guest_registration.JPG?raw=true "Registration")
2. Room booking
![Room Booking](src/demo_images/guest_room_booking.JPG?raw=true "Room Booking")
3. View guests
![View guests](src/demo_images/guest_view.JPG?raw=true "View guests")
4. View guest booking
![View guest booking](src/demo_images/guest_view_bookings.JPG?raw=true "View guest booking")

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
