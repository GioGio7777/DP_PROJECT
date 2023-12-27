# Importing necessary modules and classes
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands


# Singleton metaclass to ensure a single instance of BotConnection
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Create a new instance if it doesn't exist
            instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# Singleton class for handling Discord bot connection
class BotConnection(metaclass=SingletonMeta):

    def __init__(self):
        self.client = None

    @staticmethod
    def bot_connection():
        # Configuring Discord intents to enable specific events
        intents = discord.Intents.all()
        intents.message_content = True

        # Loading environment variables from .env file
        load_dotenv()
        bot_token = os.getenv("BOT_TOKEN")

        # Creating a new Discord client with commands extension
        discord.Client(intents=intents)
        client = commands.Bot(command_prefix="!", intents=intents)
        return client, bot_token

    def run_bot(self):
        # Running the bot if it hasn't been initialized yet
        if self.client is None:
            client, token = self.bot_connection()
            client.run(token)
            return client


# Main execution block
if __name__ == "__main__":
    # Creating a singleton instance of BotConnection
    bot_connection_instance = BotConnection()

    # Running the bot
    bot = bot_connection_instance.run_bot()
