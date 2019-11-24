#!/bin/bash

set -e
export PYTHONPATH=.
# This is needed for pytest
#venv/bin/pip3 install -e

/venv/bin/python ./invertedindex/api/app.py
