from collections import defaultdict
from itertools import cycle

import Orange
import re
from flask import Flask

app = Flask(__name__)

datasets_info: dict = dict(Orange.datasets.items())


def convert_data(name: str) -> dict[str: dict[str: str | int]]:
    """
    :param name: name of dataset file (.tab)
    :return: dict of all elements
    """
    variables = cycle([x.name for x in Orange.data.Table(name).domain.variables])
    data_table = {
        element[-1].value: {next(variables): i for i in element.list[:-1]} for element in Orange.data.Table(name)
    }
    return data_table


print(convert_data('zoo'))


@app.route('/datasets-api')
def datasets_api():
    return {'/info': 'returns values for all available datasets',
            '/info/name': 'returns info for this specific dataset',
            '/data/name': 'returns data for this specific dataset',
            }


@app.route('/datasets-api/info/')
def datasets_api_info():
    return datasets_info


@app.route('/datasets-api/info/<string:name>')
def datasets_api_info_name(name):
    try:
        return datasets_info[name]

    except KeyError as e:
        return {'KeyError': str(e)}


@app.route('/datasets-api/data/<string:name>')
def datasets_api_data(name):
    try:
        if re.search(r'\.(tab|dst)$', name):
            return convert_data(name)

        file: str = datasets_info[name]['location']
        return convert_data(name)

    except KeyError as e:
        return {'KeyError': str(e)}


if __name__ == '__main__':
    app.run()
