import discord
from settings import ffmpeg_options
import asyncio

async def play_next_song(voice_client, queues, message):
    if len(queues) > 0:
        next_song_url = queues.pop(0)
        player = discord.FFmpegOpusAudio(next_song_url, **ffmpeg_options)
        voice_client.play(player, after=lambda e: asyncio.run(play_next_song(voice_client, queues, message)))
    else:
        await message.channel.send("No hay mas elementos en la cola")

