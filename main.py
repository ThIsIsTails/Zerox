import datetime
import os

import discord
from discord.ext.commands import Bot

from discord_slash import SlashCommand

from discord_components import *

from tools import utils
from tools.json_reader import json

client = Bot(command_prefix="!", intents=discord.Intents.all())
utils.client = client
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    DiscordComponents(client)
    print("There sessions starts")

@client.command()
async def cog(ctx, param, file):
    if not utils.check_perms(ctx.author, "all"):
        embed = discord.Embed(
            title = "Error: Permissions needed",
            description = "У вас отсутствует право ALL для использования этой команды.",
            color = discord.Color.red(),
            timestamp = datetime.datetime.now(datetime.timezone.utc)
        )
        await ctx.reply(embed=embed)
        return

    if param == "load":
        try:
            client.load_extension(f"commands.{file}")
            print(f"Extension {file} was loaded.")
            await ctx.message.add_reaction(":white_check_mark:")
            return
        except Exception as error:
            embed = discord.Embed(
                title="Error: Extension error",
                description=f"Во время загрузки произошла ошибка.\n```py\n{error}\n```",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            await ctx.reply(embed=embed)
            return
    elif param == "reload":
        try:
            client.reload_extension(f"commands.{file}")
            print(f"Extension {file} was reloaded.")
            await ctx.message.add_reaction(":white_check_mark:")
            return
        except Exception as error:
            embed = discord.Embed(
                title="Error: Extension error",
                description=f"Во время перезагрузки произошла ошибка.\n```py\n{error}\n```",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            await ctx.reply(embed=embed)
            return
    elif param == "unload":
        try:
            client.unload_extension(f"commands.{file}")
            print(f"Extension {file} was unloaded.")
            await ctx.message.add_reaction(":white_check_mark:")
            return
        except Exception as error:
            embed = discord.Embed(
                title="Error: Extension error",
                description=f"Во время отгрузки произошла ошибка.\n```py\n{error}\n```",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            await ctx.reply(embed=embed)
            return
    else:
        await ctx.reply("Not founded param.")

for i in os.listdir("./commands"):
    if i.endswith(".py"):
        client.load_extension(f"commands.{i[:-3]}")
        print(f"{i} loaded successfully")

client.run(json("./settings.json").get_list()["token"])