1. запрашиваем зугрузочный файл через публичный ключ
2. загружаем с помощью полученного URL
3. распаковываем по одному
4. если файл существует, просто переписываем, если нет - возвращаем список,
 в котором только отсутсвующие файлы
5. посылаем в телеграм список с файлами
6. очищаем список.


## ПРИМЕР .env файла:

**BOT_TOKEN**="токен от bot_father" <br>
**ZIP_FILE** = "downloaded_file.zip"<br>
**PATH_TO_EXTRACT** = "PATH"<br>
**BASE_URL** = "https://cloud-api.yandex.net/v1/disk/public/resources/download?"<br>
**PUBLIC_KEY** = "1u09L12324og6qQ"  # в конце ссылки на папку/файл  в URL от ЯД"
<br><br>
` сначала нужно напечатать что-то в бота, а потом в Linux:` <br>
 *curl https://api.telegram.org/bot{ВАШ:ТОКЕН}/getUpdates*<br>
**CHAT_ID**  = ID в JSON  и будет вашим chat ID
