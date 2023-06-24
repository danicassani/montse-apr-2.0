import discord

from discord.commands.context import ApplicationContext as AppCtx
from discord.message import Message as Msg

import random

import os # default module
from dotenv import load_dotenv
from utils.validators import not_allowed_message, is_temaikens_channel, is_bot
from utils.constants import MODERATION_PHRASES, MONTSE_PHRASES

from asgiref.sync import sync_to_async
from db.models import User, Warning

load_dotenv() # load all the variables from the env file
TEMAIKENS_CHANNEL_ID = int(os.environ.get("TEMAIKENS_CHANNEL_ID"))
TEMAIKEN_GUILD_ID=[int(os.environ.get("TEMAIKEN_GUILD_ID"))]
# Intent permissions
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.event
async def on_message(msg : Msg):
    print(f"{msg.author}: {msg.content}")
    user = await User.objects.filter(discord_user_id=msg.author.id).afirst()

    if is_bot(msg):
        return
    
    if not user:
        user = await User.objects.acreate(discord_user_id=msg.author.id)
        await user.asave()
    
    if "montse" in msg.content.lower() and not is_temaikens_channel(msg):
        montse_phrase = random.choice(MONTSE_PHRASES)
        await msg.channel.send(montse_phrase, delete_after=5)
    
    if not_allowed_message(msg, bot):
        await msg.delete()
        await msg.channel.send(f"{msg.author.mention} Mensaje no permitido.", delete_after=5)
        await msg.author.send(MODERATION_PHRASES["no_temaiken"])
        user = await User.objects.aget(discord_user_id=msg.author.id)
        warning = await Warning.objects.acreate(user=user,
                          reason="Mensaje no permitido en canal Temaikens.",
                          message=msg.content)
        await warning.asave()



@bot.slash_command(name = "hola", 
                   description = "Es Montse, ¿O quizá no...?",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def hola(ctx : AppCtx):
    await ctx.respond("Hola, me llamo José Antonio.")

# This command needs a certain role: "Admin"

@bot.slash_command(name = "borrar", 
                   description = "Borra los últimos n mensajes del canal. Este comando solo lo podemos ver y usar 4 personas.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def borrar(ctx : AppCtx, n : int):
    await ctx.channel.purge(limit=n)
    await ctx.respond(f"Se han borrado {n} mensajes.", delete_after=5)

@bot.slash_command(name="say",
                   description="Interfaz para hablar desde Montse.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def say(ctx : AppCtx, message : str):
    await ctx.send(message)

bot.run(os.getenv('TOKEN')) # run the bot with the token