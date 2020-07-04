from discord.ext import commands
from extensions import utils
import discord
import urllib
import asyncio


discord.Guild.create_custom_emoji

class LoL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, region, username):
        region = region.upper()
        summoner = self.bot.cassiopeia.get_summoner(name=username, region=region)

        embed = discord.Embed()
        embed.set_thumbnail(url=summoner.profile_icon.url)
        embed.set_author(name=summoner.name, icon_url=summoner.profile_icon.url)
        embed.add_field(name='Level', value=summoner.level)
        embed.add_field(name='Region', value=region)
        await ctx.send(embed=embed)

    @commands.command()
    async def emoji(self, ctx):
        champions = self.bot.cassiopeia.get_champions('EUW')
        for champion in champions[100:150]:
            data = urllib.request.urlopen(champion.image.url).read()
            print(champion.name)
            await asyncio.sleep(20)
            await ctx.guild.create_custom_emoji(name=champion.name.replace(' ', '').replace("'", '').replace('.', '').replace('&', ''), image=data)

    @commands.command()
    async def masteries(self, ctx, region, username):
        region = region.upper()
        summoner = self.bot.cassiopeia.get_summoner(name=username, region=region)
        masteries = summoner.champion_masteries

        embeds = []
        while True:
            embed = discord.Embed()
            embed.set_thumbnail(url=summoner.profile_icon.url)
            embed.set_author(name=summoner.name, icon_url=summoner.profile_icon.url)

            index = (len(embeds) * 15, (len(embeds) + 1) * 15)
            emojis = [
                discord.utils.get(
                    self.bot.emojis,
                    name=mastery.champion.name
                        .replace(' ', '')
                        .replace("'", '')
                        .replace('.', '')
                        .replace('&', '')
                )
                for mastery in masteries[index[0]:index[1]]
            ]
            champ_names = [
                mastery.champion.name
                for mastery in masteries[index[0]:index[1]]
            ]
            champ_levels = [
                str(mastery.level)
                for mastery in masteries[index[0]:index[1]]
            ]
            champ_points = [
                str(mastery.points)
                for mastery in masteries[index[0]:index[1]]
            ]

            # How many characters fit onto an embed row
            embed_val = str()
            lists = [emojis, champ_names, champ_levels, champ_points]
            zip_list = zip(*lists)
            for emoji, name, level, points in zip_list:
                embed_val += f'{emoji} {name} {level} ({points})\n'
            embed.add_field(name='Masteries', value=embed_val)

            embeds.append(embed)
            if len(embeds) * 15 > len(masteries):
                break

        p = utils.Paginator(ctx, embeds)
        await p.paginate()


def setup(bot):
    bot.add_cog(LoL(bot))
