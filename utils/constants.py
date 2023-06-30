import discord
MODERATION_PHRASES = {
    'no_temaiken': """Por favor, no está permitido enviar mensajes corrientes al canal de #Temaikens. Ese canal está destinado a 2 cosas:         
- Enviar temas.
- Dar feedback a temas de compañeros.
Gracias."""
}

MONTSE_PHRASES = ["¿Quién es Montse?", 
                  "¿A quién le hablas?", 
                  "A mi no me mires.", 
                  "Ya no me llamo así.",
                  "¡Insolente!",
                  "No sé de qué me hablas.",
                  "Yo soy José Antonio.",
                  "¡Déjame ya!",
                  "Shhhhhhh, ¿no ves que estoy de resaca?"]


ROULETTES=[discord.OptionChoice("Ejercicio", "Ejercicio"),
           discord.OptionChoice("Nota", "Nota"),
           discord.OptionChoice("Compás", "Compás")]

REVIEWS=[discord.OptionChoice("Sugerencia", "Sugerencia"),
         discord.OptionChoice("Frase", "Frase"),]


NOTES = ["Do", "Do#/Reb" "Re", "Re#/Mib", "Mi", "Fa", "Fa#/Solb", "Sol", "Sol#/Lab", "La", "La#/Sib", "Si"]

TIME_SIGNATURES = ["2/4", "3/4", "4/4", "5/4", "6/8", "7/8" "12/8"]