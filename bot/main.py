import telebot

from telebot import types

from constants import *
from messages import *

bot = telebot.TeleBot(TOKEN)				# Bot creating through TOKEN

# COMMANDS ================================================================
@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "Hello")

@bot.message_handler(commands=['locate'])
def locate(message):
	markup = _get_RKMarkup(_get_items(LOCATIONS), 3)

	bot.send_message(message.chat.id, LOCATION_CHOOSE, reply_markup = markup)

@bot.message_handler(commands=['category'])
def locate(message):
	markup = _get_RKMarkup(_get_items(CATEGORIES), 3)

	bot.send_message(message.chat.id, CATEGORY_CHOOSE, reply_markup = markup)


@bot.message_handler(func=lambda message: True)
def echo(message):
	bot.send_message(message.chat.id, message.text.upper())

# MAIN =====================================================================
def main():									# method for bot polling
	print('Started!')

	bot.polling()

# AUXILLARY ================================================================
def _get_RKMarkup(arr, limit):
	markup = types.ReplyKeyboardMarkup(row_width=limit)

	size = len(arr)

	# print(size)

	for i in range(0, size, limit):
		
		row = []

		for j in range(limit):

			if i+j < size:
				row.append(arr[i+j])

				# print(arr[i+j] + '')

			else:
				break

		markup.row(*row)

	# print(markup)

	return markup

def _get_items(file):

	try:
		with open(file, "r") as file:
			arr = []

			for line in file:
				arr.append(line)

			return arr
	except:
		print(file + ' not found!')

if __name__ == '__main__':
	main()