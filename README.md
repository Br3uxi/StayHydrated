# StayHydrated [![Discord Hackweek](https://img.shields.io/badge/Discord%20Hackweek-2019-blue.svg)](https://blog.discordapp.com/discord-community-hack-week-build-and-create-alongside-us-6b2a7b7bba33) [![Language Python](https://img.shields.io/badge/Language-Python-green.svg)](https://www.python.org) [![Wumpus](https://img.shields.io/badge/Wumpus-Awesome-92a6ed.svg)](https://www.python.org)
A little discord bot, written for the [Discord Hack Week](https://discord.gg/hackweek) to help you stay hydrated :D
The idea came to me while brainstorming on a topic during a big heatwave in germany.

## Install
(Instructions for Linux)
1. Download and install Python >= 3.6 and Git
2. Clone this Repo
3. Create a new Virtual Environment (OPTIONAL) 
```bash
python3 -m venv venv/
```
4. Activate the Virtual Environment (OPTIONAL)
```bash
source venv/bin/activate
```
5. Install the requirements
```bash
pip install -r requirements.txt
```
6. Create a Environment Variable called "discord_token" and store your Bot Token from the [Discord Developer Platform](http://discordapp.com/developers/applications/) in it
7. Run the Main File
```bash
python3 stay_hydrated.py
```
(to leave the Virtual Env, just type "deactivate")

### [Supervisor](http://supervisord.org)
To run this bot with Supervisor, just copy the sample Config to /etc/supervisor/conf.d/StayHydrated.conf and change the values to your needs
```conf
[program:StayHydrated]
user = <you>
directory=<whereever>
command=<...>/StayHydrated/venv/bin/python3 stay_hydrated.py
autostart=true
autorestart=true
stderr_logfile = <...>/StayHydrated/log/err.log
stdout_logfile = <...>/StayHydrated/log/out.log
```
Then run
```bash
(sudo) supervisorctl reread
(sudo) supervisorctl add StayHydrated
(sudo) supervisorctl start StayHydrated
```
Now your Bot should stay running!
