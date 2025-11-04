#!/usr/bin/env python3

import os
import socket
import json
import sys

TCP_HOST = "127.0.0.1"
TCP_PORT = 24880

# What we care about
# session_disconnected
# track_changed
# 

# List of PLAYER_EVENTs that have a TRACK_ID
TRACK_EVENTS = {
    "track_changed",
    "stopped",
    "playing",
    "paused",
    "loading",
    "preloading",
    "preload_next",
    "end_of_track",
    "unavailable",
    "seeked",
    "position_correction",
}

# Additional environment variables to include if they exist
OPTIONAL_FIELDS = [
    "OLD_TRACK_ID",
    "NEW_TRACK_ID",
    "POSITION_MS",
    "DURATION_MS",
    "IS_EXPLICIT",
    "VOLUME",
    "COVERS",
    "URI",
    "NAME",
    "ITEM_TYPE",
    "ARTISTS",
    "ALBUM_ARTISTS",
    "ALBUM",
    "POPULARITY",
    "NUMBER",
    "DISC_NUMBER",
    "DESCRIPTION",
    "PUBLISH_TIME",
    "SHOW_NAME",
]

def main():
    # Determine which PLAYER_EVENT this is
    event_type = os.getenv("PLAYER_EVENT", "unknown").lower()
    payload = {"event": event_type}

    # Include TRACK_ID if present
    if event_type in TRACK_EVENTS:
        track_id = os.getenv("TRACK_ID")
        if track_id:
            payload["track_id"] = track_id

    # Include other optional fields if they exist
    for key in OPTIONAL_FIELDS:
        value = os.getenv(key)
        if value:
            # Special handling for COVERS: split newline-separated URLs into a list
            if key == "COVERS":
                payload["covers"] = value.strip().split("\n")
            # Special handling for fields with multiple values separated by newline
            elif key in {"LANGUAGE", "ARTISTS", "ALBUM_ARTISTS"}:
                payload[key.lower()] = value.strip().split("\n")
            else:
                payload[key.lower()] = value
    
    try:
        with socket.create_connection((TCP_HOST, TCP_PORT)) as sock:
            json_line = json.dumps(payload) + "\n"
            sock.sendall(json_line.encode("utf-8"))
            print(f"Sent JSON: {payload}")
    except Exception as e:
        print(f"Failed to send JSON: {e}")

if __name__ == "__main__":
    main()
