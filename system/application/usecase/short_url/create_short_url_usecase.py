from system.application.dto.api.requests.url_request import NewShortUrlRequest
from system.domain.ports.repositories.use_case_port import RequestUseCase


class CreateShortUrlUseCase(RequestUseCase[NewShortUrlRequest]):
    def execute(self, payload: NewShortUrlRequest) -> NewShortUrlRequest:
        raise Exception(payload)
