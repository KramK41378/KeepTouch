from hashlib import _Hash
from pydantic import BaseModel


class Message(BaseModel):
    message: str
    sender: str
    receiver: str
    key: _Hash