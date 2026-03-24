import uuid
from typing import Dict, List, Optional

from hotglue_etl_exceptions import InvalidPayloadError
from hotglue_singer_sdk.target_sdk.client import PluginBase

from target_brainial.client import BrainialSink


class TendersSink(BrainialSink):
    """Sink for the Brainial Tenders stream."""

    name = "tenders"
    endpoint = "tenders/"
    entity = "tender_id"

    def __init__(
        self,
        target: PluginBase,
        stream_name: str,
        schema: Dict,
        key_properties: Optional[List[str]],
    ) -> None:
        super().__init__(target, stream_name, schema, key_properties)
        self._clients_by_name = self._fetch_clients()

    def preprocess_record(self, record: dict, context: dict) -> dict:
        client_name = record.pop("client_name", None)
        if client_name:
            client_id = self._clients_by_name.get(client_name)
            if not client_id:
                raise InvalidPayloadError(f"Client not found: '{client_name}'")
            record["tender_client"] = client_id
        return record

    def upsert_record(self, record: dict, context: dict):
        state_dict = {}
        tender_id = record.pop("tender_id", None)

        if tender_id:
            payload = {"tender_update_data": {"id": tender_id, **record}}
            self.request_api("PUT", request_data=payload, endpoint=f"tenders/{tender_id}")
            return tender_id, True, {**state_dict, "is_updated": True}
        else:
            payload = dict(record)
            # The API expects a new_tender_id to be provided when creating a new tender
            if "new_tender_id" not in payload:
                payload["new_tender_id"] = str(uuid.uuid4())
            response = self.request_api("POST", request_data=payload, endpoint="tenders/")
            created_id = response.json().get("tender_id", payload["new_tender_id"])
            return created_id, True, state_dict
