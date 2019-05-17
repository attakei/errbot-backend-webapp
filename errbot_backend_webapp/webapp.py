import logging
from typing import Mapping

from errbot.backends.base import Identifier, Message, ONLINE, Person
from errbot.core import ErrBot

# Import as single file plugin
try:
    import errbot_backend_webapp  # noqa: flake8
except ImportError:
    import sys
    import pathlib
    sys.path.append(str(pathlib.Path(__file__).parents[1]))

from errbot_backend_webapp.config import WebappConfig
from errbot_backend_webapp.server import WebServer

Logger = logging.getLogger(__name__)


class WebappPerson(Person):
    def __init__(self, person, **opts):
        self._person = person
        self._opts = opts

    @property
    def person(self):
        return self._person

    @property
    def client(self):
        return self._person

    @property
    def nick(self):
        return self._person

    @property
    def aclattr(self):
        return ''

    @property
    def fullname(self):
        return self._person

    @property
    def opts(self):
        return self._opts


class WebappMessage(Message):
    def __init__(
            self,
            body: str = '',
            frm: Identifier = None,
            to: Identifier = None,
            parent: 'Message' = None,
            delayed: bool = False,
            partial: bool = False,
            extras: Mapping = None,
            flow=None,
            ):
        super().__init__(body, frm, to, parent, delayed, partial, flow)

    def clone(self):
        return WebappMessage(
            body=self._body,
            frm=self._from,
            to=self._to,
            parent=self._parent,
            delayed=self._delayed,
            partial=self._partial,
            extras=self._extras,
            flow=self._flow,
        )


class WebappBackend(ErrBot):
    """Webapplication backend core class

    Messages is exchanging by WebSocket,
    because response message is possibly to be splitted
    """
    def __init__(self, config):
        super().__init__(config)
        Logger.debug('Initializing Webapp backend')

        if hasattr(self.bot_config, 'BOT_IDENTITY') \
                and 'username' in self.bot_config.BOT_IDENTITY:
            username = self.bot_config.BOT_IDENTITY['username']
            self.bot_identifier = self.build_identifier(username)
        else:
            self.bot_identifier = self.build_identifier('@webmaster')
        self.webapp = None

    def build_identifier(self, text_representation: str) -> Identifier:
        return WebappPerson(text_representation)

    def build_message(
            self, text: str
            ) -> WebappMessage:
        return WebappMessage(text)

    def change_presence(self, status: str = ONLINE, message: str = ''):
        # TODO: Currently, this does not have 'presense'
        pass

    def build_reply(
            self, msg: WebappMessage,
            text: str = None,
            private: bool = False,
            threaded: bool = False) -> WebappMessage:
        reply = self.build_message(text)
        reply.frm = msg.to
        reply.to = msg.frm
        return reply

    @property
    def mode(self):
        return 'webapp'

    @property
    def rooms(self):
        return []

    def query_room(self, room):
        raise ValueError('Room is not implemented')

    def serve_forever(self):
        self.connect_callback()
        config = WebappConfig(self.bot_config)
        self.webapp = WebappConector(self)
        self.webapp.run(config)

    def callback_message(self, msg: WebappMessage):
        super().callback_message(msg)

    def send_message(self, partial_message: WebappMessage):
        """Overrided: after regular process, it send body to WebSocket of user
        """
        super().send_message(partial_message)
        to_: WebappPerson = partial_message.to
        body_ = partial_message.body
        ws_ = to_.opts.get('websocket', False)
        if ws_:
            ws_.send(body_)


class WebappConector(object):
    def __init__(self, errbot: WebappBackend):
        self._errbot = errbot
        self._server = WebServer()

    def run(self, config):
        self._server.configure(handler=self._handle_socket)
        self._server.run(config)

    def _handle_socket(self, ws):
        frm = WebappPerson(
            '@anonymous', websocket=ws)
        while not ws.closed:
            data = ws.receive()
            msg = self._errbot.build_message(data)
            msg.frm = frm
            msg.to = self._errbot.bot_identifier
            self._errbot.callback_message(msg)
