import os
import discord
from discord.ext import commands
from discord_cah import SeverGame


class CardsBot(commands.Bot):
    def __init__(self, token=None, formatter=None, pm_help=False, **options):
        description = "A bot which allows for card games to be played."
        super().__init__("c: ", formatter, description, pm_help, **options)

        if token is None:
            self.token = os.environ['DISCORD_CAH_BOT_TOKEN']
        else:
            self.token = token

        self.gms = []

        # Register commands:
        self.start_game = self.group(name="start", pass_context=True)(self.start_game)
        self.start_game.command(name="cah", pass_context=True)(self.start_cah_game)
        pass

    def create_session(self, channel_id):
        g = SeverGame(self, channel_id.id, reg_msg_method=False)
        self.gms.append(g)
        self.loop.create_task(g.run())
        pass

    async def on_message(self, *args, **kwargs):
        msg = args[0]
        author = msg.author
        if author == self.user:
            return
        await self.process_commands(*args, **kwargs)

        for g in self.gms:
            await g.on_message(*args, **kwargs)

    async def start_game(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.say('Invalid start command passed...')

    async def start_cah_game(self, ctx):
        """Starts a game."""
        channel = ctx.message.channel

        if type(channel) == discord.channel.PrivateChannel:
            await self.say("I'm afraid you can't start a fantastical game by yourself. Sorry.")
        else:
            self.create_session(ctx.message.channel)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    def start_bot(self):
        self.run(self.token)

