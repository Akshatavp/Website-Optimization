import socket
import time
import docker
from AI_Integration.Analysis import determine_required_value 

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

    while True:
        open_ports = sum(check_port(host, port) for port in ports)
        print(f"\nChecking ports on {host}...")
        print(f"Open ports: {open_ports}")

        running_containers = {container.id[:12]: container for container in client.containers.list(all=True) if container.status == 'running'}
        running_ids = set(running_containers.keys())

        current_running_count = len(running_ids)
        print(f"Current running containers: {current_running_count}")

        # Start new containers if running count is less than desired count
        if current_running_count < desired_count:
            for i in range(desired_count - current_running_count):
                try:
                    if i < len(container_ids):
                        container_id = container_ids[i]
                        if container_id not in running_ids:
                            try:
                                # If container exists but isn't running, start it
                                container = client.containers.get(container_id)
                                container.start()
                                print(f"Started existing container {container.short_id}")
                            except docker.errors.NotFound:
                                # If container doesn't exist, create and start it
                                port_mapping = {3000: ports[i]}
                                container = client.containers.run(image_name, detach=True, ports=port_mapping)
                                print(f"Created and started new container {container.short_id} with port mapping {port_mapping}")
                            except docker.errors.APIError as e:
                                print(f"Error starting container {container_id}: {e}")
                    else:
                        # Create new container if container_ids list is exhausted
                        port_mapping = {3000: ports[current_running_count + i]}
                        container = client.containers.run(image_name, detach=True, ports=port_mapping)
                        print(f"Started new container with port mapping {port_mapping}")
                except IndexError:
                    print("Not enough ports or container IDs provided for desired count.")
                    break

        # Stop extra containers if running count is more than desired count
        elif current_running_count > desired_count:
            for container_id, container in list(running_containers.items())[desired_count:]:
                try:
                    container.stop()
                    print(f"Stopped container {container.short_id}")
                except docker.errors.APIError as e:
                    print(f"Error stopping container {container.short_id}: {e}")

        time.sleep(5)  # Wait for 5 seconds before checking again

if __name__ == "__main__":
    host = "127.0.0.1"  # Host to check (localhost in this case)
    ports = [3001, 3002, 3003]  # List of ports to map on the host
    container_ids = ["54518e8108cd", "c0f413718a93", "40fc34ff1732"]  # Replace with your container IDs
    image_name = "webopti-1"  # Replace with your Docker image name
    desired_count = determine_required_value()  # Desired number of running containers
    print(desired_count)
    print(f"Monitoring ports on {host}: {ports}")
    monitor_ports_and_manage_containers(host, ports, container_ids, image_name, desired_count)

