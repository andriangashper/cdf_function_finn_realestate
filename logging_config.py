import logging

def configure_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(stream_handler)
    
    return logger