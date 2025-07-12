import json
from http.client import responses

import requests

# host = 'http://127.0.0.1:8000/api/chat/stream'
host = 'http://127.0.0.1:8000/api/create_conversation'
headers = {
    'Content-Type': 'application/json',
    "Authorization": 'Bearer pat_DmDqOVnk7IXzEJTL1hel93xKkxYzgu7jabvRnpH9VMl3CCrs3jwX2Wqi8WDudn3d',
}
data = {
    # 'user_id':'1',
    # 'content':'你好！'
    'bot_id':'7522105808012869642',
}
# responses = requests.post(host, headers=headers, data=json.dumps(data))
responses = requests.post(host, headers=headers)
# print(responses.text, end='', flush=True)
print(responses.text)