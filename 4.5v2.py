import datetime
import random
from os import getenv

import paramiko
import psycopg2
from requests import Session, get


def compute_median(lst):
    """
    Вычисление медианты списка
    :param lst: входящий список значений
    :return: медиана
    """
    quotient, remainder = divmod(len(lst), 2)
    return lst[quotient] if remainder else sum(sorted(lst)[quotient - 1:quotient + 1]) / 2


def compute_avg(lst):
    """
    Вычисление среднего арифметические значения списка
    :param lst: входящий список значений
    :return: среднее арифметические значение
    """
    return sum(lst) / len(lst)


def usage_type(avg, median):
    """
    Вычисление типа использования
    :param avg: среднее занечение метрик
    :param median: медианное значение метрик
    :return: возврат значения типа использования
    """
    if (avg < 1.25 * median) and (avg > 0.75 * median):
        return "стабильна"
    elif avg > 1.25 * median:
        return "скачки"
    else:
        return "снижения"


def intensity(median):
    """
    Вычисление интенсивности использования
    :param median: медианное значение метрик
    :return: возврат значения интенсивности
    """
    if (0 < median) and (median <= 30):
        return "низкая"
    if (30 < median) and (median <= 60):
        return "умеренная"
    if (60 < median) and (median <= 90):
        return "высокая"
    return "запредельная"


def decision(usage, intens):
    """
    Принятие решения о дальнецшем использовании ресурса
    :param usage: тип использования
    :param intens: интенсивности использованя
    :return: возврат решения
    """
    if intens == "низкая":
        return "отказаться"
    if intens == "запредельная":
        return "усилить"
    if intens == "умеренная" and usage in ("стабильна", "скачки"):
        return "отсавить"
    if intens == "высокая" and usage in ("снижения", "стабильна"):
        return "отсавить"
    if usage == "снижения" and intens == "умеренная":
        return "отказаться"
    if usage == "скачки" and intens == "высокая":
        return "усилить"


def metric_generator(connect_data):
    """
    Генератор метрик в БД
    :param connect_data: Данные для авторизации на сервере генерации метрик
    :return: заполняет БД случайными метриками
    """
    with paramiko.SSHClient() as ssh_connect:
        ssh_connect.load_system_host_keys()
        ssh_connect.connect(**connect_data)
        rnd_seed = random.randint(0, 5)
        _, _, stderr = ssh_connect.exec_command(f"monitoring_module {rnd_seed}")
        error = stderr.read().decode()
        if error:
            print(error)
            exit(1)


def db_data_get(connect_data):
    """
    Получение всех записей из БД
    :param connect_data: Данные для подключения к БД
    :return: Всех записей из БД
    """
    with psycopg2.connect(**connect_data) as db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(R"""
                SET search_path TO usage_stats;
                SELECT team, resource, dimension, collect_date, usage FROM resources;
            """)
            return cursor.fetchall()


def obj_creator(data):
    """
    Генератор обьекта заданной структуры из сырых данных
    :param data: сырые данные
    :return: Обект заданной тсруктуры
    """
    final_data = {}
    for msg in data:
        team_name, project, resource, due, resource_metric = msg
        a = {"time": due, "value": int(resource_metric)}
        final_data.setdefault(team_name, {}).setdefault(project, {}).setdefault(resource, []).append(a)
    return final_data


def get_data_from_http(url):
    """
    Генерация списка метрик по HTTP
    :param url: адресс веб сервера источника метрик
    :return: лист метрик
    """
    rnd_seed = random.randint(1, 3)
    team_raw = get(url + f"/monitoring/infrastructure/using/summary/{rnd_seed}").text.split("$")
    final_list = []
    for team_raw_data in team_raw:
        team_name, team_data = team_raw_data.split("|")
        team_data = team_data.split(";")
        for team_data_split_data in team_data:
            project, resource, due, resource_metric = team_data_split_data[1:-1].split(",")
            yr, mt, dy = due[0:10].split("-")
            date = datetime.date(year=int(yr), month=int(mt), day=int(dy))
            final_list.append((team_name, project, resource, date, int(resource_metric)))
    return final_list


# ------ TRELLO PART ------


def get_trello_boards(session: Session, creds):
    boards = session.get(f"{TRELLO_API_URL}members/me/boards", params=creds).json()
    return {board["name"]: {
        "id": board["id"],
        "column": get_trello_board_columns(session, creds, board["id"])
    } for board in boards}


def universal_trello_getter(session: Session, creds, board_id, resource):
    return session.get(f"{TRELLO_API_URL}boards/{board_id}/{resource}", params=creds).json()


def get_trello_board_columns(session: Session, creds, board_id):
    columns = universal_trello_getter(session, creds, board_id, "lists")
    return {column["name"]: column["id"] for column in columns}


