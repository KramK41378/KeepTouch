import json
from io import TextIOWrapper
from pathlib import Path

from pydantic import BaseModel, Field

from dotenv import load_dotenv

load_dotenv()


class Config(BaseModel):
    name: str = None


def get_readable_config_file() -> TextIOWrapper:
    if not Path('config.json').exists():
        with open('config.json', 'w') as f:
            json.dump({}, f)
    return open('config.json', 'r')

def get_writeable_config_file() -> TextIOWrapper:
    if not Path('config.json').exists():
        with open('config.json', 'w') as f:
            json.dump({}, f)
    return open('config.json', 'w')


def get_config() -> Config:
    try:
        with get_readable_config_file() as config_file:
            config = json.load(config_file)
        return Config(**config)
    except json.decoder.JSONDecodeError:
        return Config()

def get_name() -> str:
    while not (name := input('Введите имя:\n').strip()): ...
    return name


def save_config(config) -> None:
    with get_writeable_config_file() as config_file:
        json.dump(config.model_dump(), config_file)


def setup() -> Config:
    config = get_config()

    if not config.name:
        config.name = get_name()

    save_config(config)
    return config


if __name__ == '__main__':
    print(setup())
