#!/bin/bash

# Run this from the directory in which `legal` was cloned.

find . -mindepth 1 -maxdepth 1 -type d ! \( -name "jwt" -o -name "logs" \) -exec rm -rf {} +
find . -maxdepth 1 -type f ! -name "wsgi.py" -exec rm -rf {} +
