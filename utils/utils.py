import discord
import asyncio
import os
import shutil  
from pytube import YouTube


async def play_next_song(ctx, queues):
    if queues:
        song = queues.pop(0)
        if ctx.voice_client and ctx.voice_client.is_playing():
            return 
        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            voice_channel = await voice_channel.connect()
        ctx.voice_client.play(discord.FFmpegOpusAudio(song), after=lambda e: asyncio.run(play_next_song(ctx, queues)))


def delete_audio():
    shutil.rmtree('music')

def delete_first_song():
    music_dir = 'music'
    if os.path.exists(music_dir) and os.path.isdir(music_dir):
        songs = os.listdir(music_dir)
        if songs:
            first_song = os.path.join(music_dir, songs[0])
            os.remove(first_song)


def find_music_name(url):
    try:
        yt = YouTube(url)
        video_title = yt.title
        music_dir = 'music'
        if os.path.exists(music_dir) and os.path.isdir(music_dir):
            for filename in os.listdir(music_dir):
                if video_title in filename:
                    return os.path.join(music_dir, filename)
            print(f"No se encontró ningún archivo con el título '{video_title}'.")
            return None
        else:
            print("La carpeta de música no existe.")
            return None
    except Exception as e:
        print(f"Error al buscar el nombre del archivo de música: {e}")
        return None


def remove_all_files(dir):
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))



def download_vid(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first() 
    audio_stream.download(output_path='music')