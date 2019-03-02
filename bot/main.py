import telebot

from telebot import types

from constants import *
from datetime import datetime
import os
bot = telebot.TeleBot(TOKEN)				# Bot creating through TOKEN

# /start
@bot.message_handler(commands=['start'])
def start(message):
	markup = _get_RKMarkup(_get_items(LOCATIONS), 3)

	bot.send_message(message.chat.id, "Hello", reply_markup = markup)


def save(message):
	text  = message.text
	name  = message.from_user.first_name
	date = datetime.now()
	diro = "../Notes/" + name
	if not os.path.exists(diro):
		os.mkdir(diro)
	road  = "../Notes/" + name + "/" + date.strftime('%d_%m_%Y_%H_%M_%S') + ".txt"
	f = open(road , "a")
	date = date.strftime('%d/%m/%Y %H:%M:%S')
	f.write(name + " " + date + " " + text)



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