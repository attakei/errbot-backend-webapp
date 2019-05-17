"""Backend webserver module
"""
from pathlib import Path

from flask import Flask, request
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from jinja2 import Environment, FileSystemLoader


class WebServer(object):
    def __init__(self):
        self._resources_dir: Path = Path(__file__).parent / 'resources'
        self._app: Flask = Flask(__name__)
        self._sockets: Sockets = Sockets(self._app)

    def configure(self, handler=None):
        self._app.config['SECRET_KEY'] = 'secret'
        self._app.route('/')(self._get_index)
        if handler is None:
            handler = self._sockets_connect
        self._sockets.route('/connect')(handler)

    def run(self, config=None):
        """Run server
        """
        server = pywsgi.WSGIServer(
            (config.host, config.port),
            self._app,
            handler_class=WebSocketHandler)
        server.serve_forever()

    def _get_index(self):
        """Render index document"""
        # TODO: Need performance check
        jinja2_env = Environment(
            loader=FileSystemLoader(str(self._resources_dir)))
        template = jinja2_env.get_template('index.html')
        return template.render({'request': request})

    def _sockets_connect(self, ws):
        while not ws.closed:
            message = ws.receive()
            ws.send(message)


# Trial running endpoint
if __name__ == '__main__':
    web = WebServer()
    web.configure()
    web.run()
