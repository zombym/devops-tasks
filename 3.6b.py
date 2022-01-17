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


if __name__ == '__main__':
    input_data = input()
    team_raw = input_data.split("$")
    final_data = {}

    for team_raw_data in team_raw:
        precessed_data = {}
        team_name, team_data = team_raw_data.split("|")
        team_data = team_data.split(";")

        project_metrics = {}
        for team_data_split_data in team_data:
            project, resource, *_, resource_metric = team_data_split_data[1:-1].split(",")
            precessed_data.setdefault(project, {}).setdefault(resource, []).append(int(resource_metric))
        final_data.setdefault(team_name, []).append(precessed_data)

    print("Ресурс|Значение|среднее|медиана|использование|интенсивность|решение|")
    for name, data in final_data.items():
        print(f"команда {name}")
        for prj in data:
            for prj_name, prj_values in prj.items():
                for res, val in prj_values.items():
                    median = compute_median(val)
                    avg = compute_avg(val)
                    usage = usage_type(avg, median)
                    intens = intensity(median)
                    print(f"{prj_name} | {res} | {avg} | {median} | {usage} | {intens} | {decision(usage, intens)}")
