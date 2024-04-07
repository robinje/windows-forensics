import subprocess

def get_windows_logs():
    try:
        # Run the wevtutil command to get the list of logs
        output = subprocess.check_output(['wevtutil', 'el'], universal_newlines=True)
        
        # Split the output into lines
        lines = output.split('\n')
        
        # Remove any empty lines
        logs = [line.strip() for line in lines if line.strip()]
        
        return logs
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return []

def get_log_entry_count(log_name):
    try:
        # Run the wevtutil command to get the number of entries in the log
        output = subprocess.check_output(['wevtutil', 'qe', log_name], universal_newlines=True, stderr=subprocess.STDOUT)
        
        # Split the output into lines
        lines = output.split('\n')
        
        # Return the number of lines (excluding the header and empty lines)
        return len([line for line in lines if line.strip() and not line.startswith('Event[')])
    except subprocess.CalledProcessError as e:
        error_message = str(e.output)
        if "Access is denied." in error_message:
            return -1  # Return -1 to indicate access denied error
        elif e.returncode == 4201:
            return -2  # Return -2 to indicate channel not found error
        else:
            print(f"Error executing command for log '{log_name}': {e}")
            return 0

# Get the list of Windows logs
windows_logs = get_windows_logs()

# Print the logs with more than one entry
print("Logs with more than one entry:")
for log in windows_logs:
    entry_count = get_log_entry_count(log)
    if entry_count == -1:
        continue  # Skip logs with access denied error
    elif entry_count > 1:
        print(f"{log}: {entry_count} entries")