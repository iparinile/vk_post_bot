import os

from dotenv import load_dotenv
from pyrogram import Client, types

from work_with_text.correction_text_of_post import correction_text_of_post

load_dotenv()

api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")

app = Client("my_account", api_id=api_id, api_hash=api_hash)

CHANNEL_ID_FROM = int(os.getenv("CHANNEL_ID_FROM"))
CHANNEL_ID_TO = int(os.getenv("CHANNEL_ID_TO"))

current_media_group_id = 0


@app.on_message()
def my_handler(client: Client, message: types.Message):
    global current_media_group_id
    if message.chat.id == CHANNEL_ID_FROM:
        if message.media_group_id is not None:
            if message.media_group_id != current_media_group_id:
                current_media_group_id = message.media_group_id
                caption_text = message.caption
                if caption_text is not None:
                    caption_text = correction_text_of_post(caption_text)
                app.copy_media_group(CHANNEL_ID_TO, message.chat.id, message.id, caption_text)
        elif (message.photo is not None) or (message.video is not None):
            caption_text = message.caption
            if caption_text is not None:
                caption_text = correction_text_of_post(caption_text)
            app.copy_message(CHANNEL_ID_TO, message.chat.id, message.id, caption_text)
        else:
            if message.text is not None:
                text = correction_text_of_post(message.text)

                app.send_message(chat_id=CHANNEL_ID_TO, text=text)


app.run()