def get_trello_labels(session: Session, creds, board_id):
    labels = universal_trello_getter(session, creds, board_id, "labels")
    return {label["id"]: label["name"] for label in labels}


def get_all_trello_cards_id(session: Session, creds, board_id):
    cards_id_list = universal_trello_getter(session, creds, board_id, "cards/all")
    return [cards_id["id"] for cards_id in cards_id_list]


def create_trello_label(session: Session, creds, board_id, name):
    existing_labels = get_trello_labels(session, creds, board_id)
    if name in existing_labels.values():
        return 0
    colors = ["yellow", "purple", "blue", "red", "green", "orange", "black", "sky", "pink", "lime"]
    query = {**creds,
             "name": name,
             "color": colors[random.randint(0, len(colors)-1)],
             "idBoard": board_id
             }
    session.post(f"{TRELLO_API_URL}labels", params=query)


def create_trello_board_card(session: Session, creds, column_id, team_name, due, resource_data, decision_value):
    resource, project = resource_data
    card_name = ""
    if decision_value == "усилить":
        card_name = f"Увеличить квоты ресурса {project} по измерению {resource}"
    if decision_value == "отказаться":
        card_name = f"Отказаться от использования ресурса {project} по измерению {resource}"

    params = {**creds,
              "name": card_name,
              "idList": column_id,
              "idLabels": team_name,
              "due": due
              }
    session.post(f"{TRELLO_API_URL}cards", params=params)


def delete_all_cards(session: Session, creds, board_id):
    for card_id in get_all_trello_cards_id(session, creds, board_id):
        session.delete(f"{TRELLO_API_URL}cards/{card_id}", params=creds)


def delete_all_labels(session: Session, creds, board_id):
    lebels_list = get_trello_labels(session, creds, board_id)
    for label_id in lebels_list.keys():
        session.delete(f"{TRELLO_API_URL}labels/{label_id}", params=creds)


if __name__ == '__main__':
    print("start")

    TRELLO_API_URL = "https://api.trello.com/1/"
    full_msg = ""

    trello_connect_data = {
        "key": getenv("TRELLO_API_KEY"),
        "token": getenv("TRELLO_API_TOKEN")
    }

    ssh_connect_data = {
        "hostname": "localhost",
        "port": "2222",
        "username": "service_user",
        "password": "q1w2e3"
    }

    db_connect_data = {
        "database": "postgres",
        "user": "postgres",
        "password": "q1w2e3",
        "host": "localhost",
        "port": "5432"
    }

    source_type = ""

    while source_type not in ("DB", "HTTP", "EXIT"):
        source_type = input("Введите источник данных DB/HTTP or EXIT: ")

    if source_type == "DB":
        full_msg = db_data_get(db_connect_data)
    elif source_type == "HTTP":
        full_msg = get_data_from_http("http://127.0.0.1:21122/")
    else:
        print("Выход")
        exit(0)

    trello_session = Session()
    # metric_generator(ssh_connect_data)

    boards = get_trello_boards(trello_session, trello_connect_data)
    board_id = boards["kurstask"].get("id")

    columns = get_trello_board_columns(trello_session, trello_connect_data, board_id)
    column_id = columns["To Do"]

    delete_all_cards(trello_session, trello_connect_data, board_id)
    delete_all_labels(trello_session, trello_connect_data, board_id)

    final_data = obj_creator(full_msg)

    print("Ресурс|Значение|среднее|медиана|использование|интенсивность|решение|дата последний метрики")
    for name, prj in final_data.items():
        print(f"команда {name}")
        create_trello_label(trello_session, trello_connect_data, board_id, name)
        for prj_name, res_values in prj.items():
            for res, values in res_values.items():
                value_list = []
                time = []
                for value in values:
                    value_list.append(value["value"])
                    time.append(value["time"])
                last_time = time[-1] + datetime.timedelta(14)
                median = compute_median(value_list)
                avg = compute_avg(value_list)
                usage = usage_type(avg, median)
                intens = intensity(median)
                final_decision = decision(usage, intens)
                if final_decision != "отсавить":
                    existing_labels = get_trello_labels(trello_session, trello_connect_data, board_id)
                    team_name_id = None
                    for label_id, label_name in existing_labels.items():
                        if label_name == name:
                            team_name_id = label_id
                    create_trello_board_card(session=trello_session,
                                             creds=trello_connect_data,
                                             column_id=column_id,
                                             team_name=team_name_id,
                                             resource_data=(res, prj_name),
                                             due=last_time,
                                             decision_value=final_decision)

                    print(
                     f"{prj_name} | {res} | {avg} | {median} | {usage} | {intens} | {final_decision} | {last_time}")
