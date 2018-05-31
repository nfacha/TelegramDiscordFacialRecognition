# -*- coding: utf-8 -*-
import logging
import os

import face_recognition
from telegram import Bot, ParseMode
from telegram import Message
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

upd = None  # type: Updater
def init():
    import sys
    if sys.version_info[0] < 3:
        print("Python3 is required!")
        sys.exit(0)
    updater = Updater(os.getenv("api-key"))

    dp = updater.dispatcher
    dp.add_error_handler(error)
    dp.add_handler(MessageHandler(Filters.photo, execute))
    updater.start_polling()
    print("Bot is listening")

def execute(bot,update):
    """

    :type bot: telegram.bot.Bot
    """
    message = update.message  # type: Message
    print(message)
    print("Received file from "+message.from_user.username)
    update.message.reply_text("Please wait, processing...", parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    file = bot.get_file(update['_effective_message']['photo'][-1]['file_id'])
    name = "tmp/"+file.file_id+"."+str(file.file_path).split(".")[-1];
    print(name)
    file.download(name)
    found = False
    print("Initializing recognition...")
    for filename in os.listdir("known-person"):
        image = face_recognition.load_image_file("known-person/" + filename)
        unknown_image = face_recognition.load_image_file(name)
        try:
            image_encoding = face_recognition.face_encodings(image)[0]
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            known_faces = [
                image_encoding
            ]
            results = face_recognition.compare_faces(known_faces, unknown_face_encoding, tolerance=0.6)

            if results[0]:
                print("MATCH // Positive ID against sample known-person/" + filename)
                response = "✅ Facial recognition match! -> " + filename
                found = True
                break
            else:
                print("NO MATCH // against sample known-person/" + filename)

        except IndexError:
            pass
    if not found:
        response = "❓ No facial recognition match found"
        print("No results found")
    print("-------------------")
    update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


    pass


def spin():
    init()
    keepUp = True
    while keepUp:
        command = input()
        if command == "stop":
            keepUp = False


