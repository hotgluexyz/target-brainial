import uuid

from target_brainial.client import BrainialSink


class TendersSink(BrainialSink):
    """Sink for the Brainial Tenders stream."""

    name = "tenders"
    endpoint = "tenders/"
    entity = "tender_id"

    def preprocess_record(self, record: dict, context: dict) -> dict:
        return record

    def upsert_record(self, record: dict, context: dict):
        state_dict = {}
        tender_id = record.pop("tender_id", None)

        if tender_id:
            payload = {"tender_update_data": {"id": tender_id, **record}}
            self.request_api("PUT", request_data=payload, endpoint=f"tenders/{tender_id}")
            return tender_id, True, {**state_dict, "is_updated": True}
        else:
            # The API expects a new_tender_id to be provided when creating a new tender
            new_id = str(uuid.uuid4())
            record.setdefault("tender_source", "")
            payload = {"new_tender_id": new_id, **record}
            response = self.request_api("POST", request_data=payload, endpoint="tenders/")
            created_id = response.json().get("tender_id", new_id)
            return created_id, True, state_dict
