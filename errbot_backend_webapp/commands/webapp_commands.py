import logging

from errbot import BotPlugin, botcmd


Logger = logging.getLogger(__name__)


class WebappCommands(BotPlugin):
    def activate(self):
        """Activate only in Webapp backend
        """
        if self.mode != 'webapp':
            Logger.debug('Auto disable in not Webapp backend')
            return
        super().activate()

    @botcmd
    def asadmin(self, msg, _):
        """Change privileged user
        """
        self._bot.user = self.build_identifier(self.bot_config.BOT_ADMINS[0])
        return f'You are now an admin: {self._bot.user}.'

    @botcmd
    def asuser(self, msg, args):
        """Change specified user(default: anonymous)
        """
        if args:
            usr = args
            if usr[0] != '@':
                usr = '@' + usr
            self._bot.user = self.build_identifier(usr)
        else:
            self._bot.user = self.build_identifier('@anonymous')
        return f'You are now: {self._bot.user}.'
