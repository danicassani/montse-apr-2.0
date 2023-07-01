import discord
from dotenv import load_dotenv
import os
from discord.commands.context import ApplicationContext as AppCtx


def contains_audio_attatchment(ctx: discord.Message):
    """Validate that the message has an audio attachment"""
    if len(ctx.attachments) == 1:
        if ctx.attachments[0].content_type.startswith("audio"):
            return True
    return False


def is_temaikens_channel(ctx: discord.Message):
    """Validate that the message was sent in the Temaikens channel"""
    load_dotenv()  # load all the variables from the env file
    TEMAIKENS_CHANNEL_ID = int(os.environ.get("TEMAIKENS_CHANNEL_ID"))
    return ctx.channel.id == TEMAIKENS_CHANNEL_ID


def is_bot(ctx: discord.Message):
    """Validate that the message was not sent by a bot"""
    return ctx.author.bot


def is_reference_to_audio_file(ctx: discord.Message, bot: discord.Bot):
    """Validate that the message is a reference"""
    if ctx.reference is None:
        return False
    ref: discord.message.MessageReference = ctx.reference
    ref_msg: discord.Message = bot.get_message(ref.message_id)

    return contains_audio_attatchment(ref_msg)


def not_allowed_message(ctx: discord.Message, bot: discord.Bot):
    """Validate that the message is not allowed"""
    return is_temaikens_channel(ctx) and not (contains_audio_attatchment(ctx) or is_reference_to_audio_file(ctx, bot))


def is_temaiken(ctx: discord.Message):
    return is_temaikens_channel(ctx) and contains_audio_attatchment(ctx)
