#!/bin/bash
pushd ./backend
source venv/bin/activate
exec python query_interface_server.py