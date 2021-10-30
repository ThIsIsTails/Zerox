import discord
import os
from tools.json_reader import json
import datetime

client = None


def check_perms(author: discord.Member, permission: str) -> bool:
    """
    Чекает права через settings.json и если указаного парва нету то вернёт false.

    :param author: Юзер который использует команду.
    :param permission: Право которое нужно.
    :return: Может ли юзер использовать команду или нет (True/False).
    """

    js = json(os.path.join("./settings.json")).get_list()["permissions"]

    return author.id in js[permission]


def ts() -> datetime:
    return datetime.datetime.now(datetime.timezone.utc)


async def log_channel(embed: discord.Embed):
    await client.get_channel(id=903727885209174106).send(embed=embed)
