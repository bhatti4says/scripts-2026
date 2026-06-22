#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "=== Starting Fresh Ubuntu Post-Install Setup ==="

# 1. Update package lists
echo "--> Updating package repositories..."
sudo apt update -y

# 2. Install requested tools (OpenSSH, Ping, Tracepath, Net-tools)
echo "--> Installing OpenSSH Server and network utilities..."
sudo apt install -y openssh-server iputils-ping iputils-tracepath net-tools

# 3. Configure Basic Security Policy & SSH Hardening
echo "--> Hardening SSH Configuration..."
SSH_CONFIG="/etc/ssh/sshd_config"

# Create a backup of the original SSH config
sudo cp $SSH_CONFIG "${SSH_CONFIG}.bak"

# Apply secure settings: Disable root password login, enforce public keys, disable password auth
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' $SSH_CONFIG
sudo sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/g' $SSH_CONFIG
sudo sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/g' $SSH_CONFIG
sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin prohibit-password/g' $SSH_CONFIG
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin prohibit-password/g' $SSH_CONFIG

# Restart SSH service to apply changes
sudo systemctl restart ssh

# 4. Configure Firewall (UFW)
echo "--> Configuring Uncomplicated Firewall (UFW)..."
# Set default policies to deny incoming, allow outgoing
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH connections
sudo ufw allow ssh

# Enable the firewall (echo "y" passes the confirmation prompt automatically)
echo "y" | sudo ufw enable

echo "=== Setup Completed Successfully! ==="
echo "CRITICAL: Ensure you add your Mac's SSH public key (~/.ssh/id_rsa.pub) to ~/.ssh/authorized_keys on this machine before closing your terminal, or you will be locked out!"
