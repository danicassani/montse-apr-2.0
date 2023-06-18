import discord
import json

import os # default module
from dotenv import load_dotenv

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "hola", description = "Es Montse, ¿Qué va a decir?")
async def hola(ctx):
    await ctx.respond("Hola, Blissett")



bot.run(os.getenv('TOKEN')) # run the bot with the token