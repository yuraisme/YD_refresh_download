import requests
import os
from dotenv import load_dotenv
from logger import init_logging

load_dotenv()

ENV = dict(os.environ)
BOT_TOKEN = ENV["BOT_TOKEN"]
CHAT_ID = ENV["CHAT_ID"]


logger = init_logging('DEBUG',name ='telegramm.py')
logger.info("Start module telegramm message send")

# URL метода sendPhoto API Telegram
API_URL= f"https://api.telegram.org/bot{BOT_TOKEN}/"


FILE_TYPES = { # для расшифровки, чего посылаем-то -добавляем в конце API_URL
    "jpg": "photo",     
    "png": "photo",
    "mp4": "video",
    "txt": "document",
    "pdf": "document",
}

TELEGRAMM_METOD_TELEGRAM = {
    "jpg": "sendPhoto",
    "png": "sendPhoto",
    "mp4": "sendVideo",
    "txt": "sendDocument",
    "pdf": "sendDocument",
}
class Telegramm:     
    def _send_message(self, message):
        # в   начале префикс b  - убираем и кавычки -тоже
        message = message[2:].replace("'",'')
        payload = {
           "chat_id": CHAT_ID,
            "text": message
        }
        response = requests.post(API_URL +"sendMessage",
                            json=payload,
                            timeout=1000
                        )
        return response

    def send_data(self, path_to_extract: str, list_files=None):
        if list_files is not None and path_to_extract !="":
            for file_path in list_files:
                try: #смотрим - текстовый или бинарный файл к нам попал
                    logger.debug("what kind file need to send: %s", file_path)
                    file_ext = file_path[-3:]
                    with open(os.path.join(path_to_extract, file_path), "rb") as photo:
                        if file_ext == 'txt':
                            logger.debug("sending message to telegrmm")
                            response = self._send_message(str(photo.read()))
                        else:
                            logger.debug("sending binary file to telegrmm")
                            response = requests.post(
                                API_URL + TELEGRAMM_METOD_TELEGRAM[file_ext],
                                data={"chat_id": CHAT_ID},
                                files={FILE_TYPES[file_ext]: photo},
                                timeout=1000,
                            )
                        # Проверка результата
                        if response.status_code == 200:
                            logger.info("File %s succefully send", file_path)
                            print("Файл успешно отправлен!")
                        else:
                            logger.error("Error %s",response.text)
                            print(
                                f"Ошибка: {response.status_code},\
                                  {response.text}"
                            )
                except Exception as e:
                    logger.error("Error %s", e)
                    print(f"Что-то случилось!: {e}")
