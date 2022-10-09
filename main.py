import time
from threading import Timer
from datetime import datetime, timedelta
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


def format_data(data_list):
    time_data = []
    text_data = []
    try:
        for data in data_list:
            data_split = data.split('; ')
            time_data.append(data_split[0])
            text_data.append(data_split[1])
        return time_data, text_data
    except:
        return 0, 0


def calculate_time(time_data):
    posting_time = []
    try:
        for i in range(len(time_data)):
            days, hours, minutes = list(map(int, time_data[i].split(':')))
            delay = days * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60
            # run_at = datetime.now() + timedelta(days=int(days), hours=int(hours), minutes=int(minutes))
            # delay = run_at - datetime.now()
            posting_time.append(delay)
        return posting_time
    except:
        return 0


def main():
    TOKEN = '5797780733:AAFlU1EkmrPkVm2H8-zX9O8fRsC3YpSlaCU'
    bot = Bot(TOKEN)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start'])
    async def com_start(message: types.Message):
        await message.answer('Привет! Я покорный раб МП Раменки и помогаю выкладывать в чат актуальное расписание!')

    @dp.message_handler(commands=['help'])
    async def com_start(message: types.Message):
        await message.answer('Команды:\n'
                             '/start - запуск\n'
                             '/load_info - загрузка актуального расписания\n'
                             '/help - список доступных комманд')

    @dp.message_handler(commands=['load_info'])
    async def com_load_info(message: types.Message):
        await message.answer('Привет! Загрузи в меня расписание в формате:\n'
                             'Запись;\n'
                             'дд.чч.мм.сс (через какое время выложить пост); текст поста (сколько угодно строк)')

    @dp.message_handler()
    async def load_info(message: types.Message):
        if message.text.split('\n')[0].lower() == 'запись':
            data_list = message.text.split('\n')[1:]

            time_data, text_data = format_data(data_list)

            if not time_data or not text_data:
                await message.reply('[!] Ошибка в формате введенных данных!')
                return

            posting_time = calculate_time(time_data)

            if not posting_time:
                await message.reply('[!] Ошибка в формате введенного времени!')
                return

            for i in range(len(posting_time)):
                await posting(posting_time[i], text_data[i], message.from_user.id)
                posting_time = [j - posting_time[i] for j in posting_time]
                print(posting_time)

    @dp.message_handler(content_types=['text'])
    async def posting(time_sec, message, id):
        print(time_sec)
        time.sleep(time_sec)
        await bot.send_message(id, message)

    executor.start_polling(dp, skip_updates=1)


if __name__ == '__main__':
    main()
