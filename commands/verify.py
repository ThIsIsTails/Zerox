import datetime

import discord
import discord_components
from discord.ext import commands

from discord_components import *

from tools import utils


class verif(commands.Cog):
    def __init__(self, client):
        self.client: discord.Client = client

    @commands.Cog.listener("on_member_join")
    async def join(self, member: discord.Member):
        embed = discord.Embed(
            title = "Пользователь присоединился",
            description = f"Пользователь {member.mention} ({member}) присоединился к серверу.",
            color = discord.Color.blue(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )

        role = discord.utils.get(member.guild.roles, name="noref")
        await member.add_roles(role, reason="Joined to the server")

        channel = self.client.get_channel(id=903727885209174106)
        await channel.send(embed=embed)

    @commands.Cog.listener("on_member_remove")
    async def leave(self, member: discord.Member):
        embed = discord.Embed(
            title="Пользователь вышел",
            description=f"Пользователь {member.mention} ({member}) вышел с сервера.",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )

        channel = self.client.get_channel(id=903727885209174106)
        await channel.send(embed=embed)

    @commands.Cog.listener("on_ready")
    async def ready(self):
        guild = self.client.get_guild(id=903684277064069151)
        channel = guild.get_channel(channel_id = 903700729078906911)

        await channel.purge(limit=1)

        embed = discord.Embed(
            title = "Пройдите верификацию",
            description = "Добро пожаловать на наш сервер! Чтобы получить полный доступ к серверу, надо нажать на кнопку ниже.",
            color = discord.Color.blue()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/903927793388236800/903927814867255336/1635583565997.png")

        buttons = [
            Button(label="Верифицироваться", custom_id="verify")
        ]

        await channel.send(embed=embed, components=buttons)

        while True:
            res: Interaction = await self.client.wait_for("button_click", check = lambda i: i.custom_id == "verify")

            if res.channel == channel:
                role = discord.utils.get(guild.roles, name="noref")
                await res.author.remove_roles(role, reason="Verified")

                embed=discord.Embed(
                    title = "Удачи тебе на нашем сервере!",
                    color = discord.Color.green()
                )

                await res.respond(type=4, embed=embed)

                embed =discord.Embed(
                    title = "Верифицорование",
                    description = f"Пользователь {res.author.mention} ({res.author}) верифицоровался и попал на сервер!",
                    color = discord.Color.blue(),
                    timestamp=utils.ts()
                )
                await utils.log_channel(embed)

def setup(client):
    client.add_cog(verif(client))
