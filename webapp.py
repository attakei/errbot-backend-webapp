import logging
from pathlib import Path
from typing import Mapping

from errbot.backends.base import Identifier, Message, ONLINE, Person
from errbot.backends.text import TextRoom
from errbot.core import ErrBot
from sanic import Sanic
from sanic.response import text, html


Logger = logging.getLogger(__name__)


class WebappPerson(Person):
    def __init__(self, person):
        self._person = person

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
            req=None,
            ):
        super().__init__(body, frm, to, parent, delayed, partial, flow)
        self.req = req


class WebappBackend(ErrBot):
    """Webapplication backend core class"""
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
        self.webapp_thread = None
        self._rooms = []

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
        reply.req = msg.req
        reply.frm = msg.to
        reply.to = msg.frm
        return reply

    @property
    def mode(self):
        return 'webapp'

    @property
    def rooms(self):
        return self._rooms

    def query_room(self, room):
        if not room.startswith('#'):
            raise ValueError('A Room name must start by #.')
        text_room = TextRoom(room[1:], self)
        if text_room not in self._rooms:
            self._rooms.insert(0, text_room)
        else:
            self._rooms.insert(
                0, self._rooms.pop(self._rooms.index(text_room)))
        return text_room

    def serve_forever(self):
        self.query_room('#testroom').join()
        self.connect_callback()
        self.webapp = WebappServer(self)
        self.webapp.run()

    async def callback_message(self, msg: WebappMessage):
        super().callback_message(msg)

    def send_simple_reply(
            self,
            msg: WebappMessage,
            text: str,
            private=False,
            threaded=False
            ):
        msg.req['errbot_reply'] = text
        super().send_simple_reply(msg, text, private, threaded)


class WebappServer(object):
    def __init__(self, errbot: WebappBackend):
        self._errbot = errbot
        self._static_dir = Path(__file__).parent / 'resources'
        self._app = Sanic(__name__)
        self._app.static('', str(self._static_dir))
        self._app.route('/')(self._get_index)
        self._app.route('/msg', methods=['POST'])(self._post_message)

    def run(self):
        self._app.run()

    async def _get_index(self, request):
        index_html = self._static_dir / 'index.html'
        body = ''
        with index_html.open() as fp:
            body = fp.read()
        return html(body)

    async def _post_message(self, request):
        msg = self._errbot.build_message(request.body.decode())
        msg.frm = self._errbot.build_identifier('@anonymous')
        msg.to = self._errbot.bot_identifier
        msg.req = request
        await self._errbot.callback_message(msg)
        return text(msg.req['errbot_reply'])
