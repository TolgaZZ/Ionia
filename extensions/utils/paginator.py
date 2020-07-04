import asyncio
import discord


class Paginator:
    def __init__(self, ctx, embeds: list):
        self.ctx = ctx
        self.embeds = embeds
        self.max_page = len(embeds)
        self.current_page = 1
        self.reactions = [
            ('⏪', self.first_page),
            ('◀️', self.previous_page),
            ('▶️', self.next_page),
            ('⏩', self.last_page),
        ]

    async def setup(self):
        embed = self.embeds[0]
        embed.set_footer(text=f'Page 1/{self.max_page}')
        self.message = await self.ctx.channel.send(embed=embed)

        if len(self.embeds) == 1:
            return

        for r, _ in self.reactions:
            await self.message.add_reaction(r)

    async def alter_page(self, page):
        embed = self.embeds[page - 1]
        embed.set_footer(text=f'Page {self.current_page}/{self.max_page}')
        await self.message.edit(embed=embed)

    async def first_page(self):
        self.current_page = 1
        await self.alter_page(self.current_page)

    async def previous_page(self):
        if self.current_page == 1:
            self.current_page = self.max_page
            await self.alter_page(self.current_page)
        else:
            self.current_page -= 1
            await self.alter_page(self.current_page)

    async def next_page(self):
        if self.current_page == self.max_page:
            self.current_page = 1
            await self.alter_page(self.current_page)
        else:
            self.current_page += 1
            await self.alter_page(self.current_page)

    async def last_page(self):
        self.current_page = self.max_page
        await self.alter_page(self.current_page)

    def check(self, reaction, user):
        if user.id != self.ctx.author.id:
            return False
        if reaction.message.id != self.message.id:
            return False

        for emoji, function in self.reactions:
            if reaction.emoji == emoji:
                self.page_func = function
                return True
        return False

    async def paginate(self):
        await self.setup()
        while True:
            try:
                reaction, user = await self.ctx.bot.wait_for(
                    'reaction_add', check=self.check, timeout=120
                )
            except asyncio.TimeoutError:
                await self.message.clear_reactions()

            try:
                await self.message.remove_reaction(reaction, user)
            except discord.HTTPException:
                pass
            await self.page_func()
