from loadzip import LoadZip
from telegramm import Telegramm
import os
import time
from dotenv import load_dotenv
from logger import init_logging

logger = init_logging('DEBUG',name ='main.py')
logger.info("Start main module")

load_dotenv()
logger.debug('loading .env environment variables')
ENV = dict(os.environ)
BASE_URL = ENV["BASE_URL"]
PUBLIC_KEY = ENV["PUBLIC_KEY"]
PATH_TO_EXTRACT = ENV["PATH_TO_EXTRACT"]
ZIP_FILE = ENV["ZIP_FILE"]  # название ZIP файла для временного хранения


telegramm = Telegramm()

if __name__ == "__main__":
    while True:
        logger.info("Try to load zip from YD")
        zip_file = LoadZip(BASE_URL, PUBLIC_KEY)  # инициализируем
        if not zip_file.load_zip_file(PATH_TO_EXTRACT, ZIP_FILE):
            logger.debug('nothing new - sleep & pass')
            time.sleep(150)
            continue
        list_for_send = zip_file.extract_zip()
        if list_for_send:
            print(f"files for send: {list_for_send}")
            logger.info('new files found - Send to telegram')
            telegramm.send_data(PATH_TO_EXTRACT, list_for_send)
        else:
            # print('нет изменений!')
            logger.info('Нет обновления на YD')
        # exit(9)
    # time.sleep(150)
