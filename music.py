import discord
from settings import TOKEN
from commands.pause import pause_command
from commands.play import play_command
from commands.resume import resume_command
from commands.stop import stop_command
from commands.skip import skip_command



def run_bot():
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)
        queues = []
        voice_clients = {}

        @client.event
        async def on_ready():
            print(f'{client.user} esta ahora corriendo!')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            command, *args = message.content.split()

            if command == "?play":
                if not args: 
                    await message.channel.send("Debes incluir la url después del comando.")
                    return
                await play_command(voice_clients, message, args, queues)
            elif command == "?pause":
                await pause_command(voice_clients, message)
            elif command == "?resume":
                await resume_command(voice_clients, message)
            elif command == "?skip":
                await skip_command(voice_clients, message, queues)
            elif command == "?stop":
                await stop_command(voice_clients, message)
            else:
                await message.channel.send("Comando no reconocido")

        client.run(TOKEN)

    except Exception as e:
        print("Ocurrió un error:", e)
