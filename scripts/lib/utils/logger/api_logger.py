import logging
import sys
import threading

from concurrent_log_handler import ConcurrentTimedRotatingFileHandler
from loguru import logger
from pathlib import Path
from scripts.lib.utils.configuration import load_logging_config
from scripts.lib.utils.logger.request_context import request_id_ctx


# class for redirect standard logs to Loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = logger.level(record.levelname).name if record.levelname in logger._core.levels else record.levelno
        service = record.name
        get_logger(service).opt(depth=6, exception=record.exc_info).log(level, record.getMessage())


def formatter(format):
    def real_formatter(record):
        record["extra"]["request_id"] = request_id_ctx.get()
        record["extra"]["thread_name"] = threading.current_thread().name
        return format
    return real_formatter
  

def logging_setup():

    # Remove previous sinks
    logger.remove()

    logging_config = load_logging_config()

    ignored_services = logging_config["ignored-services"]
    intercepted_loggers = logging_config["intercepted-loggers"]

    # Generate sinks from config file
    for sink in logging_config["sinks"]:

        # Get sink's configurations

        type = sink["type"]

        if type == "file":
            rotation = sink.get("rotation", {})
            path=sink["path"]
            handler = ConcurrentTimedRotatingFileHandler(
                filename=path,
                when=rotation.get("when", "midnight"),
                interval=rotation.get("interval", 1),
                backupCount=rotation.get("backupCount", 7),
                maxBytes=rotation.get("maxBytes", None),
                use_gzip=rotation.get("use_gzip", True),
                encoding=rotation.get("encoding", "utf-8")
            )
            
            # Create, if not exists, the directory where sink's logs will be saved
            dir = path.split("/")[:-1] # Remove the filename from the full path
            Path(*dir).mkdir(parents=True, exist_ok=True)            

        elif type == "console":
            handler = sys.stdout

        # Set sink's logs format
        fmt = sink.get("format")
        format = formatter(fmt)

        general = sink.get("general", False)
        name = sink.get("name", "")

        if general:
            filter = lambda record, ignored=ignored_services: record["extra"].get("service") not in ignored
        else:
            filter = lambda record, srv = name: record["extra"].get("service") == srv

        lvl = sink.get("level", "INFO")
        colorize = sink.get("colorize", False)

        logger.add(
            sink=handler,
            level=lvl,
            colorize=colorize,
            format=format,
            filter=filter
        )

    # Intercept loggers from Uvicorn
    for logger_name in intercepted_loggers:
        log = logging.getLogger(logger_name)
        log.handlers = [InterceptHandler()]
        log.propagate = False
        

def get_logger(service: str):
    return logger.bind(service=service)