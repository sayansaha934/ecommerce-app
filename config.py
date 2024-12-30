import json
from pydantic import BaseModel


class Config(BaseModel):
    DATABASE_URL: str



def get_config():
    with open("env.json") as json_env_file:
        env_config = json.load(json_env_file)
    config_data = Config(**env_config)
    return config_data


config: Config = get_config()
