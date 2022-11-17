import threading

import pyprctl
from injector import inject

from mani.infrastructure.domain.cqrs.bus.asynchronous_bus import AsynchronousBus
from mani.infrastructure.logging.get_logger import get_logger

logger = get_logger(__name__)


@inject
def asynchronous_bus_runner(bus: AsynchronousBus):
    logger.info("Sequential bus runner starting...")
    pyprctl.set_name("Sequential bus runner")
    self = threading.current_thread()
    while getattr(self, "should_be_running", True):
        bus.drain()
    logger.info("Stopping sequential bus runner...")
