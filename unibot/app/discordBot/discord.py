from dotenv import load_dotenv
import discord
import os
from app.gptBot.gpt import chat_response
load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')

class DClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        print(message.content)
        if message.author == self.user:
            return
    
        command, user_message = None, None

        command_key = [self.user.mention,'/bot']
        for text in command_key:
            if message.content.startswith(text):
                command = text
                user_message = message.content[len(text):].strip()

        if command == '/lecture':
            pass

        if command == '/bot' or command == self.user.mention:
            bot_response = chat_response(prompt=user_message)
            if len(bot_response) > 2000:
                parts = bot_response.split('\n')
                current_message = ""
                for part in parts:
                    if len(current_message) + len(part) + 1 > 2000:
                        await message.channel.send(current_message)
                        current_message = ""
                    current_message += part + "\n"
                if current_message:
                    await message.channel.send(current_message)
            else:
                await message.channel.send(bot_response)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = DClient(intents=intents)