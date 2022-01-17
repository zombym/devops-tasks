import requests

from flask import Flask, Response

from prometheus_client.core import REGISTRY, HistogramMetricFamily
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


class CustomCollector(object):
    stored_teams = {}

    BUCKETS = {
        "0": 0,
        "10": 0,
        "20": 0,
        "30": 0,
        "40": 0,
        "50": 0,
        "60": 0,
        "70": 0,
        "80": 0,
        "90": 0,
        "100": 0
    }

    def collect(self):
        export_data = HistogramMetricFamily('my_counter_total', 'Help text', labels=['name', 'team'])

        for label, data in CustomCollector.stored_teams.items():
            for project, resources in data[0].items():
                for res in resources:
                    summ = 0
                    BUC = CustomCollector.BUCKETS.copy()
                    for value in resources[res]:
                        summ += value
                        BUC[str(round(value, -1))] += 1

                    export_data.add_metric([label, f"{project}-{res}"], list(BUC.items()), summ)
        yield export_data


REGISTRY.register(CustomCollector())


app = Flask(__name__)


@app.route("/")
def export():
    return main()


def main():
    base_url = "http://127.0.0.1:21122/"
    response = requests.get(base_url + "/monitoring/infrastructure/using/summary/1")
    team_raw = response.text.split("$")
    final_data = {}
    msg = []

    for team_raw_data in team_raw:
        precessed_data = {}
        team_name, team_data = team_raw_data.split("|")
        team_data = team_data.split(";")

        for team_data_split_data in team_data:
            project, resource, *_, resource_metric = team_data_split_data[1:-1].split(",")
            precessed_data.setdefault(project, {}).setdefault(resource, []).append(int(resource_metric))
        final_data.setdefault(team_name, []).append(precessed_data)

    CustomCollector.stored_teams = final_data

    for name in final_data.keys():
        for prj in final_data[name]:
            for prj_name, prj_values in prj.items():
                for res, val in prj_values.items():
                    for measurement in val:
                        msg.append(f"{name} | {prj_name}-{res} | {measurement}<br>")
    return ''.join(msg)


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(port=33281)
