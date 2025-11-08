#!/bin/bash
set -e

# ----- CONFIGURATION -----
SERVICE_NAME="librespot-relay.service"
SERVICE_USER="librespotrelay"
APP_DIR="/opt/librespot-relay"
VENV_DIR="$APP_DIR/venv"
LOG_FILE="/var/log/librespot-relay.log"
SERVICE_FILE="$SERVICE_NAME"

# ----- Create dedicated service user -----
if ! id -u "$SERVICE_USER" >/dev/null 2>&1; then
    echo "Creating service user $SERVICE_USER..."
    sudo useradd --system --no-create-home --shell /usr/sbin/nologin "$SERVICE_USER"
fi

# ----- 2️ Copy application files -----
echo "Copying application files to $APP_DIR..."
sudo mkdir -p "$APP_DIR"
sudo cp -r ./* "$APP_DIR"
sudo chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"

# ----- 3️ Create virtual environment -----
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    sudo -u "$SERVICE_USER" python3 -m venv "$VENV_DIR"
fi

# Activate venv and install dependencies
echo "Installing dependencies..."
sudo -u "$SERVICE_USER" "$VENV_DIR/bin/pip" install --upgrade pip
sudo -u "$SERVICE_USER" "$VENV_DIR/bin/pip" install -r "$APP_DIR/requirements.txt"

# ----- 4️ Setup log file -----
sudo touch "$LOG_FILE"
sudo chown "$SERVICE_USER:$SERVICE_USER" "$LOG_FILE"

# ----- 5️ Install systemd service -----
echo "Installing systemd service..."
sudo cp "$SERVICE_FILE" "/etc/systemd/system/$SERVICE_NAME"
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo "$SERVICE_NAME installed and running."
