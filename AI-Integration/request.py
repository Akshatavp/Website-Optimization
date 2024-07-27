import requests

def check_server(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Server at {url} is up and running.")
        else:
            print(f"Server at {url} is up but returned status code: {response.status_code}")
    except requests.ConnectionError:
        print(f"Server at {url} is down.")

def shutdown_server(port, hostname='127.0.0.1'):
    url = f"http://{hostname}:{port}/shutdown"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Server at {url} has been shut down.")
        else:
            print(f"Failed to shut down server at {url}. Status code: {response.status_code}")
    except requests.ConnectionError:
        print(f"Server at {url} is already down or cannot be reached.")

def monitor_servers(ports, hostname='127.0.0.1'):
    urls = [f"http://{hostname}:{port}" for port in ports]
    for url in urls:
        check_server(url)

def read_ports_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            ports = file.read().splitlines()
            return [int(port.strip()) for port in ports if port.strip().isdigit()]
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

if __name__ == "__main__":
    file_path = 'ports.txt'  # File containing the list of all possible ports
    all_ports = read_ports_from_file(file_path)

    if not all_ports:
        print("No ports found in ports.txt.")
        exit(1)

    # Take input from the user
    num_ports = int(input("Enter the number of ports to monitor: "))

    # Determine the ports to monitor based on input
    if 1 <= num_ports <= len(all_ports):
        ports_to_monitor = all_ports[:num_ports]
        print(f"Monitoring the following ports: {ports_to_monitor}")
        
        # Monitor the specified number of ports
        monitor_servers(ports_to_monitor)
        
        # Shut down ports that are not being monitored
        ports_not_monitored = all_ports[num_ports:]
        for port in ports_not_monitored:
            print(f"Shutting down server at http://127.0.0.1:{port}")
            shutdown_server(port)
    else:
        print(f"Invalid input. Please enter a number between 1 and {len(all_ports)}.")
