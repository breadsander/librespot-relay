#!/bin/bash
set -e

SERVICE_NAME="librespot-relay.service"
SERVICE_USER="librespotrelay"
APP_DIR="/opt/librespot-relay"
LOG_FILE="/var/log/librespot-relay.log"
SYSTEMD_PATH="/etc/systemd/system/$SERVICE_NAME"

echo "Stopping and disabling service..."
if systemctl is-active --quiet "$SERVICE_NAME"; then
    sudo systemctl stop "$SERVICE_NAME"
fi

if systemctl is-enabled --quiet "$SERVICE_NAME"; then
    sudo systemctl disable "$SERVICE_NAME"
fi

echo "Removing systemd service file..."
if [ -f "$SYSTEMD_PATH" ]; then
    sudo rm -f "$SYSTEMD_PATH"
    sudo systemctl daemon-reload
fi

echo "Removing application files..."
if [ -d "$APP_DIR" ]; then
    sudo rm -rf "$APP_DIR"
fi

echo "Removing log file..."
if [ -f "$LOG_FILE" ]; then
    sudo rm -f "$LOG_FILE"
fi

# Optional: remove the dedicated service user
if id -u "$SERVICE_USER" >/dev/null 2>&1; then
    echo "Removing service user $SERVICE_USER..."
    sudo userdel "$SERVICE_USER" || true
fi

echo "Uninstallation complete."
