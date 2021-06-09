from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler,Filters,CallbackQueryHandler
from telegram import ReplyKeyboardMarkup,ReplyKeyboardRemove,InlineKeyboardMarkup,InlineKeyboardButton,ParseMode,Bot
import requests,json
import os, sys

config = json.load(open('config.json','r'))

TOKEN = config['token']
DEV = True
signup = config['signup']
admins = config['admins']
refr = config['ref']
tkn = config['token_name']
tgk = config['telegram_kanal']
tgc = config['telegram_chat']
tw = config['twitter']
twp = config['twitter_post']
website = config['website']
data = []
dash_key = [['💰Balance','👥Referral'],['👨‍💻Profile','📈About'],['💣Withdraw', '📜Rules']]
continue_key = [['Continue👌']]
completed_key = [['Completed✅']]
admin_key = [['К-во','База','Рассылка']]

webhook_url = 'Your Webook' #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
PORT = int(os.environ.get('PORT','8443'))


def start(update, context):    
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        if user not in data['users']:
            data['users'].append(user)
            if user not in data['chat_id']: #######
                chat1id = str(update.message.chat.id)
                data['chat_id'].append(chat1id)
            if user not in data['twitter']:
                data['twitter'][user] = ""
            if user not in data['bep20']:
                data['bep20'][user] = ""
            if user not in data['mail']:
                data['mail'][user] = ""
            ref_id = update.message.text.split()
            if len(ref_id) > 1:
                data['ref'][user] = ref_id[1]
                if str(ref_id[1]) not in data['referred']:
                    data['referred'][str(ref_id[1])] = 1
                else:
                    data['referred'][str(ref_id[1])] += 1
            else:
                data['ref'][user] = 0
            data['total'] += 1
            data['id'][user] = data['total']
            msg = config['intro'] + '\n\n[👾Visit our website]({})'.format(website) #ИНТРО
            #ПРИМЕР "*bold* _italic_ `fixed width font` [link](http://google.com)\.",parse_mode= 'MarkdownV2'
            reply_markup = ReplyKeyboardMarkup(continue_key,resize_keyboard=True) #кнопка продолжить
            update.message.reply_text(msg, parse_mode= 'MarkdownV2',disable_web_page_preview=True,reply_markup=reply_markup) #----+вывод интр
            data['process'][user] = 'Continue'
            json.dump(data,open('users.json','w'))
        else:
            welcome_msg = "Welcome Back"
            reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True) #dash_key
            update.message.reply_text(welcome_msg,reply_markup=reply_markup) #----

    else:
        msg = '{} \n. I don\'t reply in group, come in private'.format(config['intro'])
        update.message.reply_text(msg)


def profile(update, context):
    if update.message.chat.type == 'private':
        user = str(update.message.chat.username)
        mail = data['mail'][user]
        twi = data['twitter'][user]
        bep20_addr = data['bep20'][user]
        msg = 'Your Provided Data:\n\n    Name: {}\n\n    E-mail: {}\n\n    Twitter: {}\n\n    Binance Smart Chain Address: {}'.format(user,mail,twi,bep20_addr)
        reply_markup = ReplyKeyboardMarkup(dash_key,resize_keyboard=True)
        update.message.reply_text(msg,reply_markup=reply_markup)

---------- FULL CODE AFTER DONATE ----------

if __name__ == '__main__':
    data = json.load(open('users.json','r'))
    updater = Updater(TOKEN,use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start)) #обработчики команд
    dp.add_handler(CommandHandler("admin",admin))
    dp.add_handler(MessageHandler(Filters.regex("^👨‍💻Profile$"),profile))
    dp.add_handler(MessageHandler(Filters.regex("^📈About$"),about))
    dp.add_handler(MessageHandler(Filters.regex("^💣Withdraw$"),withdraw))
    dp.add_handler(MessageHandler(Filters.regex("^📜Rules"),rules))
    dp.add_handler(MessageHandler(Filters.regex("^👥Referral$"),ref))
    dp.add_handler(MessageHandler(Filters.regex("^💰Balance$"),bal))
    dp.add_handler(MessageHandler(Filters.regex("^К-во$"),users))
    dp.add_handler(MessageHandler(Filters.regex("^Рассылка$"),mailing))
    dp.add_handler(MessageHandler(Filters.regex("^База$"),get_file))
    dp.add_handler(MessageHandler(Filters.text,extra))
    ##dp.add_handler(MessageHandler(Filters.text,registration))

    if DEV is not True:
        updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN)
        updater.bot.set_webhook(webhook_url + TOKEN)
    else:
        updater.start_polling()
    print("Bot Started")
    updater.idle()


#telegram.error.RetryAfter: Flood control exceeded. Retry in 3 seconds увеличить время таймаута
