import requests

def main():
    base_url = "http://httpbin.org"

    query_params = {
        "order": "votes",
        "sort": "desc"
    }

    headers = {
        "X-Shop-Token": "vfhnsirf",
        "User-Agent": "Mega-Browser"
    }

    response = requests.get(base_url + "/get", params=query_params, headers=headers)
    print(response.json())


if __name__ == '__main__':
    main()