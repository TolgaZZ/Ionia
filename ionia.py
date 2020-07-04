from discord.ext import commands
import cassiopeia
import config
import discord
import sys
import traceback


class Ionia(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=config.prefix, case_insensitive=True)
        self.load_extensions()
        self.cassiopeia = cassiopeia
        cassiopeia.set_riot_api_key(config.api_key)

    def load_extensions(self):
        for extension in config.extensions:
            try:
                self.load_extension(extension)
            except Exception:
                print(
                    f"Extension '{extension}' failed to load",
                    file=sys.stderr
                )
                traceback.print_exc()

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        print(f'Using version {discord.__version__} of discord.py')

    async def on_command_error(self, ctx, error):
        print(error)
        if hasattr(error, 'original') and 'query' in str(error.original):
            await ctx.send(f'Summoner `{ctx.args[3]}` does not exist')
        elif hasattr(error, 'original') and isinstance(error.original, ValueError):
            await ctx.send(f'`{ctx.args[2]}` is not a valid region')
        elif isinstance(error, commands.CommandInvokeError):
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print(
                f'{error.original.__class__.__name__}: {error.original}',
                file=sys.stderr
            )

    def run(self):
        super().run(config.token)


if __name__ == '__main__':
    ionia = Ionia()
    ionia.run()
