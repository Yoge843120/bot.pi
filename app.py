import requests
from bs4 import BeautifulSoup
import pandas as pd
import telegram
from telegram.ext import Updater, CommandHandler, Job

bot_token = "your_bot_token_here"
bot = telegram.Bot(token=bot_token)
updater = Updater(token=bot_token, use_context=True)
job_queue = updater.job_queue

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I am a bot that can show you live data of NSE indices.")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can use these commands to get data:\n/nifty for Nifty 50\n/bank for Bank Nifty\n/fin for Fin Nifty")

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Stopping the bot.")
    job_queue.stop()

def send_nifty_data(context):
    chat_id = context. job.context
    # send a message that says you are getting data
    context. bot.send_message(chat_id=chat_id, text="Getting data for Nifty 50...")
    # define the URL of the page that contains the Nifty 50 option chain data
    url = "https://www.nseindia.com/option-chain"
    # send a GET request to the URL and get the HTML content
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    content = response.text
    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")
    # find the table that contains call and put oi data
    call_table = soup.find("table", {"id": "octable"})
    # find the table rows that contain the call oi and put oi data
    call_oi_rows = call_table.select("tr.call-oi-table-row")
    put_oi_rows = call_table.select("tr.put-oi-table-row")
    # extract the total call oi and total put oi values
    total_call_oi = sum(int(row.select_one("td:nth-of-type(2)").text.replace(",", "")) for row in call_oi_rows)
    total_put_oi = sum(int(row.select_one("td:nth-of-type(21)").text.replace(",", "")) for row in put_oi_rows)
    # calculate the pcr value by dividing the total put oi by the total call oi
    pcr = total_put_oi / total_call_oi
    # format the data as a string
    data = f"Total Call OI: {total_call_oi}\nTotal Put OI: {total_put_oi}\nPCR: {pcr}"
    # send a message with the data to the user
    context.bot.send_message(chat_id=chat_id, text=data)

def send_bank_data(context):
    chat_id = context.job.context
    # send a message that says you are getting data
    context.bot.send_message(chat_id=chat_id, text="Getting data for Bank Nifty...")
    # define the URL of the page that contains Bank Nifty option chain data
    url = "https://www.nseindia.com/option-chain"
    # send a GET request to the URL and get the HTML content
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    content = response.text
    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")
    # find the table that contains call and put oi data
    call_table = soup.find("table", {"id": "octable"})
    # find the table rows that contain the call oi and put oi data
    call_oi_rows = call_table.select("tr.call-oi-table-row")
    put_oi_rows = call_table.select("tr.put-oi-table-row")
    # extract the total call oi and total put oi values
    total_call_oi = sum(int(row.select_one("td:nth-of-type(2)").text.replace(",", "")) for row in call_oi_rows)
    total_put_oi = sum(int(row.select_one("td:nth-of-type(21)").text.replace(",", "")) for row in put_oi_rows)
    # calculate the pcr value by dividing the total put oi by the total call oi
    pcr = total_put_oi / total_call_oi
    # format the data as a string
    data = f"Total Call OI: {total_call_oi}\nTotal Put OI: {total_put_oi}\nPCR: {pcr}"
    # send a message with the data to the user
    context.bot.send_message(chat_id=chat_id, text=data)

def send_fin_data(context):
    chat_id = context.job.context
    # send a message that says you are getting data
    context.bot.send_message(chat_id=chat_id, text="Getting data for Fin Nifty...")
    # define the URL of the page that contains Fin Nifty option chain data
    url = "https://www.nseindia.com/option-chain"
    # send a GET request to the URL and get the HTML content
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    content = response.text
    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")
    # find the table that contains call and put oi data
    call_table = soup.find("table", {"id": "octable"})
    # find the table rows that contain the call oi and put oi data
    call_oi_rows = call_table.select("tr.call-oi-table-row")
    put_oi_rows = call_table.select("tr.put-oi-table-row")
    # extract the total call oi and total put oi values
    total_call_oi = sum(int(row.select_one("td:nth-of-type(2)").text.replace(",", "")) for row in call_oi_rows)
    total_put_oi = sum(int(row.select_one("td:nth-of-type(21)").text.replace(",", "")) for row in put_oi_rows)
    # calculate the pcr value by dividing the total put oi by the total call oi
    pcr = total_put_oi / total_call_oi
    # format the data as a string
    data = f"Total Call OI: {total_call_oi}\nTotal Put OI: {total_put_oi}\nPCR: {pcr}"
    # send a message with the data to the user
    context.bot.send_message(chat_id=chat_id, text=data)

def nifty(update, context):
    chat_id = update.effective_chat.id
    # schedule the job to run immediately
    job_queue.run_once(send_nifty_data, 0, context=chat_id)

def bank(update, context):
    chat_id = update.effective_chat.id
    # schedule the job to run immediately
    job_queue.run_once(send_bank_data, 0, context=chat_id)

def fin(update, context):
    chat_id = update.effective_chat.id
    # schedule the job to run immediately
    job_queue.run_once(send_fin_data, 0, context=chat_id)

# define command handlers
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
stop_handler = CommandHandler('stop', stop)
nifty_handler = CommandHandler('nifty', nifty)
bank_handler = CommandHandler('bank', bank)
fin_handler = CommandHandler('fin', fin)

# add command handlers to the updater
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(stop_handler)
updater.dispatcher.add_handler(nifty_handler)
updater.dispatcher.add_handler(bank_handler)
updater.dispatcher.add_handler(fin_handler)

# start the bot
updater.start_polling()

