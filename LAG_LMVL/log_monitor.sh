#!/bin/bash

# OpenVPN Log Monitor - LAG-LMV (Log Monitoring Viewer)

# This script monitors OpenVPN and system logs for anomalies and security issues.
# It also performs a checklist verification for specified applications.
# All generated logs and reports are archived.

# --- Configuration ---
# Define log file paths
OPENVPN_LOG="/var/log/openvpn.log"
SYS_LOG="/var/log/syslog" # or /var/log/messages, depending on your Linux distribution

# Base directory for script-generated logs and status files
# Ensure this directory exists and the script has write permissions
LOG_BASE_DIR="/var/log/monitoring_script"

# Directory for backing up all generated logs and reports
# This should be a path where the current user has write permissions
BACKUP_BASE_DIR="$HOME/Documents/monitoring_logs_backup"

# --- CHECKLIST CONFIGURATION ---
# Base directory where application health check files (.txt) are expected to be.
# For example: ~/Checklist/WebApp1.txt
CHECKLIST_BASE_DIR="$HOME/Checklist"

# List of expected application names for which a .txt file should exist in CHECKLIST_BASE_DIR.
# If a file is missing, it will be flagged as an error in the report.
EXPECTED_CHECKLIST_APPS=(
    "WebApp1"
    "DatabaseService"
    "VPNClient"
    "FirewallD"
    "SSHServer"
    "WebserverNginx"
    "PaymentGatewayService"
    "CloudSyncDaemon"
    "CameraService"
    "PasswordManagerService"
    "NotebookSyncAgent"
    "SocialMediaBridge"
    "AIMonitoring"
    # Add more APP names here as needed
)
# --- END CHECKLIST CONFIGURATION ---

# --- Output File Definitions (Relative to LOG_BASE_DIR) ---
SCRIPT_RUN_HISTORY_LOG="$LOG_BASE_DIR/script_run_history.log"
CURRENT_RUN_DETAILS_LOG="$LOG_BASE_DIR/current_run_details.log"
LATEST_INTRUSION_LOG_PATH_FILE="$LOG_BASE_DIR/latest_intrusion_log_path.txt"
LATEST_CHECKLIST_REPORT_PATH_FILE="$LOG_BASE_DIR/latest_checklist_report_path.txt"
STATUS_FILE="$LOG_BASE_DIR/status.txt" # Contains 'ok' or 'errors' for GUI

# --- Functions ---

# Function to ensure log directories exist
ensure_dirs() {
    mkdir -p "$LOG_BASE_DIR"
    mkdir -p "$BACKUP_BASE_DIR"
    mkdir -p "$CHECKLIST_BASE_DIR"
}

# Function to get a formatted timestamp
get_timestamp() {
    date +"%Y-%m-%d_%H%M%S"
}

# Function to log script execution
log_script_history() {
    local timestamp=$(get_timestamp)
    echo "$timestamp: Script started." >> "$SCRIPT_RUN_HISTORY_LOG"
}

# Function to check for OpenVPN anomalies
check_openvpn_logs() {
    local log_file="$1"
    local timestamp=$(get_timestamp)
    local output_file="$LOG_BASE_DIR/openvpn_anomalies_$timestamp.log"
    echo "--- OpenVPN Log Analysis Report ($timestamp) ---" > "$output_file"

    if [ -f "$log_file" ]; then
        # Failed authentication attempts
        grep -E "AUTH_FAILED|AUTHENTICATION_FAILED" "$log_file" >> "$output_file"
        # TLS errors
        grep -E "TLS Error:|TLS-ERROR" "$log_file" >> "$output_file"
        # Connectivity issues
        grep -E "Restarting|SIGTERM|SIGUSR1" "$log_file" >> "$output_file"
        # Specific warnings/errors
        grep -E "WARNING:|ERROR:" "$log_file" >> "$output_file"
    else
        echo "OpenVPN log file not found at: $log_file" >> "$output_file"
        return 1 # Indicate an error
    fi
    echo "" >> "$output_file"
    echo "Last 100 lines of OpenVPN log:" >> "$output_file"
    tail -n 100 "$log_file" >> "$output_file" 2>&1 || echo "Could not read last 100 lines of OpenVPN log." >> "$output_file"

    echo "$output_file" # Return the path to the report
    return 0
}

# Function to check for system anomalies
check_system_logs() {
    local log_file="$1"
    local timestamp=$(get_timestamp)
    local output_file="$LOG_BASE_DIR/system_anomalies_$timestamp.log"
    echo "--- System Log Analysis Report ($timestamp) ---" > "$output_file"

    if [ -f "$log_file" ]; then
        # Failed SSH login attempts
        grep -E "Failed password|sshd.*Disconnected" "$log_file" >> "$output_file"
        # Critical system errors
        grep -E "kernel:|error|crit" "$log_file" >> "$output_file"
        # Disk/filesystem errors
        grep -E "disk error|filesystem error|read-only filesystem" "$log_file" >> "$output_file"
        # Network issues
        grep -E "network unreachable|No route to host|connection timed out" "$log_file" >> "$output_file"
    else
        echo "System log file not found at: $log_file" >> "$output_file"
        return 1 # Indicate an error
    fi
    echo "" >> "$output_file"
    echo "Last 100 lines of System log:" >> "$output_file"
    tail -n 100 "$log_file" >> "$output_file" 2>&1 || echo "Could not read last 100 lines of system log." >> "$output_file"

    echo "$output_file" # Return the path to the report
    return 0
}

