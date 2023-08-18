from pynamodb.models import Model

from system.infrastructure.enums.environment_enum import Environments
from system.infrastructure.settings.config import Config


class NoSqlAdapter(Model):
    class Meta:
        table_name = Config.DATABASE.TABLE
        if Config.ENVIRONMENT == Environments.LOCAL.value:
            host = Config.DYNAMODB.DYNAMODB_ENDPOINT_URL
        region = Config.INTERNAL_AWS_CREDENTIALS.AWS_DEFAULT_REGION
        aws_credentials_access_key_id = Config.CLOUD_CREDENTIALS.AWS_ACCESS_KEY_ID
        aws_credentials_access_key = Config.CLOUD_CREDENTIALS.AWS_SECRET_ACCESS_KEY
