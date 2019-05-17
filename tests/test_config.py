"""Test case of config set
"""
import pytest

from errbot_backend_webapp.config import WebappConfig


@pytest.mark.parametrize(
    'config,key,expected',
    [
        # Defaults
        ({}, 'host', 'localhost'),
        ({}, 'port', 8080),
        # Overrides
        ({'host': '0.0.0.0'}, 'host', '0.0.0.0'),
        ({'port': 8081}, 'port', 8081),
    ]
)
def test_webapp_config(config, key, expected):
    class Config(object):
        def __init__(self, param):
            self.BOT_IDENTITY = param

    bot_config = Config(config)
    webapp_config = WebappConfig(bot_config)
    assert getattr(webapp_config, key) == expected
