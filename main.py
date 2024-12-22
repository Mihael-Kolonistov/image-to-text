from aiogram import Bot, Dispatcher, types, executor
import cv2
import os

TOKEN = ""

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot)
old_f=""
@dp.message_handler()
async def start(message: types.Message):
    await message.reply(f'Пришли <b>фото</b> для конвертации его в текст из символов:\nФото должно быть:\n<code>    </code>-<b>квадратным, ну, +-</b>\n<code>    </code>-<b>Файлом</b>!', parse_mode='html')

@dp.message_handler(content_types=['photo', 'document'])
async def scan_message(message: types.Message):
            try:
                 os.remove(f"{destination}")
            except:
                 print("no old files")            
            destination = f"{message.from_user.id}.jpg"
            await message.reply(f'Качаю...', parse_mode='html')
            destination_file = await message.document.download(destination)
            

            string = " `.,-':<>;+!*/?%&98#"
            coef = 255 / (len(string) - 1)
            image = cv2.imread(destination)
            height, width, channels = image.shape
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            await message.reply(f'Обработка...', parse_mode='html')
            with open(f"{destination}.txt", "w") as file:
                global old_f
                for x in range(0, width - 1, 8):
                    s = ""
                    for y in range(0, height - 1, 4):
                        try:
                            s += string[len(string) - int(gray_image[x, y] / coef) - 1]
                            continue
                        except IndexError:
                            pass
                    if len(s) != 0:
                        file.write(s + "\n")
                old_f = destination                
            await message.reply(f'Отправка...', parse_mode='html')
            l=open(f"{destination}.txt", 'rb')
            await message.reply_document(l)
            l.close()
            os.remove(f"{destination}.txt")
            
if __name__ == "__main__":
    executor.start_polling(dispatcher=dp)
