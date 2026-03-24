import requests

from hotglue_singer_sdk.target_sdk.client import HotglueSink
from hotglue_etl_exceptions import InvalidCredentialsError, InvalidPayloadError

CLIENTS_URL = "https://app.brainial.com/org/tender_client/"


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
        elif response.status_code in [400, 422, 500]:
            self.logger.error("Invalid payload. Body sent: %s", response.request.body)
            raise InvalidPayloadError(response.text)
        super().validate_response(response)

    def _fetch_clients(self) -> dict:
        """Return a mapping of client name → client id from the Brainial API."""
        response = requests.get(CLIENTS_URL, headers=self.default_headers)
        self.validate_response(response)
        clients = response.json()
        return {c["name"]: c["id"] for c in clients if "name" in c and "id" in c}
