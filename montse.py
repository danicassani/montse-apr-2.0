import discord

from discord.commands.context import ApplicationContext as AppCtx
from discord.message import Message as Msg

import random

import os  # default module
from dotenv import load_dotenv
from utils.validators import not_allowed_message, is_temaikens_channel, is_bot, is_temaiken
from utils.constants import MODERATION_PHRASES, ROULETTES, NOTES, TIME_SIGNATURES, REVIEWS
# , ExcerciseSelectView
from utils.modals import SuggestionModal, PhraseModal, ExcerciseModal, PhraseReviewView, SuggestionReviewView

from tortoise import Tortoise, timezone

from models import User, Warning, Suggestion, Phrase, Excercise, Tune

from datetime import timedelta

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
intents.members = True

bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    await Tortoise.init(
        db_url=f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}",
        modules={'models': ['models']},
        use_tz=True,
        timezone="Europe/Madrid"
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
        print(f"User inserted: {user}")

    await user.save()  # Update last_activity field

    if "montse" in msg.content.lower() and not is_temaikens_channel(msg):
        all_phrases = await Phrase.filter(approved=True).all()
        if len(all_phrases) == 0:
            await msg.channel.send("No hay frases para Montse aún en la base de datos.")
            return
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

    # if is_temaiken(msg):
    #     user, _ = await User.get_or_create(discord_user_id=msg.author.id)
    #     await user.save()
    #     try:
    #         temaiken = await Tune(author=user, title=msg.attachments[0].filename, description=msg.content) #.create
    #         pass
    #     except Exception as e:
    #         print(e)
    #         await msg.channel.send("Asegúrate de que no has mandado un temaiken ya con ese nombre.")
    #         return

    #     #ask to the user if he did any of the excersices on the database
    #     excercises = await Excercise.all()
    #     try:
    #         excercise_select_view = ExcerciseSelectView(temaiken, excercises)
    #         await msg.channel.send("¿Has hecho alguno de estos ejercicios?", view=excercise_select_view)
    #     except Exception as e:
    #         print(e)
    #         await msg.channel.send("No hay ejercicios en la base de datos.")
    #         return


@bot.slash_command(name="hola",
                   description="Es Montse, ¿O quizá no...?",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def hola(ctx: AppCtx):
    await ctx.respond("Hola, Temaikèn")


@bot.slash_command(name="borrar",
                   description="Borra los últimos n mensajes del canal. Este comando solo lo podemos ver y usar 4 personas.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def borrar(ctx: AppCtx, n: int):
    """Delete command. Deletes the last n messages in the channel where the command was used. Don't forget to limit it to certain roles or people in the server throguth the Discord GUI."""
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
    modal = SuggestionModal(
        title="Formulario de sugerencia", suggestion=sugerencia)
    await ctx.send_modal(modal)


@bot.slash_command(name="frase",
                   description="Añadir una frase para Montse.",
                   guild_ids=TEMAIKEN_GUILD_ID)
async def frase(ctx: AppCtx, frase: str):
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
        ejercicios: list[Excercise] = await Excercise.all()
        if len(ejercicios) == 0:
            await ctx.respond("No hay aún ejercicios en la base de datos.", delete_after=5)
            return
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
        suggester: User = await suggestion.suggester
        if suggester is None:
            embed.add_field(
                name=f"Anónimo: {suggestion.title}", value=suggestion.content)
        else:
            suggester_id = suggester.discord_user_id
            suggester_name = await bot.get_or_fetch_user(suggester_id)
            embed.add_field(
                name=f"{suggester_name}: {suggestion.title}", value=suggestion.content)

        await ctx.respond(embeds=[embed], view=SuggestionReviewView(suggestion))

    elif tipo == "Frase":
        phrase = await Phrase.filter(reviewer_id=None).first()
        if phrase is None:
            await ctx.respond("No hay frases para revisar.", delete_after=5)
            return
        embed = discord.Embed(title="Frases:")
        author: User = await phrase.author
        author_id = author.discord_user_id

        author_name = await bot.get_or_fetch_user(author_id)
        embed.add_field(
            name=f"{author_name}: {phrase.content}", value=phrase.context)
        await ctx.respond(embeds=[embed], view=PhraseReviewView(phrase))


@bot.slash_command(name="inactive_members",
                   description="Muestra los usuarios inactivos.",
                        guild_ids=TEMAIKEN_GUILD_ID)
async def inactive_members(ctx: AppCtx):
    """Sends a list of all the members in the server that haven't sent a message in the last 30 days."""
    members = ctx.guild.members
    inactive_members: list[User] = []
    unregistered_members: list[User] = []
    for member in members:
        if member.bot:
            continue
        user = await User.get_or_none(discord_user_id=member.id)
        if user is None:
            user = await User(discord_user_id=member.id,
                              user_name=member.name)  # Does this save it in DB? I think not.
            unregistered_members.append(user)
            continue

    users = await User.all()
    for user in users:
        if user.last_activity < timezone.now() - timedelta(days=60):
            inactive_members.append(user)

    embed = discord.Embed(title="Usuarios inactivos:")
    for user in inactive_members:
        embed.add_field(name=user.user_name, value=user.last_activity)

    for user in unregistered_members:
        embed.add_field(name=user.user_name, value="No registrado")

    await ctx.respond(embeds=[embed])


bot.run(os.getenv('TOKEN'))
