import discord

from discord.commands.context import ApplicationContext as AppCtx
from discord.message import Message as Msg
from discord.ext.commands import Group

import json
import random

import os # default module
from dotenv import load_dotenv
from utils.validators import contains_audio_attatchment, is_temaikens_channel, is_human, is_admin
from utils.constants import MODERATION_PHRASES, MONTSE_PHRASES

load_dotenv() # load all the variables from the env file
TEMAIKENS_CHANNEL_ID = int(os.environ.get("TEMAIKENS_CHANNEL_ID"))
# Intent permissions
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    print(f"Temaikens channel id is {TEMAIKENS_CHANNEL_ID}")

@bot.event
async def on_message(msg : Msg):
    print(f"{msg.author}: {msg.content}")

    if not is_human(msg):
        return
    
    if "montse" in msg.content.lower():
        montse_phrase = random.choice(MONTSE_PHRASES)
        await msg.channel.send(montse_phrase, delete_after=5)
    
    if is_temaikens_channel(msg) and not contains_audio_attatchment(msg):
        await msg.channel.send(f"{msg.author.mention} Mensaje no permitido.", delete_after=5)
        await msg.author.send(MODERATION_PHRASES["no_temaiken"])
        await msg.delete()
    
@bot.slash_command(name = "hola", description = "Es Montse, ¿O quizá no...?")
async def hola(ctx : AppCtx):
    await ctx.respond("Hola, me llamo José Antonio.")

# This command needs a certain role: "Admin"

@bot.check(is_admin)
@bot.slash_command(name = "borrar", description = "Borra los últimos n mensajes del canal.")
async def borrar(ctx : AppCtx, n : int):
    print("Roles", ctx.author.roles)
    await ctx.channel.purge(limit=n+1)


bot.run(os.getenv('TOKEN')) # run the bot with the token