import discord
from dotenv import load_dotenv
import os
from discord.commands.context import ApplicationContext as AppCtx

def contains_audio_attatchment(ctx : discord.Message):
    """Validate that the message has an audio attachment"""
    if len(ctx.attachments) == 1:
        if ctx.attachments[0].content_type.startswith("audio"):
            return True
    return False

def is_temaikens_channel(ctx : discord.Message):
    """Validate that the message was sent in the Temaikens channel"""
    load_dotenv() # load all the variables from the env file
    TEMAIKENS_CHANNEL_ID = int(os.environ.get("TEMAIKENS_CHANNEL_ID"))
    return ctx.channel.id == TEMAIKENS_CHANNEL_ID

def is_human(ctx : discord.Message):
    """Validate that the message was not sent by a bot"""
    return not ctx.author.bot

def is_admin(ctx : AppCtx):
    """Validate that the user has the Admin role"""
    return ctx.author.guild_permissions.administrator