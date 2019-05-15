"""Test case of config set
"""
import pytest

from errbot_backend_webapp.webapp import WebappConfig


@pytest.mark.parametrize(
    'config,key,expected',
    [
        # Defaults
        ({}, 'host', 'localhost'),
        ({}, 'port', 8080),
    ]
)
def test_webapp_config(config, key, expected):
    class Config(object):
        def __init__(self, param):
            for k, v in param.items():
                setattr(self, k, v)
    bot_config = Config(config)
    webapp_config = WebappConfig(bot_config)
    assert getattr(webapp_config, key) == expected
