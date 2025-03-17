import LoggingModule
import threading
import time


if __name__ == "__main__":
    print("Start logging from multiple threads")
    logger = LoggingModule.LoggerFactory.create_logger('my_logger', log_format='text', log_file='app.log')
    thread_safe_logger = LoggingModule.ThreadSafeLogger(logger)

    # Создаем несколько потоков
    threads = []
    for i in range(5):  # Создадим 5 потоков
        thread = threading.Thread(target=LoggingModule.log_messages, args=(i, thread_safe_logger))
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()