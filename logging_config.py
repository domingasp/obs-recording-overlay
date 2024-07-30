import logging


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    logFormatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s"
    )
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler("logfile.log")
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
