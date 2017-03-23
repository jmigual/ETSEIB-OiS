import logging


def configure_default_logger():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    formatter = logging.Formatter("[{asctime}s] ({levelname}) {message}", style="{")
    handler_s = logging.StreamHandler()
    handler_f = logging.FileHandler("info.log")
    handler_s.setFormatter(formatter)
    handler_f.setFormatter(formatter)
    log.addHandler(handler_s)
    log.addHandler(handler_f)

configure_default_logger()
