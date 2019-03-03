import telebot

from telebot import types

from constants import *

bot = telebot.TeleBot(TOKEN)				# Bot creating through TOKEN

# /start
@bot.message_handler(commands=['start'])
def start(message):
	markup = _get_RKMarkup(_get_items(LOCATIONS), 3)

	bot.send_message(message.chat.id, "Hello", reply_markup = markup)

# MAIN =====================================================================
def main():									# method for bot polling
	print('Started!')

	# for i in _get_items(LOCATIONS):
	# 	print(i, end='')

	bot.polling()

# AUXILLARY ================================================================
def _get_RKMarkup(arr, limit):
	markup = types.ReplyKeyboardMarkup(row_width=limit)

	size = len(arr)

	# print(size)

	for i in range(0, size, limit):
		
		row = []

		for j in range(limit):

			if i + j < size:
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