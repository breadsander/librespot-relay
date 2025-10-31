#!/usr/bin/env python3
import os
import json

event_data = {
    event = os.environ.get("PLAYER_EVENT")
}

FIFO = "/tmp/spotify_events.fifo"
with open(FIFO, "w") as f:
    f.write(json.dumps(event_data) + "\n")
