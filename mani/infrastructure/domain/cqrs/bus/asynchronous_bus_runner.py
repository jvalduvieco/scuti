import threading

import pyprctl
from injector import inject

from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus
from mani.infrastructure.logging.get_logger import get_logger

logger = get_logger(__name__)


class SequentialBusRunnerThread:
    @inject
    def __init__(self, bus: AsynchronousBus):
        self._bus = bus
        self._should_be_running = False

    def run(self):
        self._should_be_running = True
        logger.info("Sequential bus runner starting...")
        pyprctl.set_name("Sequential bus runner")
        while self._should_be_running:
            self._bus.drain(block=True)
        logger.info("Stopping sequential bus runner...")

    def stop(self):
        logger.info("Sequential bus runner stop requested...")
        self._should_be_running = False
        self._bus.wake_up()

