# batcave-api
A FastAPI based API for using a raspberry pi to control a garage door opener

Running locally for development/testing
* A modern version of Python
* A virtual environment created per the fastapi docs at https://fastapi.tiangolo.com/virtual-environments/
* Leave the `RPi.GPIO` code commented out in `app/connection_manager.py` for running
  locally, but this will need to be reverted on the pi.
* Leave rpi-lgpio commented out in requirements.txt when installing dependencies in the virtual
  environment locally, but this will need to be uncommented on the pi

In this example, the user on the pi is `batman`. Replace `batman` with whatever user you want to use on the pi.
Replace {pi_ip} with the IP address of you pi on your local network.

On the pi: 
```
cd srv
sudo mkdir batcave-api
sudo chmod 774 batcave-api
sudo chown www-data:batman batcave-api
sudo mkdir batcave-api/batvenv
sudo chown www-data:batman batcave-api/batvenv
sudo chmod 774 batcave-api/batvenv
python -m venv batcave-api/batvenv
```
Not sure by you may need to make the group for `/srv` be `www-data` and give the group write access as well.

Back here in your local repo, remove any `__pycache__` directories created by running locally,
and then copy the app code to the pi:
```
find . -name "__pycache__" -type d -exec rm -rf {} \;
scp -r app requirements.txt batman@{pi_ip}:/srv/batcave-api
scp pi-plumbing/batcave.service batman@{pi_ip}:
```

Back on the pi at `/home/batman`
```
cd /srv/batcave-api
sudo chown -R www-data:batman *
sudo chmod -R 774 batvenv
source batvenv/bin/activate
``` 
Create a `.env` file in the `/srv/batcave-api` directory and add line `APP_MODE=production`
This prevents the `/docs` endpoint from being advertised on your "production" batcave server.
See the other required fields in `.env.example` and enter appropriate values form your auth0 dashboard
(see Applications -> Applications and Applications -> APIs).

Now inside the venv at `/srv/batcave-api`, before installing the requirements from the
`requirements.txt`, you need to remember to edit the last line to uncomment the dependency for `rpi-lgpio`.
```
(batvenv): pip install --upgrade pip
(batvenv): pip install -r ./requirements.txt
```
www-data is the user for running the fastAPI service, but www-data doesn't have the 
gpio group, which is required to access gpio libs/functionality. Add it with 
```
sudo usermod -a -G gpio www-data
```

Test to make sure the app will start on the pi
```
(batvenv): fastapi run
```
Then on another machine
```
curl http://{pi_ip}:8000/api
```
You should see the response `["Stu","hello"]`

Now you can `ctl-c` to shut fastapi down and `deactivate` to stop the venv.
Now is the time to uncomment the `RPi.GPIO` related code that is commented out in `app/connection_manager.py`.
This will be necessary for the pi control the relay which will trigger the opener.

Next up get the app running as a service. In a previous step the batcave.service
file was copied to the home directory on the pi. From there:
```
sudo mv batcave.service /etc/systemd/system
sudo chown root:root /etc/systemd/system/batcave.service 
sudo chmod 644 /etc/systemd/system/batcave.service
sudo systemctl daemon-reload
sudo systemctl start batcave.service
sudo systemctl status batcave.service
sudo systemctl enable batcave.service
```
Verify the app once again with curl from a different machine.
```
curl http://{pi_ip}:8000/api
```

# TODO's
* logging in general
* production logging on the pi including rolling
* Wiring diagram for pi/relay/garage door.
* Info about the front end repo
  * running locally `source venv/bin/activate` and `fastapi dev`

## Installing CADDY on the pi 
Using CADDY as a reverse proxy for fastAPI on the pi for tls. See CADDY section of front end repo
`batcave2`.
