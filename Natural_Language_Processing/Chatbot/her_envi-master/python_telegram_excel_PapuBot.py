# -*- coding: utf-8 -*-
"""
Created on Tue May  1 11:39:08 2018

@author: Alberto
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

# path
import os
import sys

path='C:\\Users\\Alberto\\.spyder-py3'

if path not in sys.path:
    sys.path.append(path)

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging



################################### EXCEL ################### s
import openpyxl
import datetime

def add_clear_excel(value, add_clear):
    # 0 clear
    # 1 add
    # motiv add motive
    
    # Path
    path='C:\\Users\\Alberto\\Documents\\PYTHON_EXCEL\\prueba.xlsx'
    wb=openpyxl.load_workbook(path)
    # Numero de hoja
    sheet=wb.active
    ###########
    n=6
    if (add_clear==0):
        n=7
        value=None
    i=str(n)
    col='B'
    col2='C'
    col3='D'
    print("Gastos anteriores: \n")
    while (sheet[col+i].value!=None):
        if (add_clear==0):
            sheet[col+i]=None
            sheet[col2+i]=None
        n+=1
        i=str(n)
        print(sheet[col+i].value)
    sheet[col+i]=value
    sheet[col2+i]=datetime.date.today()
    sheet[col2+i].number_format = 'd-mmm-yy'
    if (add_clear!=0 and add_clear!=1):
        sheet[col3+i]= add_clear
    ##########
    wb.save(path)
    

################################### EXCEL ###################
 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING = range(3)

c1='Papu 1800-400'
c2='Clear Excel'
c3='Add Expenses'
c4='ExpensesMot'
c5='Done'

reply_keyboard = [[c1, c2],
                  [c3, c4],
                  [c5]]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

# ---------------- Funciones AUXILIARES ----------------------
def contestar(update, mistr):
    update.message.reply_text(mistr)

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):
    update.message.reply_text(
        "Hi! My name is PapuBot\n"
        "Que quieres hacer?",
        reply_markup=markup)

    return CHOOSING
#------------------------------------------------------------


#   ELECCION NORMAL
def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    
    if(text==c1):
        strr='Aplicar la regla de tres: \n\t1 -- 1800 [h]\n\tF -- x  [h]\n'
        strr+='Introduzca las horas que quiere saber :'
        update.message.reply_text(strr)
        
    elif(text==c2):
        contestar(update,'Pulsa cualquier tecla para borrar')
    elif (text==c3): #anadir gasto
       update.message.reply_text('Tell me how much you expent')
    elif(text!=c4):
        contestar(update,'Dime el motivo')
    else:
        update.message.reply_text(
        'Your {}? Yes, I would love to hear about that!'.format(text.lower()))

    return TYPING_REPLY

#   ELECCION CUSTOM
def custom_choice(bot, update):
    update.message.reply_text('Alright, send me how much you expent first')

    return TYPING

# RECEPCION DE MENSAJE
def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    
    print(text)
    print(category)
    print(user_data)
    
    del user_data['choice']
    
    print(category)
    # añadimos gasto
    if (category==c1):
        result=float(text)/float(1800)
        str2='---:> Fracion = {0:.3f}\n'.format(result)
        contestar(update,str2)
        contestar(update,'Fin de la tarea')
    elif (category==c2):  # borramos excel
        add_clear_excel(text, 0)
        contestar(update,'Fin del clear, ComemeerDonu')
    elif (category==c3):
        print('Te has gastado '+text)
        add_clear_excel(text, 1)
        contestar(update,'Fin de la tarea, gasto añadido')
    elif (category!=c4):
        l=list()
        l=list(user_data.items())
        print(l)
        add_clear_excel(l[0][0],l[0][1])
        contestar(update,'Fin de la tarea, gasto añadido, Vero Guapa ;)')
    else:
        update.message.reply_text("Neat! Just so you know, this is what told me:"
                              "{}"
                              "You can tell me more, or change .".format(
                                  facts_to_str(user_data)), reply_markup=markup)
   
    return CHOOSING



def done(bot, update, user_data):
    chat_id = update.message.chat_id
    if 'choice' in user_data:
        del user_data['choice']
    bot.send_voice(chat_id, voice=open('audio_2018.ogg', 'rb'))    
    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

####################### MAIN #####################################
# Create the Updater and pass it your bot's token.


def main():
    idbot='576486660:AAF8b947rCRQa0NU0RQOQHmz7453dD7DoF8'
    updater = Updater(idbot)
    
    
        
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    print("VeroBot started")
    
    # string del regexhandler
    regstr='^({}|{}|{})$'.format(c1,c2,c3)
    
    
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        
        states={
            CHOOSING: [RegexHandler(regstr,
                                    regular_choice,
                                    pass_user_data=True),
                       RegexHandler('^'+c4+'$',
                                    custom_choice),
                       ],

            TYPING: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
