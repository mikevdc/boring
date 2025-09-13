import configparser
import json
import os
import logging

from pathlib import Path


class Configuration:

    @classmethod
    def get(cls):
        if not hasattr(cls, 'instance'):
            config = configparser.ConfigParser()
            dir_path = Path('scripts') / 'config'

            config_path = dir_path / 'config.properties'
            config.read(str(config_path))
            cls.instance = config
            logging.info("Cargando configuración")
        return cls.instance


def get_env() -> str:
    """
    Returns the current environment: DEV, INT or PROD
    Default: DEV
    """

    config = Configuration.get()
    env_var_name = config["ENV"]["env_var_name"]

    env = os.getenv(env_var_name, "PROD").upper()
    if env not in ("DEV", "INT", "PROD"):
        raise ValueError(f"Invalid environment variable '{env_var_name}': {env}")
    return env


def load_logging_config():
    """
    Loads the logging configuration corresponding to the current environment
    """
    env = get_env()

    config = Configuration.get()
    file_name = config["LOGS"]["logging_config"]

    env_file_name = f"{file_name}.{env.lower()}.json"
    file_path = Path(env_file_name)

    if not file_path.exists():
        raise FileNotFoundError(f"Config file not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
