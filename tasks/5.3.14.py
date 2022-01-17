import json

import jsonschema
import yaml


def main():
    with open("yaml.yaml", "r") as yaml_file:
        yaml_conf = yaml.safe_load(yaml_file.read())
    print(yaml_conf)

    with open("alertSilence.schema.json") as schema_file:
        schema = json.load(schema_file)

    print(schema)
    if jsonschema.validate(instance=yaml_conf, schema=schema) is None:
        print("validation OK")


if __name__ == '__main__':
    main()
