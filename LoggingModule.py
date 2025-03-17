import logging
import logging.handlers
import xml.etree.ElementTree as ET
from datetime import datetime
import threading
import time

class LogLevel:
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

class LogFormatter(logging.Formatter):
    def format(self, record):
        raise NotImplementedError

class TextLogFormatter(LogFormatter):
    def format(self, record):
        log_message = f"{record.levelname} | {record.module} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {record.getMessage()}"
        return log_message

class XMLLogFormatter(LogFormatter):
    def format(self, record):
        log_entry = ET.Element('log_entry')
        level = ET.SubElement(log_entry, 'level')
        level.text = record.levelname
        module = ET.SubElement(log_entry, 'module')
        module.text = record.module
        timestamp = ET.SubElement(log_entry, 'timestamp')
        timestamp.text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = ET.SubElement(log_entry, 'message')
        message.text = record.getMessage()
        return ET.tostring(log_entry, encoding='unicode')

class LoggerFactory:
    @staticmethod
    def create_logger(name, log_format='text', log_file=None):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = TextLogFormatter() if log_format == 'text' else XMLLogFormatter()
        handler = logging.StreamHandler() if log_file is None else logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

# Потокобезопасный логгер
class ThreadSafeLogger:
    def __init__(self, logger):
        self.logger = logger
        self.lock = threading.Lock()

    def log(self, level, source, message):
        with self.lock:
            extra = {'source': source}
            if level == LogLevel.INFO:
                self.logger.info(message, extra=extra)
            elif level == LogLevel.WARNING:
                self.logger.warning(message, extra=extra)
            elif level == LogLevel.ERROR:
                self.logger.error(message, extra=extra)

def log_messages(thread_id, logger):
    for i in range(5):
        message = f"Message {i} from thread {thread_id}"
        logger.log(LogLevel.INFO, f"thread_{thread_id}", message)
        time.sleep(0.1)