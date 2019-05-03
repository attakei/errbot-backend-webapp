import asyncio
import logging
from pathlib import Path
from queue import Queue
from typing import Mapping

from errbot.backends.base import Identifier, Message, ONLINE, Person
from errbot.backends.text import TextRoom
from errbot.core import ErrBot
from sanic import Sanic
from sanic.response import html
from sanic.websocket import WebSocketProtocol


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

    def callback_message(self, msg: WebappMessage):
        super().callback_message(msg)

    def send_message(self, partial_message: WebappMessage):
        super().send_message(partial_message)
        to_: WebappPerson = partial_message.to
        body_ = partial_message.body
        ws_ = to_.opts.get('websocket', False)
        if ws_:
            self.webapp._queue.put(ws_.send(body_))


class WebappServer(object):
    def __init__(self, errbot: WebappBackend):
        self._errbot = errbot
        self._static_dir = Path(__file__).parent / 'resources'
        self._queue = Queue()
        self._app = Sanic(__name__)
        self._app.static('', str(self._static_dir))
        self._app.route('/')(self._get_index)
        self._app.websocket('/connect')(self._handle_socket)
        self._app.add_task(self._process_queue)

    def run(self):
        self._app.run(protocol=WebSocketProtocol)

    async def _process_queue(self):
        while True:
            if self._queue.empty():
                await asyncio.sleep(1)
                continue
            while not self._queue.empty():
                await self._queue.get()

    async def _get_index(self, request):
        index_html = self._static_dir / 'index.html'
        body = ''
        with index_html.open() as fp:
            body = fp.read()
        return html(body)

    async def _handle_socket(self, request, ws):
        frm = WebappPerson(
            '@anonymous', websocket=ws)
        while True:
            data = await ws.recv()
            msg = self._errbot.build_message(data)
            msg.frm = frm
            msg.to = self._errbot.bot_identifier
            self._errbot.callback_message(msg)
