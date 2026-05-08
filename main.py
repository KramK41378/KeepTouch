import datetime

from flask import Flask, jsonify
from pydantic import BaseModel

app = Flask(__name__)

class Md(BaseModel):
    time: datetime.datetime

@app.route('/')
def index():
    return (Md(time=datetime.datetime.now()).model_dump_json())

if __name__ == '__main__':
    app.run()