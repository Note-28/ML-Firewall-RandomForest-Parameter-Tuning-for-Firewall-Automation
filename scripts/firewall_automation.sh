#!/bin/bash

FLAG_FILE="/etc/firewall_automation_enabled"

LOG_DIR="../logs" 
LOGFILE="$LOG_DIR/firewall_automation.log"

PYTHON_SCRIPT="../firewall_automation.py"

mkdir -p "$LOG_DIR"

run_firewall_automation() {
    if [ ! -f "$FLAG_FILE" ]; then
        echo "Firewall automation is disabled. To enable, create the flag file: $FLAG_FILE" >> "$LOGFILE"
        exit 0
    fi

    echo "Firewall automation started at $(date)" >> "$LOGFILE"

    echo "Executing: sudo python3 $PYTHON_SCRIPT" >> "$LOGFILE"
    sudo /usr/bin/python3 "$PYTHON_SCRIPT" >> "$LOGFILE" 2>&1

    if [ $? -ne 0 ]; then
        echo "Error: Firewall automation script failed" >> "$LOGFILE"
        exit 1
    fi

    echo "Firewall automation completed at $(date)" >> "$LOGFILE"
}

case "$1" in
    enable)
        echo "Running the Python script to verify before enabling firewall automation." >> "$LOGFILE"
        sudo /usr/bin/python3 "$PYTHON_SCRIPT" >> "$LOGFILE" 2>&1
        
        if [ $? -ne 0 ]; then
            echo "Error: Firewall automation script failed. Enable aborted." >> "$LOGFILE"
            echo "Error: Firewall automation script failed. Enable aborted."
            exit 1
        fi

        sudo touch "$FLAG_FILE"
        echo "Firewall automation enabled at $(date)" >> "$LOGFILE"
        echo "Firewall automation enabled."
        ;;
    disable)
        sudo rm "$FLAG_FILE"
        echo "Firewall automation disabled at $(date)" >> "$LOGFILE"
        echo "Firewall automation disabled."
        ;;
    status)
        if [ -f "$FLAG_FILE" ]; then
            echo "Firewall automation is enabled."
            echo "Checked status at $(date): enabled" >> "$LOGFILE"
        else
            echo "Firewall automation is disabled."
            echo "Checked status at $(date): disabled" >> "$LOGFILE"
        fi
        ;;
    run)
        run_firewall_automation
        ;;
    *)
        echo "Usage: $0 {enable|disable|status|run}"
        exit 1
        ;;
esac
