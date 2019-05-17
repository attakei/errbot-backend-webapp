class WebappConfig(object):
    """Webapp server configuration
    """
    def __init__(self, bot_config):
        conf = getattr(bot_config, 'BOT_IDENTITY', {})
        self.host: str = conf.get('host', 'localhost')
        """Listen host"""
        self.port: int = conf.get('port', 8080)
        """Listen port"""
