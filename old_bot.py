from discord_cah import SeverGame
import discord
from discord.ext import commands
import os

"""
This is a test script to run the discord bot in a specified channel.

Make sure to define the environment variables:
 * DISCORD_CAH_BOT_TOKEN: The discord bot token
"""

bot = commands.Bot(command_prefix='?', description="A Cards Bot.")

gms = []

async def start_session(channel_id):
    g = SeverGame(bot, channel_id.id, reg_msg_method=False)
    gms.append(g)
    bot.loop.create_task(g.run())


@bot.event
async def on_message(*args, **kwargs):
    msg = args[0]
    author = msg.author
    if author == bot.user:
        return

    await bot.process_commands(*args, **kwargs)

    for g in gms:
        await g.on_message(*args, **kwargs)


@bot.command(pass_context=True)
async def start(ctx):
    """Starts a game."""
    channel = ctx.message.channel

    if type(channel) == discord.channel.PrivateChannel:
        await bot.say("I'm afraid you can't start a fantastical game by yourself. Sorry lad.")
    else:
        print("non")
        await start_session(ctx.message.channel)
    print("done")


@bot.event
async def on_ready():
    # Set command prefix to be @ mentioning it:
    bot.command_prefix = "<@{}> ".format(bot.user.id)

    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(os.environ['DISCORD_CAH_BOT_TOKEN'])
