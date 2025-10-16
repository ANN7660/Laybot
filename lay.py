import discord
from discord.ext import commands
import os

# Configuration du bot

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=’!’, intents=intents)

@bot.event
async def on_ready():
print(f’✅ Bot connecté en tant que {bot.user}’)
print(f’📊 Serveurs: {len(bot.guilds)}’)
print(’=’ * 50)

@bot.command(name=‘role’)
async def show_roles(ctx):
“”“🎭 Affiche les rôles au-dessus et en-dessous du rôle du bot”””

```
# Récupère le membre bot dans le serveur
bot_member = ctx.guild.me

# Position du rôle le plus haut du bot
bot_top_role = bot_member.top_role
bot_position = bot_top_role.position

# Récupère tous les rôles triés par position (du plus haut au plus bas)
all_roles = sorted(ctx.guild.roles, key=lambda r: r.position, reverse=True)

# Sépare les rôles en 3 catégories
roles_above = []  # Rôles au-dessus du bot
roles_below = []  # Rôles en-dessous du bot
bot_roles = []    # Rôles du bot

for role in all_roles:
    if role.position > bot_position:
        roles_above.append(role)
    elif role.position == bot_position:
        bot_roles.append(role)
    elif role.position < bot_position and role.name != "@everyone":
        roles_below.append(role)

# Création de l'embed
embed = discord.Embed(
    title=f"🎭 Hiérarchie des Rôles",
    description=f"Rôle du bot: **{bot_top_role.name}** (Position: {bot_position})",
    color=bot_top_role.color if bot_top_role.color != discord.Color.default() else discord.Color.blue()
)

# Rôles au-dessus
if roles_above:
    roles_above_text = "\n".join([f"`{role.position}` {role.mention}" for role in roles_above[:15]])
    if len(roles_above) > 15:
        roles_above_text += f"\n*... et {len(roles_above) - 15} autres*"
    embed.add_field(
        name=f"⬆️ Rôles au-dessus ({len(roles_above)})",
        value=roles_above_text,
        inline=False
    )
else:
    embed.add_field(
        name="⬆️ Rôles au-dessus",
        value="*Aucun rôle au-dessus*",
        inline=False
    )

# Rôle du bot
bot_roles_text = "\n".join([f"`{role.position}` {role.mention}" for role in bot_roles])
embed.add_field(
    name="🤖 Rôle du Bot",
    value=bot_roles_text,
    inline=False
)

# Rôles en-dessous
if roles_below:
    roles_below_text = "\n".join([f"`{role.position}` {role.mention}" for role in roles_below[:15]])
    if len(roles_below) > 15:
        roles_below_text += f"\n*... et {len(roles_below) - 15} autres*"
    embed.add_field(
        name=f"⬇️ Rôles en-dessous ({len(roles_below)})",
        value=roles_below_text,
        inline=False
    )
else:
    embed.add_field(
        name="⬇️ Rôles en-dessous",
        value="*Aucun rôle en-dessous*",
        inline=False
    )

# Informations supplémentaires
embed.add_field(
    name="📊 Statistiques",
    value=f"• Total de rôles: **{len(ctx.guild.roles)}**\n"
          f"• Au-dessus: **{len(roles_above)}**\n"
          f"• En-dessous: **{len(roles_below)}**",
    inline=False
)

embed.set_footer(
    text=f"Demandé par {ctx.author.display_name}",
    icon_url=ctx.author.display_avatar.url
)

# Ajoute l'icône du serveur si disponible
if ctx.guild.icon:
    embed.set_thumbnail(url=ctx.guild.icon.url)

await ctx.send(embed=embed)
```

# Gestion des erreurs

@bot.event
async def on_command_error(ctx, error):
if isinstance(error, commands.CommandNotFound):
return
else:
print(f”Erreur: {error}”)

# Lancement du bot

if **name** == “**main**”:
# Remplace ‘TON_TOKEN’ par ton token Discord
bot.run(os.environ.get(‘BOT_TOKEN’, ‘TON_TOKEN’))