#!/bin/bash
set -e   # Stop on first error

# 1. Create a virtual environment in ./venv
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Upgrade pip (optional but recommended)
pip install --upgrade pip

# 4. Install dependencies from requirements.txt
pip install -r requirements.txt
