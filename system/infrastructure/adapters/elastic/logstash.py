import logging

from logstash import TCPLogstashHandler

from system.infrastructure.settings.config import Config


class LogStash:
    logger = None
    app_name = Config.LOG_STASH.APP_NAME
    host = Config.LOG_STASH.LOGSTASH_HOST
    port = Config.LOG_STASH.LOGSTASH_PORT
    db_path = Config.LOG_STASH.DATABASE_PATH

    def logstash_init(
        self,
        loggername: str = Config.APPLICATION_NAME,
    ) -> logging.Logger:
        if self.logger is None:
            self.logger = logging.getLogger(loggername)
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(
                TCPLogstashHandler(
                    host=self.host,
                    port=self.port,
                    version=1,
                ),
            )

        return self.logger
