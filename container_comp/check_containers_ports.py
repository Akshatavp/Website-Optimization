import socket
import time
import docker
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from AI_Integration.Analysis import predict_traffic_average

def check_port(host, port):
    """Check if a specific port is open on a host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Set timeout for socket operations
        try:
            s.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False

def monitor_ports_and_manage_containers(host, ports, container_ids, image_name, desired_count):
    """Monitor the status of the specified ports and manage containers."""
    client = docker.from_env()
    open_ports = sum(check_port(host, port) for port in ports)
    print(f"\nChecking ports on {host}...")
    print(f"Open ports: {open_ports}")

    running_containers = {
        container.id[:12]: container 
        for container in client.containers.list(all=True) 
        if container.status == 'running' and container.id[:12] in container_ids
    }
    print(f"Running containers: {running_containers}")

    running_ids = set(running_containers.keys())
    current_running_count = len(running_ids)
    print(f"Current running containers (specified IDs): {current_running_count}")

    if current_running_count < desired_count:
        for i in range(desired_count - current_running_count):
            if i < len(container_ids):
                container_id = container_ids[i]
                if container_id not in running_ids:
                    try:
                        container = client.containers.get(container_id)
                        container.start()
                        print(f"Started existing container {container.short_id}")
                    except docker.errors.NotFound:
                        port_mapping = {3000: ports[i]}
                        container = client.containers.run(image_name, detach=True, ports=port_mapping)
                        print(f"Created and started new container {container.short_id} with port mapping {port_mapping}")
                    except docker.errors.APIError as e:
                        print(f"Error starting container {container_id}: {e}")
            else:
                try:
                    port_mapping = {3000: ports[current_running_count + i]}
                    container = client.containers.run(image_name, detach=True, ports=port_mapping)
                    print(f"Started new container with port mapping {port_mapping}")
                except IndexError:
                    print("Not enough ports provided for desired count.")
                    break
    elif current_running_count > desired_count:
        for container_id, container in list(running_containers.items())[desired_count:]:
            try:
                container.stop()
                print(f"Stopped container {container.short_id}")
            except docker.errors.APIError as e:
                print(f"Error stopping container {container.short_id}: {e}")

if __name__ == "__main__":
    host = "127.0.0.1"
    ports = [3001, 3002, 3003]
    container_ids = ["54518e8108cd", "c0f413718a93", "40fc34ff1732"]
    image_name = "webopti-1"

    while True:
        desired_count = predict_traffic_average("../data/synthetic_traffic_data.csv")
        print(f"Desired container count: {desired_count}")
        monitor_ports_and_manage_containers(host, ports, container_ids, image_name, desired_count)
        time.sleep(2 * 60)  # Sleep for 7 minutes
