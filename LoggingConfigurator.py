import logging

_handler = logging.StreamHandler()
_handler.setLevel("DEBUG")
_handler.setFormatter(logging.Formatter("[--%(levelname)s--] %(message)s"))
LOGGER = logging.getLogger("UI_DEBUG")
LOGGER.addHandler(_handler)
LOGGER.setLevel("DEBUG")
