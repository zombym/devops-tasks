import requests
import json
import jsonschema
import yaml
import os
import datetime
from zoneinfo import ZoneInfo

import gitlab

GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
GITLAB_URL = os.getenv('GITLAB_URL', 'https://gitlab.lipstack.sephoraus.com')
GITLAB_BRANCH = os.getenv('GITLAB_BRANCH', 'MSP-1561')
GITLAB_SOURCE_REPO_ID = os.getenv('GITLAB_SOURCE_REPO_ID', 3297)
AM_CLUSTER = os.getenv('AM_CLUSTER', 'eus1-platform-poc')
TEST_RUN = os.getenv('TEST_RUN', False)


def mute_to_alertmanager(string_data, cluster):
    alertmanager_url = f"http://alertmanager.{cluster}.internalsephora.com/api/v1/silences"

    headers = {
        "Content-Type": "application/json"
    }

    mute_conf = yaml.safe_load(string_data.decode('utf-8'))

    with open("alert.schema.json") as schema_file:
        schema = json.load(schema_file)
    try:
        if jsonschema.validate(instance=mute_conf, schema=schema) is None:
            print("validation OK")

            for silent in mute_conf.values():
                for definition in silent:
                    alertname = definition.get("alert").get("matchers").get("alertname")
                    namespace = definition.get("alert").get("matchers").get("namespace")
                    app = definition.get("alert").get("matchers").get("app")
                    startsAt = definition.get("alert").get("startsAt")
                    endsAt = definition.get("alert").get("endsAt")
                    comment = definition.get("alert").get("comment")
                    weekdays = definition.get("alert").get("weekday")

                    shour, smin = startsAt.split("-")
                    ehour, emin = endsAt.split("-")
                    today = datetime.date.today()
                    startsAt = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=int(shour),
                                                 minute=int(smin), tzinfo=ZoneInfo("UTC"))
                    endsAt = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=int(ehour),
                                               minute=int(emin), tzinfo=ZoneInfo("UTC"))

                    json_comp = {
                        "id": "",
                        "matchers": [
                            {"name": "alertname", "value": alertname, "isRegex": False, "isEqual": True},
                            {"name": "namespace", "value": namespace, "isRegex": False, "isEqual": True},
                            {"name": "app", "value": app, "isRegex": False, "isEqual": True}
                        ],
                        "startsAt": startsAt.isoformat(),
                        "endsAt": endsAt.isoformat(),
                        "createdBy": "AutomateUser",
                        "comment": comment
                    }

                    weekdays = [int(x) for x in list(weekdays)]
                    if int(today.isoweekday()) in weekdays:
                        if TEST_RUN:
                            print(f"{alertname} was TEST recorded in {cluster}.{namespace}")
                        else:
                            new_sile = requests.post(alertmanager_url, data=json.dumps(json_comp), headers=headers)
                            print(new_sile.json())

    except jsonschema.exceptions.ValidationError:
        print("validation FALSE")


def test_run_check():
    if TEST_RUN:
        global GITLAB_SOURCE_REPO_ID
        GITLAB_SOURCE_REPO_ID = 3297
        global AM_CLUSTER
        AM_CLUSTER = "eus1-platform-poc"
        global GITLAB_BRANCH
        GITLAB_BRANCH = "MSP-1561"


def get_repository_tree(cluster, project):
    root_items = project.repository_tree(all=True, ref=GITLAB_BRANCH)
    root_path = []
    for folder in root_items:
        if folder.get("type") == "tree":
            root_path.append(folder.get("name"))

    for path in root_path:
        env_list = []
        envs = project.repository_tree(path=path, all=True, ref=GITLAB_BRANCH)
        for env in envs:
            if env.get("type") == "tree":
                env_list.append(env.get("name"))
        print(f"folder {path} has {env_list} environments")
        if len(env_list) > 0:
            for envi in env_list:
                print(f"finding file mute.yaml in {path}/{envi}/alerts/mutes/")
                try:
                    file = project.files.get(file_path=f"{path}/{envi}/alerts/mutes/mute.yaml", ref=GITLAB_BRANCH)
                    mute_to_alertmanager(file.decode(), cluster=cluster)
                except gitlab.exceptions.GitlabGetError:
                    print(f"folder {path}/{envi} doesn't contain file")


def gitlab_auth():
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)
    gl.auth()
    return gl.projects.get(int(GITLAB_SOURCE_REPO_ID))


if __name__ == '__main__':

    # id=932 - k8s-state
    # eus1-plavform-poc\applications 3667
    # eus1-omni-devqa\applications 3297
    # eus1-plat-devqa\system 3300

    test_run_check()

    gitlab_project = gitlab_auth()

    get_repository_tree(cluster=AM_CLUSTER, project=gitlab_project)
