import psycopg2
import paramiko
import datetime
import random
from os import getenv
from requests import Session


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


def get_metric(team, prj, res, data):
    metric_data = []
    for string in data:
        if string[0] == team and string[1] == prj and string[2] == res:
            metric_data.append(int(string[3]))
    return metric_data


def usage_type(avg, median):
    if (avg < 1.25 * median) and (avg > 0.75 * median):
        msg = "стабильна"
    elif avg > 1.25 * median:
        msg = "скачки"
    else:
        msg = "снижения"
    return msg


def intensity(median):
    if (0 < median) and (median <= 30):
        msg = "низкая"
    elif (30 < median) and (median <= 60):
        msg = "умеренная"
    elif (60 < median) and (median <= 90):
        msg = "высокая"
    else:
        msg = "запредельная"
    return msg


def decision(usage, intens):
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
    with paramiko.SSHClient() as ssh_connect:
        ssh_connect.load_system_host_keys()
        ssh_connect.connect(**connect_data)
        rnd_seed = random.randint(0, 5)
        stdin, stdout, stderr = ssh_connect.exec_command(f"monitoring_module {rnd_seed}")


def db_data_get(connect_data):
    with psycopg2.connect(**connect_data) as db_connection:
        with db_connection.cursor() as cursor:
            cursor.execute(R"""
                SET search_path TO usage_stats;
                SELECT team, resource, dimension, collect_date, usage FROM resources;
            """)
            return cursor.fetchall()


def obj_creator(data):
    final_data = {}
    for msg in data:
        team_name, project, resource, due, resource_metric = msg
        a = {"time": due, "value": int(resource_metric)}
        final_data.setdefault(team_name, {}).setdefault(project, {}).setdefault(resource, []).append(a)
    return final_data


# ------ TRELLO PART ------


def get_trello_boards(session: Session, creds):
    boards = session.get("https://api.trello.com/1/members/me/boards", params=creds).json()
    return {board["name"]: {
        "id": board["id"],
        "column": get_trello_board_columns(session, creds, board["id"])
    } for board in boards}


def get_trello_board_columns(session: Session, creds, board_id):
    columns = session.get(f"https://api.trello.com/1/boards/{board_id}/lists", params=creds).json()
    return {column["name"]: column["id"] for column in columns}


def get_trello_labels(session: Session, creds, board_id):
    labels = session.get(f"https://api.trello.com/1/boards/{board_id}/labels", params=creds).json()
    return {label["id"]: label["name"] for label in labels}


def get_all_cards_id(session: Session, creds, board_id):
    cards_id_list = session.get(f"https://api.trello.com/1/boards/{board_id}/cards/all",
                                params=creds).json()
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
    session.post("https://api.trello.com/1/labels", params=query)


def create_trello_board_card(session: Session, creds, column_id, team_name, due, resource_id, decision_value):
    if decision_value == "усилить":
        name = f"Увеличить квоты ресурса {resource_id} по измерению {decision_value}"
    elif decision_value == "отказаться":
        name = f"Отказаться от использования ресурса {resource_id} по измерению {decision_value}"
    else:
        return 0

    params = {**creds,
              "name": name,
              "idList": column_id,
              "idLabels": team_name,
              "due": due
              }

    session.post("https://api.trello.com/1/cards", params=params)


def delete_all_cards(session: Session, creds, board_id):
    for card_id in get_all_cards_id(session, creds, board_id):
        session.delete(f"https://api.trello.com/1/cards/{card_id}", params=creds)
    return 0


def delete_all_labels(session: Session, creds, board_id):
    lebels_list = get_trello_labels(session, creds, board_id)
    for label_id in lebels_list.keys():
        session.delete(f"https://api.trello.com/1/labels/{label_id}", params=creds)
    return 0


if __name__ == '__main__':
    print("start")

    trello_connect_data = {
        "key": getenv("TRELLO_API_KEY"),
        "token": getenv("TRELLO_API_TOKEN")
    }

    trello_session = Session()

    boards = get_trello_boards(trello_session, trello_connect_data)
    board_id = None
    for board_name, board_data in boards.items():
        if board_name == "kurstask":
            board_id = board_data["id"]

    columns = get_trello_board_columns(trello_session, trello_connect_data, board_id)
    column_id = None
    for column_name, column_id_ex in columns.items():
        if column_name == "To Do":
            column_id = column_id_ex

    # exit(0)
    delete_all_cards(trello_session, trello_connect_data, board_id)
    delete_all_labels(trello_session, trello_connect_data, board_id)


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

    # metric_generator(ssh_connect_data)

    full_msg = db_data_get(db_connect_data)
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
                    # print(existing_labels)
                    team_name_id = None
                    for label_id, label_name in existing_labels.items():
                        # print(f"ID {label_id}, Name {label_name} WITH name {name}")
                        if label_name == name:
                            team_name_id = label_id
                    # print(team_name_id)
                    create_trello_board_card(session=trello_session,
                                             creds=trello_connect_data,
                                             column_id=column_id,
                                             team_name=team_name_id,
                                             resource_id=f"{res} в проекте {prj_name}",
                                             due=last_time,
                                             decision_value=final_decision)

                    print(
                     f"{prj_name} | {res} | {avg} | {median} | {usage} | {intens} | {final_decision} | {last_time}")
