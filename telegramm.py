import requests
import os
from dotenv import load_dotenv

load_dotenv()
ENV = dict(os.environ)
BOT_TOKEN = ENV["BOT_TOKEN"]
CHAT_ID = ENV["CHAT_ID"]


# ID чата, куда нужно отправить фото (можно получить с помощью getUpdates)



# URL метода sendPhoto API Telegram
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

FILE_TYPES = {
    "jpg": "photo",
    "png": "photo",
    "mp4": "video",
    "txt": "document",
    "pdf": "document",
}

TELEGRAMM_METOD = {
    "jpg": "sendPhoto",
    "png": "sendPhoto",
    "mp4": "sendVideo",
    "txt": "sendDocument",
    "pdf": "sendDocument",
}

    
class Telegramm:   
    
    def _send_message(self, message):
        # в   начале префикс b  - убираем
        message = message[2:].replace("'",'')
        payload = {
           "chat_id": CHAT_ID,
            "text": message
        }
        response = requests.post(
                            URL +"sendMessage",
                            json=payload,
                            timeout=1000
                        )
        return response

    def send_photo(self, path_to_extract: str, list_photos=None):
        if list_photos is not None:
            for file_path in list_photos:
                try:
                    with open(os.path.join(path_to_extract, file_path), "rb") as photo:
                        if file_path[-3:] == 'txt':
                            response = self._send_message(str(photo.read()))
                        else:
                            response = requests.post(
                                URL + TELEGRAMM_METOD[file_path[-3:]],
                                data={"chat_id": CHAT_ID},
                                files={FILE_TYPES[file_path[-3:]]: photo},
                                timeout=1000,
                            )
                        # Проверка результата
                        if response.status_code == 200:
                            print("Файл успешно отправлен!")
                        else:
                            print(
                                f"Ошибка: {response.status_code},\
                                  {response.text}"
                            )
                except Exception as e:
                    print(f"Что-то случилось!: {e}")
