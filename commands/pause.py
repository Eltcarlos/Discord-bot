async def pause_command(voice_clients, message):
    try:
        voice_clients[message.guild.id].pause()
    except Exception as e:
        print(e)
