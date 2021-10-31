import datetime
import os.path

import discord
import discord_slash
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, SlashCommandOptionType
from discord_components import *
from tools import utils, json_reader


class say(commands.Cog):
    def __init__(self, client):
        self.client: discord.Client = client

    @cog_ext.cog_slash(
        name="edit_role",
        guild_ids=[903684277064069151],
        description="Изменяет права роли и не только",
        options=
        [
            {
                "name": "role",
                "type": 8,
                "description": "Роль которую нужно править.",
                "required": True
            }
        ]
    )
    async def _manage_role_edit(self, ctx, role):

        if not utils.check_perms(ctx.author, "all"):
            embed = discord.Embed(
                title="Error: Permissions needed",
                description="У вас отсутствует право ALL для использования этой команды.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            await ctx.reply(embed=embed)
            return

        embed = discord.Embed(
            title = "Правление над " + role.name,
            description = "Выберите действие с помощью кнопок ниже.",
            color = discord.Color.blue(),
            timestamp=utils.ts()
        )

        buttons = [
            Button(label="Добавить/удалить права", custom_id="add_perms"),
            Button(label="Переименовать", custom_id="role_rename"),
            Button(label="Удалить", custom_id="role_delete")
        ]

        await ctx.reply(embed=embed,
                       components=buttons,
                       hidden=False)

        def cog_check(i):
            if not i.custom_id == "add_perms" or i.custom_id == "role_rename" or i.custom_id == "role_delete":
                return

        ref: Interaction = await self.client.wait_for("button_click",
        check=lambda i: i.custom_id == "add_perms" or i.custom_id == "role_rename" or i.custom_id == "role_delete")

        if ref.custom_id == "add_perms":

            js = json_reader.json(os.path.join(f"roles/{role.id}.json")).get_list()

            if js["permissions"]["all"]:
                buttons = [
                    Button(label="ALL [Все права]", custom_id="perms_all", style=ButtonStyle.green),
                    Button(label="SAY [Писать от имени бота]", custom_id="perms_say", style=ButtonStyle.red, disabled=True),
                    Button(label="MANAGE ROLE EDIT [Эта команда]", custom_id="perms_mre", style=ButtonStyle.red, disabled=True)
                ]
            else:
                buttons = [
                    Button(label="ALL [Все права]", custom_id="perms_all",
                           style= ButtonStyle.red),

                    Button(label="SAY [Писать от имени бота]", custom_id="perms_say",
                           style= ButtonStyle.green if js["permissions"]["say"] else ButtonStyle.red,
                           disabled=True),

                    Button(label="MANAGE ROLE EDIT [Эта команда]", custom_id="perms_mre",
                           style= ButtonStyle.green if js["permissions"]["mre"] else ButtonStyle.red,
                           disabled=True)
                ]

            embed=discord.Embed(
                title = "Правление прав",
                description = "Зелёная кнопк - право доступно\nКрасная кнопка - право недоступно",
                color = discord.Color.blue(),
                timestamp = utils.ts()
            )

            await ref.send(type=7, embed = embed, components=buttons)

def setup(client):
    client.add_cog(say(client))
