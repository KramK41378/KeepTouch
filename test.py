import requests

from models import Message

server_url = 'http://localhost:8080'
print(requests.get(url=server_url).text)
print(requests.get(url=f'{server_url}/get_messages/test').text)
message = Message(
    message='hi',
    sender='me',
    receiver='test',
    key='1488'
)
print(requests.post(url=f'{server_url}/send_message', json=message.model_dump()).text)
