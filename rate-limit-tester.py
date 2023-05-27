import requests
import threading
import time
import random
import string
from urllib.parse import urlparse, parse_qs, urlencode

latest_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.1234.5678 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.1234.5678 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.1234.5678 Safari/537.36 Edg/98.0.5678.1234',
    'Mozilla/5.0 (Windows NT 10.0; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
]

lock = threading.Lock()
successful_requests = 0
total_requests = 0
stop_execution = False

def make_request(url):
    global successful_requests, total_requests, stop_execution

    headers = {
        'User-Agent': random.choice(latest_user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
        'Cache-Control': 'max-age=0'
    }

    while True:
        lock.acquire()
        count = total_requests + 1
        total_requests += 1
        lock.release()

        if count == 101 and successful_requests == 0:
            start_101st_request_time = time.time()

        if stop_execution:
            break

        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params['test'] = [''.join(random.choices(string.ascii_lowercase + string.digits, k=8))]
        modified_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()

        response = requests.get(modified_url, headers=headers)
        if response.status_code == 200:
            lock.acquire()
            successful_requests += 1
            lock.release()
            print(f"Request {count}: Successful")

            if count == 101 and successful_requests == 1:
                end_101st_request_time = time.time()

            if count > 100 and response.status_code != 200:
                time_taken = time.time() - end_101st_request_time
                print(f"Time taken from 101st request until status code change: {time_taken} seconds")
                stop_execution = True

        else:
            lock.acquire()
            stop_execution = True
            lock.release()
            print(f"Request {count}: Failed with status code: {response.status_code}")
            break

url = input("Enter the URL: ")
thread_count_input = input("Enter the thread count (default: 10): ")

thread_value = int(thread_count_input) if thread_count_input.isdigit() else 10

start_time = time.time()
threads = []

for _ in range(thread_value):
    thread = threading.Thread(target=make_request, args=(url,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end_time = time.time()

print(f"\nTotal Requests: {total_requests}")
print(f"Successful Requests: {successful_requests}")
print(f"Time taken to change status code from 200: {end_time - start_time} seconds")
