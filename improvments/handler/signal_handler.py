import json
import sys


def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


def signal_handler(sig, frame, data=None):
    if data:
        save_data(data)
    sys.exit(0)
