import discord
from discord.ui import View, Button, Modal, Select, InputText

from discord.commands.context import ApplicationContext as AppCtx
from models import User, Warning, Suggestion, Phrase, Excercise, Tune


class SuggestionModal(Modal):
    def __init__(self, suggestion, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Título", placeholder="Título de la sugerencia"))
        self.add_item(InputText(label="Sugerencia", style=discord.InputTextStyle.long, value=suggestion))
        self.add_item(InputText(label="Anónima", placeholder="Sí/No"))

    async def callback(self, interaction: discord.Interaction):

        user, _ = await User.get_or_create(discord_user_id=interaction.user.id)

        suggestion = await Suggestion.create(title=self.children[0].value,
                                             content=self.children[1].value)

        if self.children[2].value.lower() == "no":
            embed = discord.Embed(title="Sugerencia:")
            embed.add_field(name="Título", value=self.children[0].value)
            embed.add_field(
                name="Autor", value=interaction.user.mention, inline=True)
            embed.add_field(name="Sugerencia",
                            value=self.children[1].value, inline=False)
            await interaction.response.send_message(embeds=[embed])
        else:
            suggestion.suggester = user
            await suggestion.save()
            await interaction.response.send_message("Sugerencia enviada. Muchas gracias!", delete_after=3)


class PhraseModal(Modal):
    def __init__(self, frase, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            InputText(label="Frase", placeholder="Frase para Montse", value=frase))
        self.add_item(InputText(label="Contexto",
                      placeholder="Explicación de la frase"))

    async def callback(self, interaction: discord.Interaction):
        user, _ = await User.get_or_create(discord_user_id=interaction.user.id)

        phrase = await Phrase.create(author=user,
                                     content=self.children[0].value,
                                     context=self.children[1].value)
        await interaction.response.send_message("Frase enviada. Será revisada por los administradores. Muchas gracias!", delete_after=5)


class ExcerciseModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(InputText(label="Título",
                      placeholder="Título único del ejercicio."))
        self.add_item(InputText(label="Premisa",
                      style=discord.InputTextStyle.long))
        self.add_item(InputText(label="Dificultad",
                      placeholder="Fácil: 1, Medio: 2, Difícil: 3"))

    async def callback(self, interaction: discord.Interaction):
        difficulty_str = self.children[2].value
        if difficulty_str.lower() in ["fácil", "facil", "f", "1"]:
            difficulty_int = 1
        elif difficulty_str.lower() in ["medio", "m", "2"]:
            difficulty_int = 2
        elif difficulty_str.lower() in ["difícil", "dificil", "d", "3"]:
            difficulty_int = 3
        else:
            return await interaction.response.send_message("Dificultad no reconocida. Por favor, elige entre Fácil, Medio o Difícil.", ephemeral=True)

        excercise = await Excercise.create(title=self.children[0].value,
                                           description=self.children[1].value,
                                           difficulty=difficulty_int)

        embed = discord.Embed(title="Ejercicio:")
        embed.add_field(name="Título", value=self.children[0].value)
        embed.add_field(name="Autor", value=interaction.user.mention)
        embed.add_field(name="Premisa", value=self.children[1].value)
        embed.add_field(name="Dificultad", value=difficulty_str)
        embed.set_footer(
            text=f"Subido a la base de datos por {interaction.user.mention}.", icon_url=interaction.user.avatar.url)

        await interaction.response.send_message(embeds=[embed])


class PhraseReviewView(View):
    def __init__(self, phrase: Phrase) -> None:
        self.phrase = phrase
        super().__init__()

    @discord.ui.button(label="Aprobar", style=discord.ButtonStyle.success, emoji="👍")
    async def button_callback_approve(self, button, interaction: discord.Interaction):

        reviewer_discord_id = interaction.user.id
        reviewer, _ = await User.get_or_create(discord_user_id=reviewer_discord_id)
        self.phrase.reviewer = reviewer
        self.phrase.approved = True
        await self.phrase.save()

        await interaction.message.edit(view=None)
        await interaction.response.send_message(":white_check_mark: Frase aprobada!")

    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.danger, emoji="👎")
    async def button_callback_reject(self, button, interaction: discord.Interaction):

        reviewer_discord_id = interaction.user.id
        reviewer, _ = await User.get_or_create(discord_user_id=reviewer_discord_id)
        self.phrase.reviewer = reviewer
        self.phrase.approved = False
        await self.phrase.save()

        await interaction.message.edit(view=None)
        await interaction.response.send_message(":x: Frase rechazada!")

    async def on_timeout(self):
        await self.message.edit(view=None)
        return await super().on_timeout()


class SuggestionReviewView(View):
    def __init__(self, suggestion: Suggestion) -> None:
        self.suggestion = suggestion
        super().__init__()

    @discord.ui.button(label="Aceptar", style=discord.ButtonStyle.success, emoji="👍")
    async def button_callback_approve(self, button, interaction: discord.Interaction):

        reviewer_discord_id = interaction.user.id
        reviewer, _ = await User.get_or_create(discord_user_id=reviewer_discord_id)
        self.suggestion.reviewer = reviewer
        self.suggestion.resolution = True
        await self.suggestion.save()

        await interaction.message.edit(view=None)
        await interaction.response.send_message(":white_check_mark: Sugerencia aprobada!")

    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.danger, emoji="👎")
    async def button_callback_reject(self, button, interaction: discord.Interaction):

        reviewer_discord_id = interaction.user.id
        reviewer, _ = await User.get_or_create(discord_user_id=reviewer_discord_id)
        self.suggestion.reviewer = reviewer
        self.suggestion.resolution = False
        await self.suggestion.save()

        await interaction.message.edit(view=None)
        await interaction.response.send_message(":x: Sugerencia rechazada!")

    async def on_timeout(self):
        await self.message.edit(view=None)
        return await super().on_timeout()


# class ExcerciseSelectView(View):
#     def __init__(self, tune : Tune, excercises : list[Excercise]) -> None:
#         self.excercises = excercises
#         self.tune = tune
#         super().__init__()
#         self.select = discord.ui.Select(placeholder="Selecciona un ejercicio que has hecho",
#                                         options=[discord.SelectOption(label=excercise.title, value=excercise.title) for excercise in self.excercises])
#         self.add_item(self.select)

#     async def select_callback(self, select : discord.ui.Select, interaction : discord.Interaction):
#         excercise_title = int(select.values[0])
#         excercise = await Excercise.get(title=excercise_title)
#         self.tune.excercise.add(excercise)

#         yes_no_view = View()
#         yes_button = discord.ui.Button(label="Sí", style=discord.ButtonStyle.success, emoji="👍")
#         no_button = discord.ui.Button(label="No", style=discord.ButtonStyle.danger, emoji="👎")
#         yes_button.callback = self.yes_callback
#         no_button.callback = self.no_callback
#         yes_no_view.add_item(yes_button)
#         yes_no_view.add_item(no_button)

#         await interaction.response.send_message(f"Quieres agregar otro ejercicio?", view=yes_no_view, ephemeral=True)

#     async def yes_callback(self, button : discord.ui.Button, interaction : discord.Interaction):
#         await interaction.response.send_message(view=self, ephemeral=True)

#     async def no_callback(self, button : discord.ui.Button, interaction : discord.Interaction):
#         await interaction.message.edit(view=None)


#     async def on_timeout(self):
#         await self.message.edit(view=None)
#         return await super().on_timeout()
