from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model

from system.infrastructure.enums.environment_enum import Environments
from system.infrastructure.settings.config import Config


class BaseModel(Model):
    class Meta:
        table_name = Config.DATABASE.TABLE
        if Config.ENVIRONMENT == Environments.LOCAL.value:
            host = Config.DATABASE.ENDPOINT_URL
        region = Config.CLOUD_CREDENTIALS.AWS_DEFAULT_REGION
        aws_credentials_access_key_id = Config.CLOUD_CREDENTIALS.AWS_ACCESS_KEY_ID
        aws_credentials_access_key = Config.CLOUD_CREDENTIALS.AWS_SECRET_ACCESS_KEY

    pk = UnicodeAttribute(hash_key=True)
    sk = UnicodeAttribute(range_key=True)
