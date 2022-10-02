from credentials import TOKEN, usr, pwd

from fileinput import filename
import logging

#Import to remove images folder
import os
import shutil
from typing import final

from telegram import InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(filename = "ig-dl.log",format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - Error line %(lineno)s', level=logging.INFO)
logger = logging.getLogger(__name__)

#Login for instagram high quality downlaod
import instaloader
insta = instaloader.Instaloader(save_metadata=False, dirname_pattern= "images", title_pattern="{target}")
insta.login(usr, pwd)

# Downloader profile function
def start(update, context):
    update.message.reply_text("Inserisca il nome utente (comprensivo di @ iniziale) del quale desidera scaricare la foto profilo 📷\n(disponibili nuove funzionalità nel menù comandi 😊)")

def downloader(update, context):
    user = update.message.from_user
    ig_username = update.message.text
    final_username = ig_username.replace ("@", "")
    try:
        profilo = instaloader.Profile.from_username(insta.context, final_username)
        profili = {profilo}
        update.message.reply_text("Invio foto in corso ☁️")
        #get file_id of media
        insta.download_profiles(profili, profile_pic=True, posts=False)
        media_id = InputFile(open("images/" + final_username + ".jpg", "rb"))
        update.message.reply_photo(photo=media_id)
    except instaloader.exceptions.ProfileNotExistsException:
        update.message.reply_text('Non esiste alcun utente con tale username 😢')
    except instaloader.exceptions.ProfileHasNoPicsException:
        update.message.reply_text("L'utente non ha foto profilo")
    except:
        generic_error(update, context)
    
def purge (update, context):
    logger.info ("%s has purged the cache", update.message.from_user.username)
    if os.path.exists('images'):
        shutil.rmtree('images')
        update.message.reply_text('Cache svuotata con successo ✅')
    else:
        update.message.reply_text('Già tutto pulito 🧹\n')


def error(update, context):
    update.message.reply_text('Errore nel testo digitato ⚠️\n''Verificate di aver anteposto la @ al nome utenre e non aver inserito maiuscole o caratteri speciali diversi da quelli consentiti 🚧')


# main function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("purge", purge))
    dp.add_handler(CommandHandler ("help", help))
    dp.add_handler(MessageHandler(Filters.regex ('@[a-z0-9+\.+\_]*'), downloader))
    dp.add_handler(MessageHandler (Filters.text, error))
    
    dp.add_error_handler(generic_error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


#Funzioni di Supporto 

def generic_error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('500 Internal Server Error; Se il problema persiste si prega di avvisare il server admin\n')



if __name__ == '__main__':
    main()