import os
import requests
from zipfile import ZipFile
from urllib.parse import urlencode
from loguru import logger
# from services.logger import init_logging

# logger = init_logging('INFO',name ='loadzip.py')

logger.info("Start module load zip")


class LoadZip:
    """КЛасс для загрузки ZIP с ЯД и распаковки его
    на диск
    Args:
        base_url (str):  копируем из URL От ЯД (без ключа в конце)
        public_key (str):  он в конце URL от ЯД
    """

    def __init__(self, base_url: str, public_key: str) -> None:
        self.base_url = base_url
        self.public_key = "https://disk.yandex.ru/d/" + public_key

    def __request_files_in_zip(self):
        """получение загрузочного URL, для последующей загрузки
        Args:
            zip_filename (str):
            unzip_path (str): куда распаковываем
        """
        logger.info('try to get final load url (https:///....zip)')
        final_url = self.base_url + urlencode(dict(public_key=self.public_key))
        # Получаем загрузочную ссылку для Zip файла
        response = requests.get(final_url)
        return response.json()["href"]

    def load_zip_file(self, path_to_extract: str, zip_filename: str):
        """Скачиваем и распаковываем ZIP файл для 
        последующего анализа

        Args:
            path_to_extract (str): _description_
            zip_filename (str): _description_

        Returns:
            _type_: _description_
        """
        #  создаем если не было
        os.makedirs(path_to_extract, exist_ok=True)
        self.path_to_extract = path_to_extract
        self.zip_file_name = zip_filename
        full_file_path = os.path.join(path_to_extract, zip_filename)
        self.zip_file_name = zip_filename
        
        # подсовываем нужные аргументы
        try:
            download_url = self.__request_files_in_zip()
        except Exception as e:
            print(f"Не получилось получить Download ссылку: {e}")
            return False
        # Загружаем файл и сохраняем его
        try:
            download_response = requests.get(download_url, timeout=1000)
            if download_response.status_code == 200:
                # сначала узнаем, не такой же уже лежит на диске
                if os.path.exists(full_file_path):
                    if os.path.getsize(full_file_path) == len(download_response.content):
                        logger.info("Nothing new - zip file the same")
                        return False
                with open(full_file_path, "wb") as zip_file:
                    zip_file.write(download_response.content)
                    logger.info(f'file {full_file_path} saved succefully')
                    # print("zip file wrote successfully!")
                    return zip_file.name
           
        except Exception as e:
            logger.error(f'Error in ZIP file download or save: {e}')
            return False

    @logger.catch
    def extract_zip(self):
        if self.zip_file_name is not None:
            with ZipFile(
                os.path.join(self.path_to_extract, self.zip_file_name), "r"
            ) as zipfile:
                result_file_list = []  # список для отправления на скачку
                # сначала сверяемся, что его нет, только потом- извлекаем
                for name in zipfile.namelist():
                    if not os.path.exists(
                        os.path.join(self.path_to_extract, name)):
                        result_file_list.append(name)
                        zipfile.extract(name, self.path_to_extract)
                return result_file_list
        return None


if __name__ == "__main__":
    zip_file = LoadZip(
        "https://cloud-api.yandex.net/v1/disk/public/resources/download?",
        "564f234gh5467",
    )
