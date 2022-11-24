from injector import inject

from scuti.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus
from scuti.infrastructure.logging.get_logger import get_logger
from scuti.infrastructure.threading.thread import Thread

logger = get_logger(__name__)


class AsynchronousBusRunner(Thread):
    @inject
    def __init__(self, bus: AsynchronousBus):
        super().__init__()
        self._bus = bus

    def get_name(self):
        return "Asynchronous bus runner"

    def execute(self):
        logger.info("Starting asynchronous bus runner...")
        while not (self._bus.is_empty() and self.should_stop()):
            self._bus.drain(block=True)
        logger.info("Stopping asynchronous bus runner...")

    def wants_to_stop(self):
        self._bus.shutdown()
