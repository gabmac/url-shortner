class HTTPPrefixNeededUseCase:
    def _https_prefix(self, target_url: str) -> str:
        if not (
            target_url.startswith(r"https://") or target_url.startswith(r"http://")
        ):
            target_url = rf"https://{target_url}"

        return target_url
