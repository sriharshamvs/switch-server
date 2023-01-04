# Project Switch - Server

__Server__ is the backend for the __Project Switch__. The server publishes RESTful APIs which are written using __flask__ and communication with the hardware is done using __MQTT__.

## Getting Started

This server is currently deployed on __raspberrypi 3__. It can also be deployed on any Debian based Linux distribution.

- Clone this repo on to your local machine

```bash
git clone git@gitlab.com:project-switch/server.git
```

### Environment

Things you need to deploy this application

- Raspbian or Debian GNU/Linux

- Python 3.7

- Mosquitto Broker

- Virtualenv

### Installing

#### MQTT Broker

- Install the Mosquitto Broker

```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
```

- Make Mosquitto auto start on boot up enter

```bash
sudo systemctl enable mosquitto.service
```

#### Database

- Install SQLite3 db

```bash
sudo apt install sqlite3
```

#### Python Environment

- Go to the project root directory and create a Virtual environment to run this application as `switch_env`

```bash
cd server
python3 -m venv switch_env
```

- Activate the python environment

```bash
source switch_env/bin/activate
```

- Install python packages for the backend

```bash
pip3 install -r requirements.txt
```

- To create a DB file, update data in `users.csv` and `topics.csv` in __db_csv__ and run the `db_init.py` file

```bash
python3 db_init.py
```

- Now run the server

```bash
python3 wsgi.py
```

The server will be running on `http://localhost:5000/`

- To deactivate the environment just type

```bash
deactivate
```

## Deployment

- Run this Application using __gunicon__

```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

- Now create a service file `switch.service` to run this application on restart
- Create it in the systemd directory

```bash
sudo nano /etc/systemd/system/switch.service 
```
- Paste the below content and change the path accordingly.
```bash
[Unit]
Description=Gunicorn instance to serve Project Switch
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/project-switch/switch-server # Update Your PATH
Environment="PATH=/home/pi/project-switch/switch-server/switch_env/bin" # Update Your PATH
ExecStart=/home/pi/project-switch/switch-server/switch_env/bin/gunicorn --workers 3 --bind unix:projectswitch.sock -m 007 wsgi:app # Update Your PATH

[Install]
WantedBy=multi-user.target
```

- Now we need to reload the daemon.

```bash
sudo systemctl daemon-reload
```

- Enable service so that it doesn’t get disabled if the server restarts.

```bash
sudo systemctl enable switch.service
```

- Now start the service.

```bash
sudo systemctl start switch.service
```

## Contributing

Please read [CONTRIBUTING](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Changelog

Check [CHANGELOG](CHANGELOG.md) to get the version details.

## License

This project is licensed under the GNU AGPLv3 License - see the [LICENSE](LICENSE) file for details
