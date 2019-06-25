import logging

from errbot import BotPlugin, botcmd


Logger = logging.getLogger(__name__)


class WebappCommands(BotPlugin):
    def activate(self):

        # This won't activate the plugin in anything else than text mode.

        if self.mode != 'webapp':
            Logger.debug('Auto disable in not Webapp backend')
            return

        super().activate()

    @botcmd
    def asadmin(self, msg, _):
        return 'Try changing admin'
