apt-get update && apt-get install -y chromium chromium-driver
#!/bin/bash
# start.sh

set -e

echo "Starting app..."

# Run Python script
python3 main.py
