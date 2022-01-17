import datetime
import random
import yaml

from requests import get


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


if __name__ == '__main__':
    print("start")

    full_msg = get_data_from_http("http://127.0.0.1:21122/")
    final_data = obj_creator(full_msg)

    yaml_price = get("http://127.0.0.1:21122/monitoring/infrastructure/using/prices").text
    price_full = yaml.safe_load(yaml_price)["values"]

    print("Ресурс|Значение|среднее|медиана|использование|интенсивность|решение|дата последний метрики|цена")
    for name, prj in final_data.items():
        print(f"команда {name}")
        for prj_name, res_values in prj.items():
            summ = 0
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
                cost = price_full[prj_name]
                summ += int(cost[res])
                print(f"{prj_name} | {res} | {avg} | {median} | {usage} | {intens} | {final_decision} | {last_time} | {cost[res]}")
            print(f"Цена за ресурс = {summ}")
