import datetime

import discord
import discord_slash
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from tools import utils


class say(commands.Cog):
    def __init__(self, client):
        self.client: discord.Client = client

    @cog_ext.cog_slash(
        name="say",
        guild_ids=[903684277064069151],
        description="Говорит от имни бота",
        options=
        [
            {
                "choices": [
                    {
                        "value": "default",
                        "name": "Дефолт (Голубой)"
                    },
                    {
                        "value": "background",
                        "name": "Фон"
                    },
                    {
                        "value": "yellow",
                        "name": "Жёлтый"
                    },
                    {
                        "value": "green",
                        "name": "Зелёный"
                    },
                    {
                        "value": "red",
                        "name": "Красный"
                    },
                ],
                "name": "color",
                "type": 3,
                "required": True,
                "description": "Цвет",
            },
            {
                "name": "description",
                "type": 3,
                "required": False,
                "description": "Описание"
            },
            {
                "name": "title",
                "type": 3,
                "required": False,
                "description": "Заголовок"
            },
            {
                "name": "large_image",
                "type": 3,
                "required": False,
                "description": "URL изображения"
            }
        ]
    )
    async def _say(self, ctx: SlashContext,
                   description: str = None,
                   title: str = None,
                   color: str = "default",
                   large_image = None):

        if not utils.check_perms(ctx.author, "say"):
            embed = discord.Embed(
                title="Error: Permissions needed",
                description="У вас отсутствует право SAY для использования этой команды.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            await ctx.reply(embed=embed)
            return

        c = None

        if color == "default":
            c = discord.Color.blue()
        elif color == "yellow":
            c = discord.Color.gold()
        elif color == "red":
            c = discord.Color.red()
        elif color == "green":
            c = discord.Color.green()
        elif color == "background":
            c = discord.Color.from_rgb(48, 49, 54)

        embed = discord.Embed(
            title=title,
            description=description,
            color=c
        )

        if title is None:
            embed = discord.Embed(
                description=description,
                color=c
            )

        if description is None:
            embed = discord.Embed(
                color=c
            )

        if large_image is not None:
            embed.set_image(url=large_image)

        await self.client.get_channel(id=ctx.channel_id).send(embed=embed)
        await ctx.send("Готово", hidden=True)

def setup(client):
    client.add_cog(say(client))
