import json


def demo(response, id):

    r = json.loads(response.text)
    news = {
        '10001': 'This is a test',
        '10002': 'This is a test2',
        '10003': 'This is a test3'
    }
    assert (news[id] == r['context']), id

