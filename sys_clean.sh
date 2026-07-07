#!/bin/bash

# ==============================================================================
# Script Name: sys_clean.sh
# Description: Automated Ubuntu System Storage Audit and Clean-up Utility.
#              Safely clears package caches, journal logs, old snaps, and pip.
# ==============================================================================

# Text Color Formatting
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}=======================================================${NC}"
echo -e "${CYAN}      STARTING ENTERPRISE STORAGE AUDIT & CLEANUP      ${NC}"
echo -e "${CYAN}=======================================================${NC}"

# 1. Capture Baseline Storage
echo -e "\n${YELLOW}[1/5] Checking Baseline Disk Space...${NC}"
df -h /

# 2. Audit Top Level System Directories (Requires sudo)
echo -e "\n${YELLOW}[2/5] Auditing Root Directory Space Usage...${NC}"
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Note: Running top-level directory audit requires sudo privileges.${NC}"
    sudo du -h --max-depth=1 / 2>/dev/null | sort -h | tail -n 12
else
    du -h --max-depth=1 / 2>/dev/null | sort -h | tail -n 12
fi

# 3. Purge Inactive/Disabled Snap Containers
echo -e "\n${YELLOW}[3/5] Cleaning Inactive Snap Container Revisions...${NC}"
if [ "$EUID" -ne 0 ]; then
    sudo snap set system refresh.retain=2
    
    # Custom loop to purge disabled snaps cleanly
    LANG=C snap list --all | awk '/disabled/{print $1, $3}' | while read snapname revision; do
        echo -e "${RED}Removing dead weight:${NC} $snapname (rev $revision)"
        sudo snap remove "$snapname" --revision="$revision" 2>/dev/null
    done
else
    snap set system refresh.retain=2
    LANG=C snap list --all | awk '/disabled/{print $1, $3}' | while read snapname revision; do
        echo -e "${RED}Removing dead weight:${NC} $snapname (rev $revision)"
        snap remove "$snapname" --revision="$revision" 2>/dev/null
    done
fi

# 4. Flush System Caches, Debris, and Vacuum Logs
echo -e "\n${YELLOW}[4/5] Sweeping System Caches & Log Vaults...${NC}"
if [ "$EUID" -ne 0 ]; then
    echo -e "${CYAN}Clearing pip cache...${NC}"
    rm -rf ~/.cache/pip
    echo -e "${CYAN}Clearing APT archives and orphans...${NC}"
    sudo apt-get autoremove --purge -y && sudo apt-get clean
    echo -e "${CYAN}Vacuuming systemd journals to 500M...${NC}"
    sudo journalctl --vacuum-size=500M
else
    rm -rf ~/.cache/pip
    apt-get autoremove --purge -y && apt-get clean
    journalctl --vacuum-size=500M
fi

# 5. Show Final Reclaimed Storage Output
echo -e "\n${YELLOW}[5/5] Finalizing Audited Drive State...${NC}"
df -h /

echo -e "\n${GREEN}=======================================================${NC}"
echo -e "${GREEN}             SYSTEM MAINTENANCE COMPLETE               ${NC}"
echo -e "${GREEN}=======================================================${NC}"
