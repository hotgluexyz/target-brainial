import json
import os

import pytest

from hotglue_singer_sdk.testing import get_standard_target_tests

from target_brainial.target import TargetBrainial

SAMPLE_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../../.secrets/config.json")


@pytest.fixture
def config():
    if not os.path.exists(SAMPLE_CONFIG_PATH):
        pytest.skip("Secrets config not found")
    with open(SAMPLE_CONFIG_PATH) as f:
        return json.load(f)


def get_tests(config):
    return get_standard_target_tests(TargetBrainial, config=config)


def test_standard_target_tests(config):
    tests = get_tests(config)
    for test in tests:
        test()
