"""Brainial target class."""

from hotglue_singer_sdk import typing as th
from hotglue_singer_sdk.target_sdk.client import HotglueSink
from hotglue_singer_sdk.target_sdk.target import TargetHotglue
from hotglue_singer_sdk.helpers.capabilities import AlertingLevel
from typing import Type

from target_brainial.sinks import TendersSink


class TargetBrainial(TargetHotglue):
    """Singer target for Brainial."""

    SINK_TYPES = [
        TendersSink,
    ]
    name = "target-brainial"
    alerting_level = AlertingLevel.ERROR

    config_jsonschema = th.PropertiesList(
        th.Property("access_token", th.StringType, required=True),
    ).to_dict()

    def get_sink_class(self, stream_name: str) -> Type[HotglueSink]:
        sink = super().get_sink_class(stream_name)
        return sink if sink else TendersSink


if __name__ == "__main__":
    TargetBrainial.cli()
