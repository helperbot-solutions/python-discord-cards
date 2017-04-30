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

        # Holds the games {channel_id: game_object}:
        self.gms = {}

        # Register commands:
        self.start_game = self.group(name="start", pass_context=True)(self.start_game)
        self.start_game.command(name="cah", pass_context=True)(self.start_cah_game)
        self.end_game = self.command(name="end", pass_context=True)(self.end_game)
        pass

    async def game_end_callback(self, game):
        channel_id = game.channel_id
        if channel_id not in self.gms:
            # Not in games (this is an error)
            return

        del(self.gms[channel_id])

    async def on_message(self, *args, **kwargs):
        msg = args[0]
        author = msg.author
        if author == self.user:
            return
        await self.process_commands(*args, **kwargs)

        for g in self.gms:
            await self.gms[g].on_message(*args, **kwargs)

    async def start_game(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.say('Invalid start command passed...')

    async def start_cah_game(self, ctx):
        """Starts a game."""
        channel_id = ctx.message.channel.id
        if channel_id in self.gms:
            await self.gms[channel_id].end()
        self.gms[channel_id] = SeverGame.create_session(self, ctx.message, self.game_end_callback)

    async def end_game(self, ctx):
        channel_id = ctx.message.channel.id
        if channel_id in self.gms:
            await self.gms[channel_id].end()

        await self.say("Game successfully terminated.")

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    def start_bot(self):
        self.run(self.token)

