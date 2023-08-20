import os

import boto3

from system.infrastructure.enums.environment_enum import Environments


class AWSCredentials:
    SESSION = boto3.Session()
    CREDENTIALS = SESSION.get_credentials()
    FROZEN_CREDENTIALS = CREDENTIALS.get_frozen_credentials()
    AWS_ACCESS_KEY_ID = FROZEN_CREDENTIALS.access_key
    AWS_SECRET_ACCESS_KEY = FROZEN_CREDENTIALS.secret_key
    AWS_DEFAULT_REGION = SESSION.region_name


class DataBaseConfiguration:
    ENDPOINT_URL = os.getenv("ENDPOINT_URL", "http://localhost:8000")
    TABLE = os.getenv("DATABASE_TABLE", "shorturl")


class ElasticSearchConfig:
    HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")
    PORT = os.getenv("ELASTICSEARCH_PORT", "9200")
    INDEX = os.getenv("ELASTICSEARCH_INDEX", "local_index")
    ACTIVE = os.getenv("ELASTICSEARCH_ACTIVE", "false") == "true"


class Logger:
    CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "short-url": {"handlers": ["default"], "level": "DEBUG"},
        },
    }


class Config:
    DATABASE = DataBaseConfiguration
    CLOUD_CREDENTIALS = AWSCredentials
    ENVIRONMENT = Environments(os.getenv("ENVIRONMENT", "local")).value
    LOGGER = Logger
    ELASTIC = ElasticSearchConfig
