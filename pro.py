from telegram.ext import Updater, CommandHandler
import logging
import requests
import pandas as pd

def get_option_data(symbol):
    # get the option chain data from NSE website
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # extract the expiry dates and the current spot price
    expiry_dates = data["records"]["expiryDates"]
    spot_price = data["records"]["underlyingValue"]

    # choose the nearest expiry date
    expiry_date = expiry_dates[0]

    # create a dataframe from the option chain data
    df = pd.DataFrame(data["filtered"]["data"])

    # filter the dataframe for the current spot price and expiry date
    filtered_df = df[(df["strikePrice"] == spot_price) & (df["expiryDate"] == expiry_date)]

    # calculate the total open interest (TOI) for put and call options
    put_toi = filtered_df["PE_OI"].sum()
    call_toi = filtered_df["CE_OI"].sum()

    # calculate the put-call ratio (PCR)
    pcr = put_toi / call_toi

    # return the PCR value as a string
    return f"{pcr:.2f}"


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="yo homie !")

def nifty(update, context):
    pcr = get_option_data("NIFTY")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Nifty 50 PCR: {pcr}")

def banknifty(update, context):
    pcr = get_option_data("BANKNIFTY")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Bank Nifty PCR: {pcr}")

def finnifty(update, context):
    pcr = get_option_data("FINNIFTY")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Fin Nifty PCR: {pcr}")

def main():
    # Telegram bot token
    token = "6230457934:AAGHq3ZOU4po9rDjVMcRRbybso0uaJCdqG0"
    updater = Updater(token)
    dispatcher = updater.dispatcher

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # Define command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("nifty", nifty))
    dispatcher.add_handler(CommandHandler("bank", banknifty))
    dispatcher.add_handler(CommandHandler("fin", finnifty))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()