from collections import Counter


def new_rps_from_input():
    """
    Ввод дополнительный значений prs
    :return: возврат дополнительных значений
    """
    print("Введите новое знаечение или значения rps или ничего")
    rps = input()
    new_rps = []
    rps = rps.strip("()")
    while rps != "":
        if ";" in rps:
            new_rps.extend(rps.split(";"))
        else:
            new_rps.append(rps)
        rps = input()
    return new_rps


def boarders_get(lst):
    """
    Ввод границ среза данных для обработки
    :param lst: лист с данными
    :return: первое и последнее значение границ среза
    """
    print("Введите границы среза через запятую или пустое значение")
    boarders = input().strip("[]")
    first, last = 0, len(lst)
    if "," in boarders and len(boarders.split(",")) <= 2:
        first, last = (boarders.split(","))
    else:
        print("не верный ввод")
    return int(first), int(last)


def main():
    rps_values = [
        5081, '17184', 10968, 9666, '9102', 12321, '10617', 11633, 5035, 9554, '10424', 9378, '8577', '11602', 14116,
        '8066', '11977', '8572', 9685, 11062, '10561', '17820', 16637, 5890, 17180, '17511', '13203', 13303, '7330',
        7186,
        '10213', '8063', '12283', 15564, 17664, '8996', '12179', '13657', 15817, '16187', '6381', 8409, '5177', 17357,
        '10814', 6679, 12241, '6556', 12913, 16454, '17589', 5292, '13639', '7335', '11531', '14346', 7493, 15850,
        '12791',
        11288]
    append_rps = new_rps_from_input()
    rps_values.extend(append_rps)
    print(rps_values)
    first_index, last_index = boarders_get(rps_values)
    int_rps_values = input_data_to_int(rps_values, first_index, last_index)
    output(compute_avg(int_rps_values), compute_median(int_rps_values))
    make_counter(sorted(int_rps_values, reverse=True))
    print(int_rps_values)


def make_counter(lst):
    """
    Подсчет частоты для списка
    :param lst: иходный список значений
    :return: вывод частот
    """
    rpc_counter = Counter()
    for value in range(0, len(lst)):
        rpc_counter[lst[value]] += 1
    print(rpc_counter)


def input_data_to_int(rps_data, start_position, end_position):
    """
    Приведение всех значений входящего списка к INT, и произведение среза указанным индексам
    :param rps_data: входящие данные
    :param start_position: первый индекс среза
    :param end_position: последний индекс среза
    :return: приведенный к INT список/срез
    """
    output_rps_values = ()
    for i in range(start_position, end_position):
        output_rps_values += (int(rps_data[i]),)
    return output_rps_values


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


def output(avg, median):
    """
    Генерация вывода в консоль
    :param avg: среднее арифметические значение
    :param median: медиана
    :return: вывод на экран
    """
    print(f"avg {avg} median {median}")
    if (avg < 1.25 * median) and (avg > 0.75 * median):
        print("Нагрузка стабильна")
    elif avg > 1.25 * median:
        print("Происходят скачки")
    else:
        print("Происходят снижения")


if __name__ == '__main__':

    main()
