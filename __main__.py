from services import LoadZip
from services import Telegramm
import os
import time
from dotenv import load_dotenv
from loguru import logger

LOG_FILE = os.path.join("logs", "app.log")
os.makedirs("logs", exist_ok=True)


logger.add(LOG_FILE, rotation="2 days")


BASE_URL = ""
PUBLIC_KEY = ""
PATH_TO_EXTRACT = ""
ZIP_FILE = ""
SLEEP_TIME = 100


@logger.catch
def init_env():
    """Инициализируем загрузку переменных окружения"""
    global BASE_URL
    global PUBLIC_KEY
    global PATH_TO_EXTRACT
    global ZIP_FILE
    global SLEEP_TIME



    try:
        load_dotenv()
        logger.debug("loading .env environment variables")
        env = dict(os.environ)
        BASE_URL = env["BASE_URL"]
        PUBLIC_KEY = env["PUBLIC_KEY"]
        PATH_TO_EXTRACT = env["PATH_TO_EXTRACT"]
        ZIP_FILE = env["ZIP_FILE"]  # название ZIP файла для временного хранения
        SLEEP_TIME = int(env["SLEEP_TIME"])

    except KeyError:
        logger.error("Не загружен .env! или переменная выходим.")
        exit(0)


if __name__ == "__main__":

    init_env()
    logger.info("Start main module")
    telegramm = Telegramm()

    while True:
        try:
            init_env()
            logger.info("Try to load zip from YD")
            zip_file = LoadZip(BASE_URL, PUBLIC_KEY)  # инициализируем
            if not zip_file.load_zip_file(PATH_TO_EXTRACT, ZIP_FILE):
                logger.info(f"nothing new - sleep & pass for {SLEEP_TIME}s")
                time.sleep(SLEEP_TIME)
                continue
            list_for_send = zip_file.extract_zip()
            if list_for_send:
                print(f"files for send: {list_for_send}")
                logger.info("new files found - Send to telegram")
                telegramm.send_data(PATH_TO_EXTRACT, list_for_send)
            else:
                # print('нет изменений!')
                logger.info("Нет обновления на YD")
            # exit(9)
            # time.sleep(SLEEP_TIME)
        except Exception as e:
            logger.error(f"Bad thing happen: {e}")
            exit(0)
        except KeyboardInterrupt:
            logger.warning('Ползьзователь попросил выйти')
            exit(0)