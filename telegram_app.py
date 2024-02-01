from dotenv import load_dotenv
import telebot
import os

from src.processings.document_processing import document2text, preprocess_text
from src import neuro
import tempfile

load_dotenv()

bot = telebot.TeleBot(os.getenv("API_KEY"))
model = neuro.init_model()
tokenizer = neuro.init_tokenizer()
print('[#] Бот активен')
msg, file_path, file_name, downloaded_file = None, None, None, None


@bot.message_handler(content_types=['document'])  # list relevant content types
def addfile(message):
    global msg, file_path, file_name, downloaded_file
    msg = message
    # ask person and give 2 buttons
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(downloaded_file)
        file_path = tmp_file.name

    # create buttons
    keyboard = telebot.types.InlineKeyboardMarkup()
    key_prediction = telebot.types.InlineKeyboardButton(text='Маршрутизация', callback_data='Маршрутизация')
    keyboard.add(key_prediction)
    key_summary = telebot.types.InlineKeyboardButton(text='Резюмирование', callback_data='Резюмирование')
    keyboard.add(key_summary)
    question = 'Выберите тип операции над документом:'
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'Маршрутизация':
            # make prediction
            original_text = document2text(file_path)
            text = preprocess_text(original_text)
            prediction = neuro.predict(model, tokenizer, text)
            bot.send_message(msg.chat.id, "// Маршрутизация\n"
                                          "Имя файла: {}\n"
                                          "Результат обработки: {}".format(file_name, prediction))
        elif call.data == 'Резюмирование':
            text = neuro.summarize_file(file_path)
            bot.send_message(msg.chat.id, "// Резюмирование\n"
                                          "Имя файла: {}\n\n"
                                          "{}".format(file_name, text))


@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, "Привет, я бот, который поможет тебе разобраться с документами.\n"
                                "Просто отправь мне документ, и мы начнём работу!")


def activate():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    activate()
