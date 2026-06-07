import requests

def fetch_status() -> int:
    response = requests.get('https://httpbin.org/status/200')
    return response.status_code

if __name__ == '__main__':
    print(f"Running app. Status code: {fetch_status()}")