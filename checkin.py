import os
import requests
import json

def glados():
    cookie = os.environ.get('GLADOS')
    if not cookie:
        return
    try:
        headers = {
            'cookie': cookie,
            'referer': 'https://glados.rocks/console/checkin',
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        }

        checkin_response = requests.post('https://glados.rocks/api/user/checkin', headers={**headers, 'content-type': 'application/json'}, data='{"token":"glados.one"}').json()

        status_response = requests.get('https://glados.rocks/api/user/status', headers=headers).json()

        return [
            'Checkin OK',
            f"{checkin_response['message']}",
            f"Left Days {status_response['data']['leftDays']}",
        ]
    except Exception as error:
        return [
            'Checkin Error',
            f"{error}",
            f"<{os.environ.get('GITHUB_SERVER_URL')}/{os.environ.get('GITHUB_REPOSITORY')}>",
        ]

def notify(contents):
    token = os.environ.get('NOTIFY')
    if not token or not contents:
        return
    requests.post('https://www.pushplus.plus/send', headers={'content-type': 'application/json'}, data=json.dumps({
        'token': token,
        'title': contents[0],
        'content': '<br>'.join(contents[1:]),
        'template': 'markdown',
    }))

def main():
    contents = glados()
    if contents:
        notify(contents)

main()
