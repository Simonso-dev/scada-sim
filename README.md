# scada-sim
A SCADA simulation using SCADA-LTS and pymodbus to demonstrate attacks.

## Disclaimer
This repository is provided **strictly for educational and research purposes**. The examples and demonstrations of attacks are intended to help developers, security professionals, and students understand vulnerabilities and improve defensive measures.

**Do not use this code or information for illegal, unethical, or unauthorized activities.** The author(s) assume no responsibility for misuse. By using this repository, you agree to comply with all applicable laws and regulations.

## Before you get started
This system is made to be run on linux and has been specifically tested on Ubuntu 24.04.1

Make sure you have the following:
- [Docker engine](https://docs.docker.com/engine/install/)
- Python 3.12.3 (should come with Ubuntu 24.04.1)
- [Python-venv](https://askubuntu.com/questions/1328392/how-to-activate-a-virtual-environment-in-ubuntu)
- [Hydra](https://github.com/vanhauser-thc/thc-hydra)

For the SCADA solution we are using the open-source tool [SCADA-LTS](https://github.com/SCADA-LTS/Scada-LTS) and the container configuration. If you want to install or set it up the scada-lts yourself read more about it [here](https://github.com/SCADA-LTS/Scada-LTS/wiki).
## Installation
Clone this repository: [scada-sim](https://github.com/Simonso-dev/scada-sim.git)

Then change directory into the project.

Run this command to install SCADA-LTS.
```Shell
sudo docker compose up
```

> Note!
> In the tutorial for how to set up scada-lts they use the `docker-compose up` command but in newer versions of docker engine this is built in.

After awhile when it seems to be done, then stop it and use the start script. Be vary when running scripts by others, so check before running.

Change the scripts to be runnable by bash.
```Shell
chmod +x ./start_scada_sim.sh ./stop_scada_sim.sh
```

Now we need to install the python virtual environment (venv). So change into the "plc" directory and create this venv.
```Shell
python3 -m venv plc-venv
```

After the venv is up then you have to activate it.
```Shell
source plc-venv/bin/activate
```

Then install the requirments.
```Shell
pip install -r requirements.txt
```

Now open a new terminal tab or window and run this command to start scada-lts. This script will first start the scada-lts database then the web frontend. If you do this manually start the database container first, then web frontend due to a bug where if the web frontend is started first it might not connect properly to the database. 
```Shell
sudo ./start_scada_sim.sh
```

Once scada-lts is up and running go to localhost:8080/Scada-LTS/, then log in with username admin and password admin. Now press the document icon with brackets to import a project or go to this url http://localhost:8080/Scada-LTS/emport.shtm. Here press the choose file button and upload a zip file that came with the repository called "SCADA-LTSmodbus.zip". Now the configuration for the server should be up. One thing that might happen is that you will need to change the ip address, this can be changed by going to this url http://localhost:8080/Scada-LTS/data_sources.shtm and pressing the icon that is a database with a pencil. On the editing page set the ip address to that of the eth0 (done by running "ip addr show" in the terminal) and save by pressing the floppy disk icon.


After this go back to the tab with python and run this command to start the modbus server/plc device. Might have to change this ip address to eth0 aswell.
```Shell
python modbus_fan_control_v2-2.py
```

Then everything should be up and running.

# Example attacks
## Direct unauthorized access to modbus server/PLC device
This first attack is very easy it is just a modbus client that connects to a modbus server/PLC device. Then change values on the server that controls wheter a fan or pump is on or off. Specifaclly this python script turns the fan on in our small scada sim. Run this command to turn on the fan.
```Shell
python atk_fan_direct.py
```

## Password brute force with hydra
This is also another easy attack that is dependent on how strong the password is. Here we use hydra to feed Scada-LTS login page the admin username and try many passwords from the infamous rockyou.txt. You can get the rockyou file [here](https://github.com/dw0rsec/rockyou.txt).
```Shell
hydra -l admin -P rockyou.txt localhost http-post-form "/Scada-LTS/login.htm:username=^USER^&password=^PASS^:Bad credentials" -s 8080
```
