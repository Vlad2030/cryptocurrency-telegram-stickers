import logging
import os

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger: logging.Logger = logging.getLogger(name="main")
logger.setLevel(os.getenv("LOG_LEVEL", "info").upper())
