# -*- coding: utf-8 -*-

import os

import discord
import face_recognition
import requests
from discord import Client
from tqdm import tqdm

client = discord.Client()  # type: Client


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="TOP SECRET"))


@client.event
async def on_message(message):
    """

    :type message: discord.message.Message
    """
    if len(message.attachments) != 0:
        print("File received from %s" % message.author.name)
        for attachment in message.attachments:
            print("Downloading file...")
            msg = await client.send_message(message.channel, "Downloading file...")
            name = str(attachment['url']).split("/")
            name = attachment['id'] + "_" + name[len(name) - 1]
            headers = {
                'User-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
            }
            response = requests.get(attachment['proxy_url'], stream=True, headers=headers)
            with open("tmp/" + name, "wb") as handle:
                for data in tqdm(response.iter_content()):
                    handle.write(data)
            await client.edit_message(msg, "Downloaded as /tmp/" + name + ", processing please wait...")
            print("File saved as %s" % name)
            found = False
            print("Initializing recognition...")
            for filename in os.listdir("known-person"):
                image = face_recognition.load_image_file("known-person/" + filename)
                unknown_image = face_recognition.load_image_file("tmp/" + name)
                try:
                    image_encoding = face_recognition.face_encodings(image)[0]
                    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
                    known_faces = [
                        image_encoding
                    ]
                    results = face_recognition.compare_faces(known_faces, unknown_face_encoding, tolerance=0.6)

                    if results[0]:
                        print("MATCH // Positive ID against sample known-person/" + filename)
                        await client.edit_message(msg,
                                                  ":white_check_mark:  Facial recognition match! -> " + filename)
                        found = True
                        break
                    else:
                        print("NO MATCH // against sample known-person/" + filename)

                except IndexError:
                    pass
            if not found:
                await client.edit_message(msg, ":question: No facial recognition match found")
                print("No results found")
            print("-------------------")


print("Aye Aye, spinning up DISCORD bot")
print("TOKEN= "+os.getenv("apikey"))
client.run(os.getenv("apikey"))
