import requests
import os

# Токен вашего бота
BOT_TOKEN = "7693612461:AAFvWVYCsRKW_zghpGcN0jDKHq6BC0BxAjA"

# ID чата, куда нужно отправить фото (можно получить с помощью getUpdates)
CHAT_ID = "416521040"


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

    def send_photo(self, path_to_extract: str, list_photos=None):
        if list_photos is not None:
            for file_path in list_photos:
                try:
                    with open(os.path.join(path_to_extract, file_path), "rb") as photo:
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
