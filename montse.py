import discord

from discord.commands.context import ApplicationContext as AppCtx
from discord.message import Message as Msg

import random

import os  # default module
from dotenv import load_dotenv
from utils.validators import not_allowed_message, is_temaikens_channel, is_bot
from utils.constants import MODERATION_PHRASES, MONTSE_PHRASES
from utils.modals import SuggestionModal, PhraseModal, ExcerciseModal

from asgiref.sync import sync_to_async
from db.models import User, Warning, Suggestion, Phrase, Excercise

load_dotenv()  # load all the variables from the env file
TEMAIKENS_CHANNEL_ID = int(os.environ.get("TEMAIKENS_CHANNEL_ID"))
TEMAIKEN_GUILD_ID = [int(os.environ.get("TEMAIKEN_GUILD_ID"))]
# Intent permissions
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.event
async def on_message(msg: Msg):
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


@bot.slash_command(name="hola",
                   description="Es Montse, ¿O quizá no...?",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def hola(ctx: AppCtx):
    await ctx.respond("Hola, me llamo José Antonio.")

# This command needs a certain role: "Admin"


@bot.slash_command(name="borrar",
                   description="Borra los últimos n mensajes del canal. Este comando solo lo podemos ver y usar 4 personas.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def borrar(ctx: AppCtx, n: int):
    await ctx.channel.purge(limit=n)
    await ctx.respond(f"Se han borrado {n} mensajes.", delete_after=5)


@bot.slash_command(name="say",
                   description="Interfaz para hablar desde Montse.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def say(ctx: AppCtx, message: str):
    await ctx.send(message)


@bot.slash_command(name="sugerir",
                   description="Hacer una sugerencia para el servidor o el bot.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def sugerir(ctx: AppCtx):
    """Suggestion command. Sends a form to the user, saves the suggestion in the database and sends it to the suggestions channel if the user chose not to be annonymous."""
    modal = SuggestionModal(title="Formulario de sugerencia")
    await ctx.send_modal(modal)

@bot.slash_command(name="frase",
                   description="Añadir una frase para Montse.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def frase(ctx: AppCtx):
    """Phrase command. Sends a form to the user, saves the phrase in the database and sends it to the phrases channel if the user chose not to be annonymous."""
    modal = PhraseModal(title="Formulario de frase para Montse")
    await ctx.send_modal(modal)

@bot.slash_command(name="ejercicio",
                   description="Añadir un ejercicio para los temaikens.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def ejercicio(ctx: AppCtx):
    """Excercise command. Sends a form to the user, saves the excercise in the database and sends it to the excercises channel if the user chose not to be annonymous."""
    modal = ExcerciseModal(title="Formulario de ejercicio para los temaikens")
    await ctx.send_modal(modal)


@bot.slash_command(name="ruleta",
                   description="Elige qué ruleta quieres tirar para restringir tu ejercicio.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def ruleta(ctx: AppCtx, tipo: discord.Option(str, 
                                                   description="Tipo de ruleta", 
                                                   choices=[
                                                        discord.OptionChoice("ejercicio", "ejercicio"),
                                                        discord.OptionChoice("tonalidad", "tonalidad"),
                                                        discord.OptionChoice("compás", "compás"),]
                                                        )):
    """Roulette command. Chooses a random roulette and sends it to the user."""
    if tipo == "ejercicio":
        ejercicios = await sync_to_async(list)(Excercise.objects.all())
        random_excercise = random.choice(ejercicios)
        embed = discord.Embed(title="Ejercicio aleatorio:")
        embed.add_field(name="Título", value=random_excercise.title)
        embed.add_field(name="Descripción", value=random_excercise.description)
        await ctx.respond(embeds=[embed])
    elif tipo == "tonalidad":
        tonalidades = ["Do", "Do#" "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#", "La", "La#", "Si"]
        random_tonalidad = random.choice(tonalidades)
        await ctx.respond(f"Tonalidad aleatoria: {random_tonalidad}")
    elif tipo == "compás":
        compases = ["2/4", "3/4", "4/4", "6/8", "12/8"]
        random_compas = random.choice(compases)
        await ctx.respond(f"Compás aleatorio: {random_compas}")




bot.run(os.getenv('TOKEN'))  # run the bot with the token


