import telebot
import json
import os

from telebot import types
from datetime import datetime
from tinydb import TinyDB, Query

from constants import *
from messages import *

MODES = ['INIT', 'LOCATION', 'CATEGORY', 'RECORD']
START = {"user_id": "0", "location": "null", "category": "null", "current_mode": "INIT"}

bot = telebot.TeleBot(TOKEN)				# Bot creating through TOKEN
db = TinyDB('vars.json')
q = Query()

# COMMANDS ================================================================
@bot.message_handler(commands=['start'])
def start(message):
	user_id = message.from_user.id

	data = START
	data['user_id'] = user_id

	if db.search(q.user_id == user_id) != []:
		db.update(data, q.user_id == user_id)

	else:
		db.insert(data)
	bot.send_message(message.chat.id, 'Hi, my name is TestBot.Your user id is ' + str(user_id), reply_markup=types.ReplyKeyboardRemove())
	
	# bot.register_next_step_handler(message,locate(message))	

@bot.message_handler(commands = ['help'])
def help_user(message):
	bot.send_message(message.chat.id, Commands, reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['locate'])
def locate(message):
	user_id = message.from_user.id
	mode = MODES[1]
	msg = message.text
	data = {'current_mode': mode}
	db.update(data, q.user_id == user_id)

	markup = _get_RKMarkup(_get_items(LOCATIONS), 3)
	bot.send_message(message.chat.id, LOCATION_CHOOSE, reply_markup=markup)

	# bot.register_next_step_handler(msg,category(msg))	



@bot.message_handler(commands=['category'])
def category(message):
	user_id = message.from_user.id
	mode = MODES[2]

	data = {'current_mode': mode}

	db.update(data, q.user_id == user_id)

	markup = _get_RKMarkup(_get_items(CATEGORIES), 3)
	bot.send_message(message.chat.id, CATEGORY_CHOOSE, reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo(message):
	user_id = message.from_user.id

	current_mode = db.search(q.user_id == user_id)[0]['current_mode']
	location = None
	category = None

	# print(current_mode)

	if current_mode == MODES[0]:
		bot.send_message(message.chat.id, 'Choose location and category please', reply_markup=types.ReplyKeyboardRemove())

	elif current_mode == MODES[1]:
		data = { 'location': message.text }

		db.update(data, q.user_id == user_id)

		bot.send_message(message.chat.id, 'Location saved', reply_markup=types.ReplyKeyboardRemove())

	elif current_mode == MODES[2]:
		data = { 'category': message.text }

		db.update(data, q.user_id == user_id)

		bot.send_message(message.chat.id, 'Category saved', reply_markup=types.ReplyKeyboardRemove())

	elif current_mode == MODES[3]:
		save(message)		# here save message

		bot.send_message(message.chat.id, 'Saved', reply_markup=types.ReplyKeyboardRemove())

	if category != 'null' and location != 'null':
		mode = MODES[3]
		data = { 'current_mode': mode }

		db.update(data, q.user_id == user_id)

	else:
		mode = MODES[0]
		data = { 'current_mode': mode }

		db.update(data, q.user_id == user_id)

def save(message):
	user_id = message.from_user.id

	location = db.search(q.user_id == user_id)[0]['location']
	category = db.search(q.user_id == user_id)[0]['category']
	
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
	# bot.enable_save_next_step_handlers(delay=2)

	# bot.load_next_step_handlers()
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

if __name__ == '__main__':
	main()