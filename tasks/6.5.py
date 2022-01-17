import json
import os
import datetime
import argparse
from requests import get


def data_from_file(file_path) -> list:
    """
    Получение списка ключенй из файла
    :param file_path: пусть к файлу
    :return: список ключей
    """
    with open(file_path, "r") as answer_file:
        return json.loads(answer_file.read())


def get_data_from_http(url) -> list:
    """
    Получение списка ключенй из внешнего источника
    :param url: адрес источника
    :return: список ключей
    """
    return json.loads(get(url).text)


def get_data_from_local() -> list:
    """
    Получение списка ключенй из существующего authorized_keys
    :return: список ключей
    """
    local_keys = []
    if os.path.exists(f"{SSH_KEY_PATH}{SSH_KEY_FILE}"):
        with open(f"{SSH_KEY_PATH}{SSH_KEY_FILE}", "r") as auth_file:
            auth_file_text = auth_file.read().split("\n")[:-1]
            for keys_records in auth_file_text:
                keys_records = keys_records.split(" ")
                local_keys.append({"email": keys_records[2], "rsa_pub_key": keys_records[1], "access_until": None})
    return local_keys


if __name__ == '__main__':

    SSH_KEY_PATH = "./.ssh/"
    SSH_KEY_FILE = "authorized_keys"

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default=False, nargs=1)
    parser.add_argument("-u", "--url", default=False, nargs=1)
    parser.add_argument("-r", "--refresh", default=0, nargs=1)
    args = parser.parse_args()

    if not (args.file or args.url):
        print("Please insert FILE path or URL")
        exit(0)

    if args.file:
        external_data = data_from_file(args.file[0])
    if args.url:
        external_data = get_data_from_http(args.url[0])

    exist_keys = get_data_from_local()

    print("INPUT DATA: ", external_data)
    print("EXIST KEYS: ", exist_keys)

    # new_keys = []
    # for key_string in exist_keys:
    #     for




    # if os.path.exists(f"{SSH_KEY_PATH}{SSH_KEY_FILE}"):
    #     print("EXIST")
    #     with open(f"{SSH_KEY_PATH}{SSH_KEY_FILE}", "r") as auth_file:
    #         auth_file_text = auth_file.read()
    #         print(auth_file_text.split("\n"))
    # else:


    # os.mkdir(SSH_KEY_PATH)
    # with open(f"{SSH_KEY_PATH}{SSH_KEY_FILE}", "w") as auth_file:
    #
    #     auth_str = "ssh-rsa"
    #     email = ""
    #     ssh_key = ""
    #     due = ""
    #     today = datetime.date
    #
    #     for obj in external_data:
    #         for key, value in obj.items():
    #             if key == "email":
    #                 email = value
    #             if key == "rsa_pub_key":
    #                 ssh_key = value
    #             if key == "access_until":
    #                 dy, mt, yr = value.split("-")
    #                 due = datetime.date(year=int(yr), month=int(mt), day=int(dy))
    #         if today.today() <= due:
    #             auth_file.write(f"{auth_str} {ssh_key} {email}\n")


