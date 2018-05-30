import os
import urllib.request
from typing import Optional, Any
from tqdm import tqdm
import discord
import requests
from discord import Channel
from discord import Client
from discord import Server
from discord.utils import get
import face_recognition

import Utils

client = discord.Client()  # type: Client

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="TOP SECRET"))
    channel = client.get_channel("445990794852302892")  # type: Channel
    await client.send_message(destination=channel, content="Loaded and ready!", tts=True)
    # await channel.send("Loaded and ready")

@client.event
async def on_message(message):
    """

    :type message: discord.message.Message
    """
    if Utils.isStaff(message.author) or message.channel.id == "451418762332209153":
        if len(message.attachments) != 0:
            print(message.embeds)
            for attachment in message.attachments:
                msg = await client.send_message(message.channel, "Downloading file...")
                name = str(attachment['url']).split("/")
                name = attachment['id']+"_"+name[len(name)-1]
                headers = {
                    'User-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
                }
                response = requests.get(attachment['proxy_url'], stream=True, headers=headers)
                with open("tmp/"+name, "wb") as handle:
                    for data in tqdm(response.iter_content()):
                        handle.write(data)
                await client.edit_message(msg, "Downloaded as /tmp/"+name+", processing please wait...")
                found = False
                for filename in os.listdir("known-person"):
                    image = face_recognition.load_image_file("known-person/"+filename)
                    unknown_image = face_recognition.load_image_file("tmp/"+name)
                    try:
                        image_encoding = face_recognition.face_encodings(image)[0]
                        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
                        known_faces = [
                            image_encoding
                        ]
                        results = face_recognition.compare_faces(known_faces, unknown_face_encoding, tolerance=0.6)

                        if results[0]:
                            await client.edit_message(msg, ":white_check_mark:  Facial recognition match! -> " + filename)
                            found = True
                            break

                    except IndexError:
                        await client.edit_message(msg, ":x: Unable to trace")
                if not found:
                    await client.edit_message(msg, ":question: No facial recognition match found")




    # if message.content.startswith('!svinfo'):
    #     await SvInfoCommand().svInfo(message, client, apiClient)
    # if message.content.startswith('!ping'):
    #     await PingCommand().svInfo(message, client, apiClient)
    # if message.content.startswith('!connect'):
    #     await ConnectCommand().connect(message, client, apiClient)
    # if message.content.startswith('!verify'):
    #     await VerifyCommand().verify(message, client, apiClient)
    # if message.content.startswith('!srv'):
    #     await SrvCommand().resolve(message, client)

client.run('NDUxMzg3NjcyOTg5MTM4OTQ1.DfBD2w.E5Y7ZUjl3-eZmUjtZrk-7jTh11w')