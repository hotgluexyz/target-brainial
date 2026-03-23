import requests

from hotglue_singer_sdk.target_sdk.client import HotglueSink
from hotglue_etl_exceptions import InvalidCredentialsError, InvalidPayloadError


class BrainialSink(HotglueSink):
    """Base sink for Brainial API."""

    @property
    def base_url(self) -> str:
        return "https://app.brainial.com/tender-api/"

    @property
    def default_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.config.get('access_token')}",
        }

    def validate_response(self, response: requests.Response) -> None:
        if response.status_code in [401, 403]:
            raise InvalidCredentialsError(response.text)
        # Brainial API returns 500 for invalid payloads
        elif response.status_code == 500:
            raise InvalidPayloadError(response.text)
        super().validate_response(response)
