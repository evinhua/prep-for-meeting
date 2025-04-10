#!/bin/bash

# Start the Flask server
cd $(dirname "$0")/api
python server.py
