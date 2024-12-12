import logging
from dotenv import load_dotenv
import os
from typing import Literal
import sys

load_dotenv()
LOG_DIR = ""
LOG_FILE_NAME = ""

try:
    LOG_DIR = dict(os.environ)['LOG_DIR']
except KeyError:
    print('.env не найден или LOG_DIR в ней, выходим')
    sys.exit(0)

LOG_FILE_NAME = os.path.join(LOG_DIR,dict(os.environ)['LOG_FILE'])
#  создаем если не было
os.makedirs(LOG_DIR, exist_ok=True)


# Настройка логирования
def init_logging(log_level:Literal["CRITICAL",
                                   "FATAL",
                                   "ERROR",
                                   "WARN",
                                   "INFO",
                                   "DEBUG",
                                   "NOTSET"]='INFO', 
                stream_on=True,
                name =__name__
                )->logging.Logger:
    """init log level from logging:
    CRITICAL = 50,        
    FATAL = CRITICAL,
    ERROR = 40,
    WARNING = 30,
    WARN = WARNING,
    INFO = 20,
    DEBUG = 10,
    NOTSET = 0,
    
    Args:
        log_level (int): logging.level
        stream_on(bool):True  - enable streaming to console
    """
    

    
    handlers = [logging.FileHandler(LOG_FILE_NAME), # Запись логов в файл
    ]
    if stream_on:
        handlers.append(                   
                logging.StreamHandler()  # Вывод логов в консоль
        )
    level_choose_dict = {"CRITICAL":logging.CRITICAL,
            'FATAL' : logging.FATAL,
            'ERROR' : logging.ERROR,
            'WARNING': logging.WARNING,
            'WARN' : logging.WARN,
            'INFO' : logging.INFO,
            'DEBUG' : logging.DEBUG,
            'NOTSET' : logging.NOTSET,                
        }
    logging.basicConfig(
    level=level_choose_dict[log_level],  # Уровень логирования: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат сообщения
    handlers=handlers
    )
    return logging.getLogger(name)


if __name__ == '__main__':
    logger = init_logging('DEBUG')
    logger.debug('test')
