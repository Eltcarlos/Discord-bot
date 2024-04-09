async def stop_command(voice_clients, message):
    try:
        voice_clients[message.guild.id].stop()
        await voice_clients[message.guild.id].disconnect()
    except Exception as e:
        print(e)