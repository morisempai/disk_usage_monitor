# Simple monitor implementation
this project implements simple monitor that displays some gauge metric on a led matrix (4x4)

Project consists of:
  - C microcontroller code that reads messages from serial port and lights leds 
  - python code that calculates what pixels to light

## Interaction protocol

first byte contains number of led to light, then folowing 5 bytes for each led to configure x, y coords, and rgb colours.

# Run python script

to run python script on linux:
```bash
git clone {repo} && cd {repo}
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python monitor/main.py --path="{something you want to monitor}"
```