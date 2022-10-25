import logging

import socketio
from flask import Flask

from mani.infrastructure.logging.get_logger import get_logger


def create_socketio_app(app: Flask) -> socketio.Server:
    socketio_logger = get_logger("werkzeug")
    engineio_logger = get_logger("engineio")
    get_logger("socketio").setLevel(logging.ERROR)
    engineio_logger.disabled = True
    socketio_logger.disabled = True
    sio = socketio.Server(async_mode="threading", cors_allowed_origins="*", logger=socketio_logger,
                          engineio_logger=engineio_logger)
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
    return sio
