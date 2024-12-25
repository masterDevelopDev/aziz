#!/bin/bash
gunicorn --bind 0.0.0.0:$PORT back.app:app