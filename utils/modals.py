import discord
from discord.ui import View, Button, Modal, Select, InputText

from discord.commands.context import ApplicationContext as AppCtx
from db.models import User, Warning, Suggestion, Phrase, Excercise

class SuggestionModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(InputText(label="Título", placeholder="Título de la sugerencia"))
        self.add_item(InputText(label="Sugerencia", style=discord.InputTextStyle.long))
        self.add_item(InputText(label="Anónima", placeholder="Sí/No"))

    async def callback(self, interaction: discord.Interaction):
        
        user = await User.objects.filter(discord_user_id=interaction.user.id).afirst()
        if not user:
            user = await User.objects.acreate(discord_user_id=interaction.user.id)
            await user.asave()
        
        suggestion = await Suggestion.objects.acreate(suggester=user,
                                                        reviewer=None,
                                                        title=self.children[0].value,
                                                        content=self.children[1].value,
                                                        resolution=None)
        await suggestion.asave()

        if self.children[2].value.lower() == "no":
            embed = discord.Embed(title="Sugerencia:")
            embed.add_field(name="Título", value=self.children[0].value)
            embed.add_field(name="Autor", value=interaction.user.mention)
            embed.add_field(name="Sugerencia", value=self.children[1].value)
            await interaction.response.send_message(embeds=[embed])
        else:
            await interaction.response.send_message("Sugerencia enviada. Muchas gracias!", delete_after=3)

class PhraseModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(InputText(label="Frase", placeholder="Frase para Montse"))
        self.add_item(InputText(label="Contexto", placeholder="Explicación de la frase"))

    async def callback(self, interaction: discord.Interaction):
        user = await User.objects.filter(discord_user_id=interaction.user.id).afirst()
        if not user:
            user = await User.objects.acreate(discord_user_id=interaction.user.id)
            await user.asave()
        
        phrase = await Phrase.objects.acreate(author=user,
                                              reviewer=None,
                                              content=self.children[0].value,
                                              context=self.children[1].value)
        await phrase.asave()
        await interaction.response.send_message("Frase enviada. Será revisada por los administradores. Muchas gracias!", delete_after=5)

class ExcerciseModal(Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(InputText(label="Título", placeholder="Título único del ejercicio."))
        self.add_item(InputText(label="Premisa", style=discord.InputTextStyle.long))
        self.add_item(InputText(label="Dificultad", placeholder="Fácil: 1, Medio: 2, Difícil: 3"))

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
        
        excercise = await Excercise.objects.acreate(title=self.children[0].value,
                                              description=self.children[1].value,
                                              difficulty=difficulty_int)
        await excercise.asave()

        embed = discord.Embed(title="Ejercicio:")
        embed.add_field(name="Título", value=self.children[0].value)
        embed.add_field(name="Autor", value=interaction.user.mention)
        embed.add_field(name="Premisa", value=self.children[1].value)
        embed.add_field(name="Dificultad", value=difficulty_str)
        embed.set_footer(text=f"Subido a la base de datos por {interaction.user.mention}.", icon_url=interaction.user.avatar.url)     

        await interaction.response.send_message(embeds=[embed])   
        