import requests

def main():
    base_url = "http://httpbin.org"

    query_params = {
        "name": "Alexey",
        "job": "developer",
        "experience": 9
    }

    headers = {
        "X-Shop-Token": "vfhnsirf",
        "User-Agent": "Mega-Browser"
    }

    response = requests.post(base_url + "/post", data=query_params, headers=headers)
    print(response.json())


if __name__ == '__main__':
    main()
