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
            metric_data.append(string[3])
    return metric_data


if __name__ == '__main__':
    str = input()

    team_count = str.split("$")
    team_name_list = []
    new_data = []
    print(len(team_count))
    for team_number in range(0, len(team_count)):
        team_name = team_count[team_number].split("|")[0]
        team_data = team_count[team_number].split("|")[1].split(";")
        team_name_list.append(team_name)
        project_list = []
        resource_list = []
        print(len(team_data))
        for team_data_number in range(0, len(team_data)):
            project_list.append(team_data[team_data_number].strip("()").split(",")[0])
            resource_list.append(team_data[team_data_number].strip("()").split(",")[1])
            new_data.append([team_name, team_data[team_data_number].strip("()").split(",")[0],
                            team_data[team_data_number].strip("()").split(",")[1],
                             team_data[team_data_number].strip("()").split(",")[3]])

    project_list = list(set(project_list))
    resource_list = list(set(resource_list))

    print(project_list)
    # for j in range(10, 700):
    #     print(new_data[j])

    team_data = {}
    for team in team_name_list:
        project = {}
        for prj in project_list:
            resource = {}
            for res in resource_list:
                metric_list = []
                    #get_metric(team, prj, res, new_data)
                resource.update({res: metric_list})
            project.update({prj: resource})
        team_data.update({team: project})

    #print(team_data)
    # for i in range(0, len(new_data)):
    #     print(new_data[i])

#TODO 'envisioneer rich mindshare':
#           {'SZY1417':
#               {'CPU':
#                   {'mean': 51.645, 'mediana': 53.0, 'usage_type': 'Stable', 'intensivity': 'Medium'};
#                'RAM':
#                   {'mean': 51.645, 'mediana': 53.0, 'usage_type': 'Stable', 'intensivity': 'Medium'};
#               }
#            }

    #print(team_data["drive revolutionary infrastructures"]["420-809"])

#{'envisioneer rich mindshare': {'420-809': {'CPU': [], 'RAM': [], 'NetFlow': []}, '2S O9806': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'L 139693': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'NBX-4230': {'CPU': [], 'RAM': [], 'NetFlow': []}, '4023 TM': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'DVM-4870': {'CPU': [], 'RAM': [], 'NetFlow': []}, '2563 ZS': {'CPU': [], 'RAM': [], 'NetFlow': []}, '168V': {'CPU': [], 'RAM': [], 'NetFlow': []}, '426 CCJ': {'CPU': [], 'RAM': [], 'NetFlow': []}, '7VR 831': {'CPU': [], 'RAM': [], 'NetFlow': []}},
#'implement open-source bandwidth': {'420-809': {'CPU': [], 'RAM': [], 'NetFlow': []}, '2S O9806': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'L 139693': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'NBX-4230': {'CPU': [], 'RAM': [], 'NetFlow': []}, '4023 TM': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'DVM-4870': {'CPU': [], 'RAM': [], 'NetFlow': []}, '2563 ZS': {'CPU': [], 'RAM': [], 'NetFlow': []}, '168V': {'CPU': [], 'RAM': [], 'NetFlow': []}, '426 CCJ': {'CPU': [], 'RAM': [], 'NetFlow': []}, '7VR 831': {'CPU': [], 'RAM': [], 'NetFlow': []}},
#'strategize world-class web services': {'420-809': {'CPU': [], 'RAM': [], 'NetFlow': []}, '2S O9806': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'L 139693': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'NBX-4230': {'CPU': [], 'RAM': [], 'NetFlow': []}, '4023 TM': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'DVM-4870': {'CPU': [], 'RAM': [], 'NetFlow': []}, '2563 ZS': {'CPU': [], 'RAM': [], 'NetFlow': []}, '168V': {'CPU': [], 'RAM': [], 'NetFlow': []}, '426 CCJ': {'CPU': [], 'RAM': [], 'NetFlow': []}, '7VR 831': {'CPU': [], 'RAM': [], 'NetFlow': []}},
#'drive revolutionary infrastructures': {'420-809': {'CPU': [], 'RAM': [], 'NetFlow': []}, '2S O9806': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'L 139693': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'NBX-4230': {'CPU': [], 'RAM': [], 'NetFlow': []}, '4023 TM': {'CPU': [], 'RAM': [], 'NetFlow': []}, 'DVM-4870': {'CPU': [], 'RAM': [], 'NetFlow': []}, '2563 ZS': {'CPU': [], 'RAM': [], 'NetFlow': []}, '168V': {'CPU': [], 'RAM': [], 'NetFlow': []}, '426 CCJ': {'CPU': [], 'RAM': [], 'NetFlow': []}, '7VR 831': {'CPU': [], 'RAM': [], 'NetFlow': []}}}