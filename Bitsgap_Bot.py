#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot
import json
import requests

API_TOKEN = '1753974075:AAGQ5B_QztpEsK0rYtm7x-9pio-wDrxaKK4'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Ciao sono BitsgapBot. Puoi usarmi per restare sempre all'erta riguardo le tue crypto preferite.
Usa i commands per utilizzare il bot e le sue funzioni.
""")

#Comando bitsgap che manda il link del sito all'utente
@bot.message_handler(commands=['bitsgap'])
def send_welcome(message):
    bot.reply_to(message, "https://app.bitsgap.com/bots-sharing/113240a0")

@bot.message_handler(commands=['excel'])
def send_welcome(message):
    bot.reply_to(message, "https://1drv.ms/x/s!AorU_8IVeEZGjO5UwrVQOZFGhvTQow?e=xhoVM8")

@bot.message_handler(commands=['addpair'])
def send_welcome(message):
    add_pair(message)
    
@bot.message_handler(commands=['removepair'])
def send_welcome(message):
    remove_pair(message)
    
@bot.message_handler(commands=['checkpairs'])
def send_welcome(message):
    bot.reply_to(message, pair_list_saved())

@bot.message_handler(commands=['binance'])
def send_welcome(message):
    Binance_Request(message)

@bot.message_handler(commands=['banane'])
def send_welcome(message):
    bot.reply_to(message, "https://www.twitch.tv/thelordsof_bananas")

# Codice per l'aggiunta di una coppia all'elenco di quelle da osservare

def add_pair(message):
    bot.reply_to(message, "Scrivi il nome di un mercato di cui vuoi tenere traccia.\n\nATTENZIONE: Inserisci la coppia nel formato 'valuta1valuta2'")
    bot.register_next_step_handler(message, write_json)

def write_json(message):
    try:
        pair = message.text
        
        #   Si controlla se la coppia inserita è presente su Binance    
        result = requests.get("https://api.binance.com/api/v3/ticker/price", params = {'symbol': pair}).json()
        bot.send_message(message.chat.id, "Hai selezionato la coppia " + result["symbol"] + ". La stiamo inserendo nel database, attendi la conferma")
        #   bot.reply_to(message, "Sto provando ad aprire il file")
    
        index = 0
        data = json.load(open("pair_data.json"))
        
        for i in data["pair"]:
            index += 1
        #   bot.reply_to(message, "Ho aperto il file")
    
        pair_data = {
                    "id":index,
                    "name":pair}
        data["pair"].append(pair_data)
        
        #   bot.reply_to(message, "Ho creato il nuovo json")
        json.dump(data, open("pair_data.json", "w"), indent = 4)
        bot.reply_to(message, "Hai correttamente impostato la coppia nel database")
    except Exception as e:
        bot.send_message(message.chat.id, "È stato riscontrato un errore, probabilmente la coppia inserita non corrisponde ad alcuna di quelle presenti su Binance.")
        bot.send_message(message.chat.id, "SUGGERIMENTI UTILI:\n1. Controlla di aver scritto bene la coppia che vuoi inserire. Il sistema accetta nomi come ADABUSD e non ADA/BUSD, ad esempio.\n2. Controlla l'effettiva esistenza della coppia su Binance: probabilmente avrai sbagliato un carattere o la pair non esiste.")
        

# Codice per la rimozione di una coppia dal database
def remove_pair(message):
    bot.send_message(message.chat.id, "Seleziona una coppia ")




        
        
        
# Codice per la visione del file ".json" 
def pair_list_saved():
    data = json.load(open("pair_data.json"))
    string_data = "Nel database ci sono le seguenti coppie salvate:\n\n"
    for i in data["pair"]:
        string_data += "ID: " + i["id"] + ", Mercato: " + i["name"] + "\n"
    return string_data
    
def Binance_Request(message):
    
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        data = json.load(open("pair_data.json"))
        stringa = ""
    
         # Ottengo i dati sul prezzo di ciascuna coppia contenuta nel file JSON
        for i in data["pair"]:
            data_to_display = requests.get(url, params = {'symbol':i["name"]}).json()
            stringa += "Nome: " + data_to_display["symbol"] + ", Prezzo: " + data_to_display["price"] + "\n"
        
        bot.send_message(message.chat.id, stringa)
    except Exception as e: 
        bot.send_message(message.chat.id, "È stato riscontrato un errore, probabilmente una coppia che hai inserito non corrisponde ad alcuna di quelle presenti su Binance.\n\nSUGGERIMENTO: Prova a togliere la coppia che non è presente su Binance, di solito funziona! :)")
#    ADA_Data = requests.get(url, params = {'symbol':'ADABUSD'})
#    Matic_Data = requests.get(url, params = {'symbol':'MATICBUSD'})
#    ADA = ADA_Data.json()
#    MATIC = Matic_Data.json()
#    stringa = "Nome: " + ADA["symbol"] + ", Prezzo: " + ADA["price"] + "\n"

    



#@bot.message_handler(commands=['excell'])
#def send_document(self, *args, **kwargs):
#    doc = open('/home/Ferremede/Resoconto_guadagni.xlsx', 'rb')
#    bot.send_document(-500512611, doc)
#    bot.send_document(-500512611, "FILEID")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
#@bot.message_handler(func=lambda message: True)
#def echo_message(message):
#    bot.reply_to(message, message.text)


bot.polling()
