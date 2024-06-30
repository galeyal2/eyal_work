import logging
import sys


class SingletonLoggerMeta(type):
    _instances = {}

    def __call__(cls, name, *args, **kwargs):
        if name not in cls._instances:
            cls._instances[name] = super().__call__(name, *args, **kwargs)
        return cls._instances[name]


class MyLogger():
    def __init__(self, name="Orca", level="INFO"):
        self.name = name
        self.level = level
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        self.logger.addHandler(console_handler)
        console_handler.setFormatter(formatter)

name = "orca"
orca: MyLogger = MyLogger(name, "INFO")
orca_logger = orca.logger
orca_logger.info(f"logger has started as {name}")

import logging

def print_all_loggers():
    print("All loggers:")
    for logger_name in logging.Logger.manager.loggerDict.keys():
        print(logger_name)

print_all_loggers()
