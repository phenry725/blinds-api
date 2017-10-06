# Home Automation API

## Prereqs
Assuming a freshly imaged RPi w/ Raspbian version higher than Jessie
* [Install Pip](https://www.raspberrypi.org/documentation/linux/software/python.md)
* [Install Flask](http://flask.pocoo.org/docs/0.12/installation/)
## General Setup
* Load api.py into /var/local/api.py on the Raspberry Pi  
`sudo mv $PWD/api.py /var/local/api.py`
* Create the service for the api then paste the api.service contents  
`sudo vim /etc/systemd/system/api.service`
* Reload Services  
`sudo systemctl reload-daemon`
* Start API Service  
`sudo systemctl enable api.serivce`
