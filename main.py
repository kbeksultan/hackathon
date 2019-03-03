import telebot

from constants import *

bot = telebot.TeleBot(TOKEN)				# Bot creating through TOKEN

# /start
@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "Hello")

def main():									# method for bot polling
	print('Started!')

	bot.polling()

if __name__ == '__main__':
	main()