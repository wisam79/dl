# Ā© TamilBots 2021-22

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
import youtube_dl
from youtube_search import YoutubeSearch
import requests

import os
from config import Config

bot = Client(
    'SongPlayRoBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

## Extra Fns -------------------------------

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------------------------------
@bot.on_message(filters.command(['start']))
def start(client, message):
    TamilBots = f'š šš²š¹š¹š¼ @{message.from_user.username}\n\nš ššŗ šøššØš§š  šš„šš² ššØš­[š¶](https://telegra.ph/file/6cb884fe1cb943ec12df1.mp4)\n\nš¦š²š»š± š§šµš² š”š®šŗš² š¢š³ š§šµš² š¦š¼š»š“ š¬š¼š šŖš®š»š... šš„°š¤\n\nš§šš½š² /s š¦š¼š»š“ š”š®šŗš²\n\nšš . `/s Faded`'
    message.reply_text(
        text=TamilBots, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('ššššššš š¬', url='https://t.me/wsh23'),
                    InlineKeyboardButton('ššš šš š¤', url='https://t.me/YTubeSR_bot?startgroup=true')
                ]
            ]
        )
    )

@bot.on_message(filters.command(['s']))
def a(client, message):
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply('š šššš«šš”š¢š§š  š­š”š š¬šØš§š ...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('ššØš®š§š ššØš­š”š¢š§š . šš«š² šš”šš§š š¢š§š  šš”š šš©šš„š„š¢š§š  š šš¢š­š­š„š š')
            return
    except Exception as e:
        m.edit(
            "āļø ššØš®š§š ššØš­š”š¢š§š . ššØš«š«š².\n\nšš«š² šš§šØš­š”šš« ššš²š°šØš«š¤ šš« ššš²šš šš©šš„š„ šš­ šš«šØš©šš«š„š².\n\nEg.`/s Faded`"
        )
        print(str(e))
        return
    m.edit("š šš¢š§šš¢š§š  š ššØš§š  š¶ šš„ššš¬š ššš¢š­ ā³ļø ššØš« ššš° ššššØš§šš¬ [š](https://telegra.ph/file/67f41ae52a85dfc0551ae.mp4)")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'š§ šš¢š­š„š : [{title[:35]}]({link})\nā³ šš®š«šš­š¢šØš§ : `{duration}`\nš¬ ššØš®š«šš : [Youtube](https://youtu.be/3pN0W4KzzNY)\nšāšØ šš¢šš°š¬ : `{views}`\n\nš šš² : @SongPlayRoBot'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('ā šš«š«šØš«\n\n Report This Erorr To Fix @TamilSupport ā¤ļø')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
