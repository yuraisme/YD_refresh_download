from loadzip import LoadZip
from telegramm import Telegramm
import os
import time
from dotenv import load_dotenv

load_dotenv()
ENV = dict(os.environ)
BASE_URL = ENV["BASE_URL"]
PUBLIC_KEY = ENV["PUBLIC_KEY"]
PATH_TO_EXTRACT = ENV["PATH_TO_EXTRACT"]
ZIP_FILE = ENV["ZIP_FILE"]  # название ZIP файла для временного хранения

prev_list_file = []
telegramm = Telegramm()

if __name__ == "__main__":
    while True:
        zip_file = LoadZip(BASE_URL, PUBLIC_KEY)  # инициализируем
        if not zip_file.load_zip_file(PATH_TO_EXTRACT, ZIP_FILE):            
            break
        list_for_send = zip_file.extract_zip()
        if list_for_send:
            print(f"files for send: {list_for_send}")
            telegramm.send_photo(PATH_TO_EXTRACT, list_for_send)
            # exit(0)
        else:
            print('нет изменений!')
        time.sleep(120)
