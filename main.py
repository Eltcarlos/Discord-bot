import discord
from utils.utils import play_next_song,  download_vid, find_music_name, remove_all_files


from discord.ext import commands
from settings import TOKEN



intents = discord.Intents.all() #allowing all intents
intents.members = True
bot = commands.Bot(command_prefix = "!",help_command=None,intents = intents)
queues = []

@bot.event
async def on_ready():
    try:
        print(f'{bot.user} esta ahora corriendo!')
    except:
        print("[!] Couldn't connect, an Error occured")
        
@bot.command(name="play")
async def play(ctx, *, url=None):
    try:
        if url is None:
            embed = discord.Embed(
                title="Error ❌",
                description="la url de la canción es requerida. el comando correcto es !play url",
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)
        download_vid(url)
        voice_channel = ctx.author.voice.channel
        if not ctx.voice_client:
            voice_channel = await voice_channel.connect()

        song = find_music_name(url)

        queues.append(song)
        
        if not ctx.voice_client.is_playing() and len(queues) > 0:
            await play_next_song(ctx, queues)
        
        embed = discord.Embed(
            title="Canción agregada ✅",
            description=f"Se agregó la canción a la cola: {url}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
                
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"Tuvimos un error al ejecutar el comando play: {e}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name="skip")
async def skip(ctx):
    try:
        if len(queues) == 0:
            embed = discord.Embed(
                title="Error ❌",
                description="No hay ninguna canción reproduciéndose actualmente.",
                color=discord.Color.red()
            )
            remove_all_files("music")
            return await ctx.send(embed=embed)

        ctx.voice_client.stop()
        await play_next_song(ctx, queues)

    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"Tuvimos un error al ejecutar el comando skip: {e}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)



@bot.command(name="stop")
async def stop(ctx):
    try:
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        remove_all_files("music")
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"Tuvimos un error al ejecutar el comando stop: {e}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)



@bot.command(name="pause")
async def pause(ctx):
    try:
        await ctx.voice_client.pause()
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"Tuvimos un error al ejecutar el comando pause: {e}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)



@bot.command(name="resume")
async def resume(ctx):
    try:
        ctx.voice_client.resume()
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f"Tuvimos un error al ejecutar el comando resume: {e}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


bot.run(TOKEN)