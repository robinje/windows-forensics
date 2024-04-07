import pprint
import subprocess

def get_windows_logs():
    try:
        # Run the wevtutil command to get the list of logs
        output = subprocess.check_output(['wevtutil', 'el'], universal_newlines=True)
    except subprocess.CalledProcessError as err:
        print(f"Error executing command: {err}")
        return []
        
    # Split the output into lines
    lines = output.split('\n')
    
    # Remove any empty lines
    logs = [line.strip() for line in lines if line.strip()]
    
    return logs


def get_log_entries(log_name):

    results = {}

    try:
        # Run the wevtutil command to get the entries in the log
        output = subprocess.check_output(['wevtutil', 'qe', log_name], universal_newlines=True, stderr=subprocess.STDOUT)

    except subprocess.CalledProcessError as err:
        error_message = str(err.output)
        if "Access is denied." in error_message:
            return results  # Return an empty list to indicate access denied error
        elif err.returncode == 4201:
            return results  # Return an empty list to indicate channel not found error
        else:
            print(f"Error executing command for log '{log_name}': {err}")
            return results
        
    # Split the output into lines
    lines = output.split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith('name:'):
            event_name = line.split(':')[1].strip()
            results[event_name] = results.get(event_name, 0) + 1
    
    return results


# Iterate over the logs and count the event occurrences
def main():

    # Get the list of Windows logs
    windows_logs = get_windows_logs()

    for log in windows_logs:
        events: dict = get_log_entries(log)
        if events:
            # Print the dictionary
            print(log)
            pprint.pprint(events)

if __name__ == "__main__":
    main()