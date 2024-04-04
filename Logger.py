import logging

logging.basicConfig(filename='error.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def log_message(message, level=logging.INFO):
    try:
        if level == logging.INFO:
            logging.info(message)
        elif level == logging.ERROR:
            logging.error(message)
        elif level == logging.CRITICAL:
            logging.critical(message)
    except Exception as e:
        print(f"Error occurred while logging: {str(e)}")


def configure_logging(filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'):
    logging.basicConfig(filename=filename, level=level, format=format)
