"""
Author: Konnor Klercke
File: latexbot.py
Purpose: Discord bot to typeset math
"""

#####################################
                                    #
import os                           #
import discord                      #
from dotenv import load_dotenv      #
from discord.ext import commands    #
from discord.ext import tasks       #
import logging                      #
import time
                                    #
#####################################


#################################################
                                                #
ACTIVITY = discord.Game("$Typesetting Time$")   #
LOG_LEVEL = logging.INFO                        #
COMMAND_PREFIX = '!'                            #
VERSION = "v0.0.1-alpha"                        #
                                                #
#################################################


# Initialize bot object to use the COMMAND_PREFIX defined above
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.event
async def on_connect():
    """
    Prints a message with bot name and version when bot connects to Discord servers.
    Sets the bot activity to ACTIVITY.
    """

    logging.warning(f'{bot.user.name} {VERSION} has successfully connected to Discord.')
    await bot.change_presence(activity = ACTIVITY)


@bot.event
async def on_ready():
    """
    Prints a list of guilds the bot is connected to when the bot is finished processing
    date from Discord servers.
    """

    logging.info('Bot loading complete. Current guilds: ')

    for guild in bot.guilds:
        label = guild.name + " (" + str(guild.id) + ")"
        logging.info(label)


@bot.event
async def on_disconnect():
    """
    Prints a message when bot disconnects from Discord. Usually this is temporary.
    """

    logging.warning('Lost connection to Discord.')


@bot.event
async def on_guild_join(guild):
    """
    Logs a message when bot joins a new guild and adds all users from that guild to the database.
    """

    logging.warning(f"Joined new guild: {guild.name + ' (' + str(guild.id) + ')'}")


@bot.event
async def on_error(event, *args, **kwargs):
    """
    Writes to err.log whenever a message triggers an error
    """

    if event == 'on_message':
        logging.error(f'Unhandled message: {args[0]}')
    else:
        logging.exception(event)



@bot.event
async def on_message(message):
    print(message.content)


def main():
    # Load bot token from .env
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # Generate timestamp of startup
    timestamp = time.strftime('%Y%m%d-%H%M%S')

    # Configure logging
    logging.basicConfig(
        level = LOG_LEVEL,
        format = '%(asctime)s: [%(levelname)s] - %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        handlers = [
            logging.FileHandler(f"logs/{timestamp}.log", mode = "w"),
            logging.StreamHandler()
        ]
    )

    bot.run(TOKEN)

if __name__ == "__main__":
    main()
