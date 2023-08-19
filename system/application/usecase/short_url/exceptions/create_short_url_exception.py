class NoURLWasFoundError(Exception):
    def __init__(
        self, message: str = "The Short Url requested does not exists", *args: object
    ):  # noqa: WPS612
        self.message = message
        super().__init__(message, *args)
