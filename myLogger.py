import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter


handler = RotatingFileHandler(
    "HongikFood.log",
    maxBytes=1000000,
    backupCount=10,
    encoding="utf-8"
)
handler.setFormatter(Formatter(
    u"[%(asctime)s] %(message)s"
))
