import requests
from concurrent.futures import ThreadPoolExecutor
import time

# Define the API endpoint
API_REGISTER_ENDPOINT = 'http://localhost:3000/register'
API_ENDPOINT = 'http://localhost:8070/'

# Define the number of requests per second
REQUESTS_PER_SECOND = 50000  # Change this value to adjust requests per second

# Define the number of total requests
TOTAL_REQUESTS = 10000

# Function to send a single request
def send_request():
    try:
        response = requests.get(API_ENDPOINT)  # Adjust method and data as needed
        # response = requests.post(API_REGISTER_ENDPOINT, json={"key": "value"})  # Adjust method and data as needed
        print(f'Response status code: {response.status_code}')
    except requests.RequestException as e:
        print(f'Error sending request: {e}')

def main():
    with ThreadPoolExecutor(max_workers=REQUESTS_PER_SECOND) as executor:
        for i in range(TOTAL_REQUESTS):
            executor.submit(send_request)
            time.sleep(1 / REQUESTS_PER_SECOND)  # Wait to ensure only the desired rate of requests per second

if __name__ == '__main__':
    # Time the execution
    start_time = time.time()
    main()
    end_time = time.time()
    
    print(f'Time taken: {end_time - start_time} seconds')
