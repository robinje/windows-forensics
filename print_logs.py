import subprocess

# Specify the name of the Windows log
LOG_NAME = "Windows PowerShell"

def get_log_entries(log_name, num_entries=60):
    try:
        # Run the wevtutil command to get the log entries
        output = subprocess.check_output(['wevtutil', 'qe', log_name, '/c:{}'.format(num_entries), '/rd:true', '/f:text'], universal_newlines=True, stderr=subprocess.STDOUT)
        
        # Split the output into lines
        lines = output.strip().split('\n')
        
        # Remove empty lines and lines starting with "Event["
        entries = [line for line in lines if line.strip() and not line.startswith('Event[')]
        
        return entries
    except subprocess.CalledProcessError as e:
        error_message = str(e.output)
        if "Access is denied." in error_message:
            print(f"Access denied for log '{log_name}'.")
        elif e.returncode == 4201:
            print(f"Log channel '{log_name}' not found.")
        else:
            print(f"Error retrieving entries from log '{log_name}': {e}")
        return []

# Get the first 10 entries from the specified log
log_entries = get_log_entries(LOG_NAME)

# Print the log entries
if log_entries:
    print(f"First 10 entries from the '{LOG_NAME}' log:")
    for entry in log_entries:
        print(entry)
else:
    print(f"No entries found in the '{LOG_NAME}' log.")