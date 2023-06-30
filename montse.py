import discord

from discord.commands.context import ApplicationContext as AppCtx
from discord.message import Message as Msg

import random

import os  # default module
from dotenv import load_dotenv
from utils.validators import not_allowed_message, is_temaikens_channel, is_bot
from utils.constants import MODERATION_PHRASES, MONTSE_PHRASES, ROULETTES, NOTES, TIME_SIGNATURES, REVIEWS
from utils.modals import SuggestionModal, PhraseModal, ExcerciseModal, PhraseReviewView, SuggestionReviewView

from tortoise import Tortoise

from models import User, Warning, Suggestion, Phrase, Excercise

import threading
import asyncio

load_dotenv()  # load all the variables from the env file

TEMAIKENS_CHANNEL_ID = int(os.environ.get("TEMAIKENS_CHANNEL_ID"))
TEMAIKEN_GUILD_ID = [int(os.environ.get("TEMAIKEN_GUILD_ID"))]
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOSTNAME = os.environ.get("POSTGRES_HOSTNAME")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

# Intent permissions
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    await Tortoise.init(
        db_url=f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}",
        modules={'models': ['models']},
    )
    await Tortoise.generate_schemas()

    print(f"{bot.user} is ready and online!")


@bot.event
async def on_message(msg: Msg):
    print(f"{msg.author}: {msg.content}")
    if is_bot(msg):
        return
    user = await User.get_or_none(discord_user_id=msg.author.id)
    if user is None:
        print(f"User with id={msg.author.id} not found in db. Inserting...")
        user = await User.create(discord_user_id=msg.author.id, user_name=msg.author.name)
        await user.save()
        print(f"User inserted: {user}")


    if "montse" in msg.content.lower() and not is_temaikens_channel(msg):
        all_phrases = await Phrase.filter(approved=True).all()
        montse_phrase = random.choice(all_phrases).content
        await msg.channel.send(montse_phrase)

    if not_allowed_message(msg, bot):
        await msg.delete()
        await msg.channel.send(f"{msg.author.mention} Mensaje no permitido.", delete_after=5)
        await msg.author.send(MODERATION_PHRASES["no_temaiken"])
        user = await User.get(discord_user_id=msg.author.id)
        warning = await Warning.create(user=user,
                                        reason="Mensaje no permitido en canal Temaikens.",
                                        message=msg.content)
        await warning.save()


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
    """Say command. Sends a message through the bot to the channel where the command was used. """
    await ctx.send(message)


@bot.slash_command(name="sugerir",
                   description="Hacer una sugerencia para el servidor o el bot.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def sugerir(ctx: AppCtx, sugerencia: str):
    """Suggestion command. Sends a form to the user, saves the suggestion in the database and sends it to the suggestions channel if the user chose not to be annonymous."""
    modal = SuggestionModal(title="Formulario de sugerencia", suggestion=sugerencia)
    await ctx.send_modal(modal)

@bot.slash_command(name="frase",
                   description="Añadir una frase para Montse.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def frase(ctx: AppCtx, frase : str):
    """Phrase command. Sends a form to the user, saves the phrase in the database and sends it to the phrases channel if the user chose not to be annonymous."""
    modal = PhraseModal(title="Formulario de frase para Montse", frase=frase)
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
                                                   choices=ROULETTES)):
    """Roulette command. Chooses a random roulette and sends it to the user."""
    if tipo == "Ejercicio":
        ejercicios : list[Excercise]= await Excercise.all()
        random_excercise = random.choice(ejercicios)
        embed = discord.Embed(title="Ejercicio aleatorio:")
        embed.add_field(name="Título", value=random_excercise.title)
        embed.add_field(name="Descripción", value=random_excercise.description)
        await ctx.respond(embeds=[embed])
    elif tipo == "Nota":
        random_note = random.choice(NOTES)
        await ctx.respond(f"Nota aleatoria: {random_note}")
    elif tipo == "Compás":
        random_compas = random.choice(TIME_SIGNATURES)
        await ctx.respond(f"Compás aleatorio: {random_compas}")

# async def prepare_loop(ctx):
#     await prepare_suggestion_review_embed(ctx)

async def prepare_suggestion_review_embed(ctx: AppCtx):
    suggestions : list[Suggestion] = list(Suggestion.all())
    embed = discord.Embed(title="Sugerencias:")

    for suggestion in suggestions:
        suggester_name = await bot.get_or_fetch_user(suggestion.suggester.discord_user_id)
        embed.add_field(name=f"{suggester_name}: {suggestion.title}", value=suggestion.content)
             
        await ctx.respond(embeds=[embed])
    return embed

@bot.slash_command(name="review",
                     description="Revisar una sugerencia, frase o ejercicio.",
                        guild_ids=TEMAIKEN_GUILD_ID)
async def review(ctx: AppCtx, tipo: discord.Option(str,
                                                    description="Tipo de elemento a revisar",
                                                    choices=REVIEWS)):
    """Review command. Sends a list of all the elements of the type selected by the user."""
    if tipo == "Sugerencia":
        suggestion = await Suggestion.filter(reviewer_id=None).first()
        if suggestion is None:
            await ctx.respond("No hay sugerencias para revisar.", delete_after=5)
            return
        embed = discord.Embed(title="Sugerencias:")
        suggester : User = await suggestion.suggester
        if suggester is None:
            embed.add_field(name=f"Anónimo: {suggestion.title}", value=suggestion.content)
        else:
            suggester_id = suggester.discord_user_id
            suggester_name = await bot.get_or_fetch_user(suggester_id)
            embed.add_field(name=f"{suggester_name}: {suggestion.title}", value=suggestion.content)

        await ctx.respond(embeds=[embed], view=SuggestionReviewView(suggestion))

    elif tipo == "Frase":
        phrase = await Phrase.filter(reviewer_id=None).first()
        if phrase is None:
            await ctx.respond("No hay frases para revisar.", delete_after=5)
            return
        embed = discord.Embed(title="Frases:")
        author : User = await phrase.author
        author_id = author.discord_user_id

        author_name = await bot.get_or_fetch_user(author_id)
        embed.add_field(name=f"{author_name}: {phrase.content}", value=phrase.context)
        await ctx.respond(embeds=[embed], view=PhraseReviewView(phrase))
bot.run(os.getenv('TOKEN'))  # run the bot with the token


