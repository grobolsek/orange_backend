from itertools import cycle
from collections import defaultdict

import Orange
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

datasets_info: dict = dict(Orange.datasets.items())


def convert_data(name: str) -> dict[str: dict]:
    """
    :param name: name of dataset file (.tab)
    :return: dict of all elements
    """
    variables = cycle([x.name for x in Orange.data.Table(name).domain.variables])
    # compare i == i because json doesn't support nan and Math.isnan doesn't work if there is a str
    # todo: fix (breaks on heart_disease)
    data_table = {
        element[-1].value:
            {next(variables): i if i == i else None for i in element.list[:-1]} for element in Orange.data.Table(name)
    }
    return data_table


def get_values(keys: list) -> dict[str: list]:
    """
    :param keys: list of keys
    :return: values of keys
    """
    values = defaultdict(set)
    for i in datasets_info.values():
        for key, value in i.items():
            if type(value) is dict:
                for k, v in value.items():
                    if k in keys:
                        values[k].add(v)
            elif key in keys:
                values[key].add(value)

    return {key: list(value) for key, value in values.items()}


@app.route('/datasets/get')
def datasets_api():
    return {'/info': 'returns values for all available datasets',
            '/info/name': 'returns info for this specific dataset',
            '/data/name': 'returns data for this specific dataset',
            }


@app.route('/datasets/get/info/')
def datasets_api_info():
    return datasets_info


@app.route('/datasets/get/info/values/<string:keys>')
def datasets_api_info_values(keys):
    try:
        return get_values(keys.split(";"))
    except ValueError:
        return {'Error': 'No values found for given keys.'}


@app.route('/datasets/get/data/<string:name>')
def datasets_api_data(name):
    try:
        return convert_data(name)

    except KeyError as e:
        return {'KeyError': str(e)}


@app.route('/datasets/remove/<dataset_name>', methods=['DELETE'])
def remove_dataset(dataset_name):
    # todo: code for removing
    return {"message": f"Dataset '{dataset_name}' has been deleted successfully."}, 200
    pass


@app.route('/datasets/edit/<dataset_name>', methods=['DELETE'])
def edit_dataset(dataset_name):
    # todo: code for changing
    pass


if __name__ == '__main__':
    app.run()
