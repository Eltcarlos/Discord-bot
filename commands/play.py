import asyncio
import yt_dlp
from utils.next_song import play_next_song

async def play_command(voice_clients, message, args, queues):
    try:
        if message.author.voice is None or message.author.voice.channel is None:
            await message.channel.send("Debes estar en un canal de voz para utilizar este comando.")
            return


        voice_channel = message.author.voice.channel
        guild_id = message.guild.id
        
        if guild_id in voice_clients:
            voice_client = voice_clients[guild_id]
        else:
            voice_client = await voice_channel.connect()
            voice_clients[guild_id] = voice_client
    except Exception as e:
        print(e)

    try:
        url = args[0]
        
        loop = asyncio.get_event_loop()
        yt_dl_options = {"format": "bestaudio/best"}
        ytdl = yt_dlp.YoutubeDL(yt_dl_options)
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

        song = data['url']
        if song is None:
            await message.channel.send("Debes poner la url de tu canción.")

        queues.append(song)

        if len(queues) > 1:
            await message.channel.send(f'Posición de la cola #{len(queues)}')

        if not voice_client.is_playing() and len(queues) > 0:
            await play_next_song(voice_client, queues, message)

    except Exception as e:
        print(e)
