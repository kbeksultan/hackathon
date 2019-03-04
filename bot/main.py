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
db = TinyDB(VARS)
loc = TinyDB(LOCATIONS)
cat = TinyDB(CATEGORIES)
ser = TinyDB(SERVICES)
q = Query()

# COMMANDS ================================================================
@bot.message_handler(commands=['start'])
def start(message):
	user_id = message.from_user.id

	user_name = message.from_user.first_name	
	data = START
	data['user_id'] = user_id

	if db.search(q.user_id == user_id) != []:
		db.update(data, q.user_id == user_id)

	else:
		db.insert(data)

	bot.send_message(message.chat.id, 'Hello, ' + str(user_name) + '\nThis bot here to accept your report\n\n' + 'Choose location and category please\n' + Commands , reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands = ['help'])
def help_user(message):
	bot.send_message(message.chat.id, Commands, reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['go'])
def go(message):
	_locate(message)

def _locate(message):
	user_id = message.from_user.id
	mode = MODES[1]
	msg = message.text
	data = {'current_mode': mode}
	db.update(data, q.user_id == user_id)

	# markup = _get_RKMarkup(_get_items(LOCATIONS), 3)
	markup = _get_RKMarkup( [x['name'] for x in loc.all()], 3)

	bot.send_message(message.chat.id, LOCATION_CHOOSE, reply_markup=markup)

	# bot.register_next_step_handler(msg,category(msg))	

@bot.message_handler(commands=['service'])
def service(message):
	user_id = message.from_user.id
	mode = MODES[3]

	data = {'current_mode': mode}
	db.update(data, q.user_id == user_id)

	# markup = _get_RKMarkup(_get_items(LOCATIONS), 3)
	markup = _get_RKMarkup( [x['title'] for x in ser.all()], 3)

	bot.send_message(message.chat.id, "Choose Service", reply_markup=markup)

# @bot.message_handler(commands=['category'])

def _category(message):
	print('asd')
	user_id = message.from_user.id
	mode = MODES[2]

	data = {'current_mode': mode}

	db.update(data, q.user_id == user_id)

	# markup = _get_RKMarkup(_get_items(CATEGORIES), 3)
	markup = _get_RKMarkup( [x['name'] for x in cat.all()], 3)
	
	bot.send_message(message.chat.id, CATEGORY_CHOOSE, reply_markup=markup)
	


@bot.message_handler(func=lambda message: True)
def echo(message):
	print(type(message))

	user_id = message.from_user.id

	current_mode = db.search(q.user_id == user_id)[0]['current_mode']
	location = None
	category = None
	service = None

	mode = None
	msg = None

	# print(current_mode)

	if current_mode == MODES[0]:
		bot.send_message(message.chat.id, 'Choose location, service and category please', reply_markup=types.ReplyKeyboardRemove())

	elif current_mode == MODES[1]:
		data = { 'location': message.text }

		db.update(data, q.user_id == user_id)

		msg = bot.send_message(message.chat.id, 'Location saved', reply_markup=types.ReplyKeyboardRemove())

		mode = 'category'

	elif current_mode == MODES[2]:
		data = { 'category': message.text }

		db.update(data, q.user_id == user_id)

		bot.send_message(message.chat.id, 'Category saved', reply_markup=types.ReplyKeyboardRemove())

		mode = 'service'

	elif current_mode == MODES[3]:
		data = { 'service': message.text }

		db.update(data, q.user_id == user_id)

		bot.send_message(message.chat.id, 'Service saved', reply_markup=types.ReplyKeyboardRemove())


	elif current_mode == MODES[4]:
		save(message)		# here save message

		bot.send_message(message.chat.id, 'Saved', reply_markup=types.ReplyKeyboardRemove())

	if mode == 'service':
		_service(message)

	elif mode == 'category':
		_category(message)
	
	elif category != 'null' and location != 'null' and service != 'null':
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
	diro += "/" + name + ".txt"
	f = open(diro , "a")
	date = date.strftime('%d/%m/%Y %H:%M:%S')
	f.write( date + " " + text + "\n")

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