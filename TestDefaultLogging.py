import LoggingModule


if __name__ == "__main__":
    logger = LoggingModule.LoggerFactory.create_logger('my_logger', log_format='text', log_file='app.log')
    thread_safe_logger = LoggingModule.ThreadSafeLogger(logger)

    thread_safe_logger.log(LoggingModule.LogLevel.INFO, 'module1', 'This is an info message.')
    thread_safe_logger.log(LoggingModule.LogLevel.WARNING, 'module2', 'This is a warning message.')
    thread_safe_logger.log(LoggingModule.LogLevel.ERROR, 'module3', 'This is an error message.')