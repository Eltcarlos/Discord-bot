from utils.next_song import play_next_song

async def skip_command(voice_clients, message, queues):
    try:
        guild_id = message.guild.id
        if guild_id not in voice_clients:
            await message.channel.send("El bot no está en un canal de voz.")
            return
        
        voice_client = voice_clients[guild_id]

        if len(queues) == 0:
            await message.channel.send("No hay canciones en la cola para saltar.")
            return
        
        await message.channel.send("Canción saltada.")
        voice_client.stop()
        
        await play_next_song(voice_clients, queues, message)
    except Exception as e:
        print(e)