# Function to perform checklist verification
perform_checklist_verification() {
    local timestamp=$(get_timestamp)
    local output_file="$LOG_BASE_DIR/checklist_report_$timestamp.log"
    local overall_status="ok"
    echo "--- Application Checklist Verification Report ($timestamp) ---" > "$output_file"
    echo "Expected applications to have status files in: $CHECKLIST_BASE_DIR" >> "$output_file"
    echo "" >> "$output_file"

    if [ ! -d "$CHECKLIST_BASE_DIR" ]; then
        echo "ERROR: Checklist directory not found: $CHECKLIST_BASE_DIR" >> "$output_file"
        overall_status="errors"
    else
        for app in "${EXPECTED_CHECKLIST_APPS[@]}"; do
            app_file="$CHECKLIST_BASE_DIR/$app.txt"
            if [ -f "$app_file" ]; then
                echo "[OK] Application '$app' status file found." >> "$output_file"
            else
                echo "[ERROR] Application '$app' status file NOT FOUND at: $app_file" >> "$output_file"
                overall_status="errors"
            fi
        done
    fi
    echo "" >> "$output_file"
    echo "Overall Checklist Status: $overall_status" >> "$output_file"

    echo "$output_file" # Return the path to the report
    echo "$overall_status" # Return the status (for main script to aggregate)
    return 0
}


# Function to archive logs
archive_logs() {
    local timestamp=$(get_timestamp)
    local archive_name="monitoring_logs_$timestamp.tar.gz"
    local archive_path="$BACKUP_BASE_DIR/$archive_name"

    # List all current logs and reports generated by this script run
    local files_to_archive=()
    for file in "$LOG_BASE_DIR"/*_anomalies_*.log "$LOG_BASE_DIR"/*_report_*.log "$LOG_BASE_DIR"/*_recent_*.log; do
        if [ -f "$file" ]; then
            files_to_archive+=("$file")
        fi
    done

    # Add the run history and status files
    files_to_archive+=("$SCRIPT_RUN_HISTORY_LOG" "$STATUS_FILE" "$LATEST_INTRUSION_LOG_PATH_FILE" "$LATEST_CHECKLIST_REPORT_PATH_FILE")

    if [ ${#files_to_archive[@]} -gt 0 ]; then
        tar -czf "$archive_path" -C "$LOG_BASE_DIR" $(for f in "${files_to_archive[@]}"; do echo "$(basename "$f")"; done)
        echo "Logs and reports archived to: "$archive_path""
    else
        echo "No logs or reports to archive."
    fi
}

# --- Main execution ---
ensure_dirs
log_script_history

start_time=$(date +%s)
echo "--- Script Run Details ($(get_timestamp)) ---" > "$CURRENT_RUN_DETAILS_LOG"
echo "" >> "$CURRENT_RUN_DETAILS_LOG"

overall_run_status="ok"

# Check OpenVPN logs
echo "Checking OpenVPN logs..." >> "$CURRENT_RUN_DETAILS_LOG"
vpn_report_path=$(check_openvpn_logs "$OPENVPN_LOG")
if [ $? -ne 0 ]; then
    overall_run_status="errors"
fi
echo "OpenVPN report: $vpn_report_path" >> "$CURRENT_RUN_DETAILS_LOG"
echo "$vpn_report_path" > "$LATEST_INTRUSION_LOG_PATH_FILE"

# Check System logs
echo "Checking System logs..." >> "$CURRENT_RUN_DETAILS_LOG"
sys_report_path=$(check_system_logs "$SYS_LOG")
if [ $? -ne 0 ]; then
    overall_run_status="errors"
fi
echo "System report: $sys_report_path" >> "$CURRENT_RUN_DETAILS_LOG"
# Note: For intrusion detection, you might want to combine these into one "intrusion" log
# For simplicity, here we just update LATEST_INTRUSION_LOG_PATH_FILE with the last one checked.
# In a real scenario, you'd merge or link both VPN and system anomalies.


# Perform Checklist Verification
echo "Performing Checklist Verification..." >> "$CURRENT_RUN_DETAILS_LOG"
checklist_output=$(perform_checklist_verification)
checklist_report_path=$(echo "$checklist_output" | head -n 1)
checklist_status=$(echo "$checklist_output" | tail -n 1)

if [ "$checklist_status" = "errors" ]; then
    overall_run_status="errors"
fi
echo "Checklist report: $checklist_report_path" >> "$CURRENT_RUN_DETAILS_LOG"
echo "$checklist_report_path" > "$LATEST_CHECKLIST_REPORT_PATH_FILE"

# Determine final status for GUI
if [ "$overall_run_status" = "errors" ]; then
    echo "errors" > "$STATUS_FILE"
    echo "Overall Status: ERRORS DETECTED" >> "$CURRENT_RUN_DETAILS_LOG"
else
    echo "ok" > "$STATUS_FILE"
    echo "Overall Status: OK" >> "$CURRENT_RUN_DETAILS_LOG"
fi

# Archive all generated logs and reports
archive_logs

end_time=$(date +%s)
duration=$((end_time - start_time))
echo "Script finished in $duration seconds." >> "$CURRENT_RUN_DETAILS_LOG"
echo "--- End of Script Run Details ---" >> "$CURRENT_RUN_DETAILS_LOG"
