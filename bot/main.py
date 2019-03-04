import telebot
import json
import os

from telebot import types
from datetime import datetime
from tinydb import TinyDB, Query

from constants import *
from messages import *

MODES = ['INIT', 'LOCATION', 'CATEGORY', 'SERVICE', 'RECORD']
START = {"user_id": "0", "location": "null", "category": "null", "service": "null", "current_mode": "INIT"}

bot = telebot.TeleBot(TOKEN)				# Bot creating through TOKEN
var = TinyDB(VARS)
loc = TinyDB(LOCATIONS)
cat = TinyDB(CATEGORIES)
ser = TinyDB(SERVICES)
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

	bot.send_message(message.chat.id, 'Your user id is ' + str(user_id), reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands = ['help'])
def help_user(message):
	bot.send_message(message.chat.id, Commands, reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['locate'])
def locate(message):
	user_id = message.from_user.id
	mode = MODES[1]

	data = {'current_mode': mode}
	db.update(data, q.user_id == user_id)

	# markup = _get_RKMarkup(_get_items(LOCATIONS), 3)
	markup = _get_RKMarkup( [x['name'] for x in loc.all()], 3)

	bot.send_message(message.chat.id, LOCATION_CHOOSE, reply_markup=markup)

@bot.message_handler(commands=['service'])
def service(message):
	user_id = message.from_user.id
	mode = MODES[3]

	data = {'current_mode': mode}
	db.update(data, q.user_id == user_id)

	# markup = _get_RKMarkup(_get_items(LOCATIONS), 3)
	markup = _get_RKMarkup( [x['title'] for x in ser.all()], 3)

	bot.send_message(message.chat.id, "Choose Service", reply_markup=markup)

@bot.message_handler(commands=['category'])
def category(message):
	user_id = message.from_user.id
	mode = MODES[2]

	data = {'current_mode': mode}

	db.update(data, q.user_id == user_id)

	# markup = _get_RKMarkup(_get_items(CATEGORIES), 3)
	markup = _get_RKMarkup( [x['name'] for x in cat.all()], 3)
	
	bot.send_message(message.chat.id, CATEGORY_CHOOSE, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo(message):
	user_id = message.from_user.id

	current_mode = db.search(q.user_id == user_id)[0]['current_mode']
	location = None
	category = None
	service = None

	# print(current_mode)

	if current_mode == MODES[0]:
		bot.send_message(message.chat.id, 'Choose location, service and category please', reply_markup=types.ReplyKeyboardRemove())

	elif current_mode == MODES[1]:
		data = { 'location': message.text }

		db.update(data, q.user_id == user_id)

		bot.send_message(message.chat.id, 'Location saved', reply_markup=types.ReplyKeyboardRemove())

	elif current_mode == MODES[2]:
		data = { 'category': message.text }

		db.update(data, q.user_id == user_id)

		bot.send_message(message.chat.id, 'Category saved', reply_markup=types.ReplyKeyboardRemove())

	elif current_mode == MODES[3]:
		data = { 'service': message.text }

		db.update(data, q.user_id == user_id)

		bot.send_message(message.chat.id, 'Service saved', reply_markup=types.ReplyKeyboardRemove())

	elif current_mode == MODES[4]:
		save(message)		# here save message

		bot.send_message(message.chat.id, 'Saved', reply_markup=types.ReplyKeyboardRemove())

	if category != 'null' and location != 'null' and service != 'null':
		mode = MODES[4]
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
	service = db.search(q.user_id == user_id)[0]['service']
	
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

if __name__ == '__main__':
	main()