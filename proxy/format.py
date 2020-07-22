import yaml
import json

result = {}
parameters = []
request_value = {}


def request_format(body):
    global request_value
    global parameters
    global result

    result = {}
    parameters = []
    request_value = {}

    variables = {}
    process = {}

    request_variables, parameters = content_format(body)

    if parameters:
        parameters = '-'.join(parameters)

    request_variables = yaml.dump(request_variables, allow_unicode=True)
    if '\n' in request_variables:
        request_variables = request_variables.replace('\n', '\n    ').replace('  ', '    ')
        request_variables = request_variables[:request_variables.rindex('\n  ')]

    for i, j in result.items():
        variables_name = i.replace('content.', '').replace('.', '_')
        variables[variables_name] = '$' + variables_name

    variables = yaml.dump(variables, allow_unicode=True)

    if '\n' in variables:
        variables = variables.replace('    ', '').replace('\n', '\n    ')
        variables = variables[:variables.rindex('\n')]

    for i, j in request_value.items():
        process[i] = j

    process = yaml.dump(process, allow_unicode=True)
    if '\n' in process:
        process = process.replace('\n', '\n    ').replace('  ', '    ')
        process = process.replace('- ', '  - ')
        process = process[:process.rindex('\n  ')]
    return variables, request_variables, parameters, request_value, process


def response_format(data):
    global request_value
    global parameters
    global result

    result = {}
    parameters = []
    request_value = {}

    data = json.loads(data)
    content_format(data)

    validate = []

    for i, j in result.items():
        eq = {'eq': []}
        eq['eq'].append(i)
        eq['eq'].append(j)
        validate.append(eq)

    return yaml.dump(validate, allow_unicode=True).replace('\n', '\n        ')


def content_format(data, key=None):

    request_variables = data
    if key:
        name = key
    else:
        name = 'content.'
    for i, j in data.items():
        if isinstance(j, dict):
            content_format(j, name+i+'.')
        else:
            result[name+i] = j
            request_name = name + i
            request_name = request_name.replace('content.', '').replace('.', '_')
            request_value[request_name] = data[i]
            request_variables[i] = '$' + request_name
            parameters.append(request_name)
    return request_variables, parameters
