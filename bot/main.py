import telebot
import json

from telebot import types

from constants import *
from datetime import datetime
import os
from messages import *

MODES = ['INIT', 'LOCATION', 'CATEGORY', 'RECORD']
START = {"location": "null", "category": "null", "current_mode": "INIT"}

bot = telebot.TeleBot(TOKEN)				# Bot creating through TOKEN

# COMMANDS ================================================================
@bot.message_handler(commands=['start'])
def start(message):
	_set_json(VARS, START)

	bot.send_message(message.chat.id, "Hello")

@bot.message_handler(commands=['locate'])
def locate(message):
	_update(VARS, 'current_mode', MODES[1])

	markup = _get_RKMarkup(_get_items(LOCATIONS), 3)

	bot.send_message(message.chat.id, LOCATION_CHOOSE, reply_markup = markup)

@bot.message_handler(commands=['category'])
def category(message):
	_update(VARS, 'current_mode', MODES[2])

	markup = _get_RKMarkup(_get_items(CATEGORIES), 3)

	bot.send_message(message.chat.id, CATEGORY_CHOOSE, reply_markup = markup)

@bot.message_handler(func=lambda message: True)
def echo(message):
	current_mode = _get_json(VARS)['current_mode']
	location = None
	category = None

	if current_mode == MODES[0]:
		bot.send_message(message.chat.id, message.text.upper())

	elif current_mode == MODES[1]:
		_update(VARS, 'location', message.text)

	elif current_mode == MODES[2]:
		_update(VARS, 'category', message.text)	

	elif current_mode == MODES[3]:
		location = _get_json(VARS)['location']
		category = _get_json(VARS)['category']

		bot.send_message(message.chat.id, location + ':' + category)
		save(message)		# here save message

	if category != 'null' and location != 'null':
		_update(VARS, 'current_mode', MODES[3])

	else:
		_update(VARS, 'current_mode', MODES[0])



def save(message):
	location = _get_json(VARS)['location']
	category = _get_json(VARS)['category']
	text  = message.text
	name  = message.from_user.first_name
	date = datetime.now()
	diro = "../Notes/" + location
	if not os.path.exists(diro):
		os.mkdir(diro)
	diro += "/" + category
	if not os.path.exists(diro):
		os.mkdir(diro)
	diro += "/" + name
	if not os.path.exists(diro):
		os.mkdir(diro)
	diro += "/" + date.strftime('%d_%m_%Y_%H_%M_%S') + ".txt"
	f = open(diro , "a")
	date = date.strftime('%d/%m/%Y %H:%M:%S')
	f.write(name + " " + date + " " + text)



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
		with open(file, "r") as f:
			arr = []

			for line in f:
				arr.append(line)

			return arr
	except:
		print(file + ' not found!')

def _update(file, field, value):
	data = _get_json(file)

	try:
		data[field] = value

	except:
		print('field not found!')

	_set_json(file, data)

def _set_json(file, data):
	try:
		with open(file, "w") as f:
			json.dump(data, f)

	except:
		print(file + ' not found!')

def _get_json(file):
	try:
		with open(file, "r") as f:
			data = json.load(f)

			return data

	except:
		print(file + ' not found!')

if __name__ == '__main__':
	main()