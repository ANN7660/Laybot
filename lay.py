import discord
from discord.ext import commands
import os

# Configuration du bot

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True  # IMPORTANT pour lire les commandes

bot = commands.Bot(command_prefix=’!’, intents=intents)

@bot.event
async def on_ready():
print(’=’ * 50)
print(f’✅ Bot connecté: {bot.user}’)
print(f’📊 Serveurs: {len(bot.guilds)}’)
print(f’🆔 ID du bot: {bot.user.id}’)
print(’=’ * 50)

```
# Change le statut du bot
await bot.change_presence(activity=discord.Game(name="!role pour voir la hiérarchie"))
```

@bot.command(name=‘role’, aliases=[‘roles’, ‘hierarchy’])
async def show_roles(ctx):
“”“🎭 Affiche les rôles au-dessus et en-dessous du rôle du bot”””

```
try:
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
        description=f"Rôle du bot: **{bot_top_role.name}**\nPosition: `{bot_position}`",
        color=bot_top_role.color if bot_top_role.color != discord.Color.default() else discord.Color.blue(),
        timestamp=discord.utils.utcnow()
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
            value="*Aucun rôle au-dessus (le bot a le rôle le plus haut)*",
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
    
    embed.add_field(
        name="ℹ️ Info",
        value="Le bot peut gérer uniquement les rôles **en-dessous** de lui dans la hiérarchie.",
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
    print(f"✅ Commande !role exécutée par {ctx.author} dans {ctx.guild.name}")
    
except Exception as e:
    print(f"❌ Erreur dans la commande !role: {e}")
    await ctx.send(f"❌ Une erreur s'est produite: {e}")
```

# Commande de test simple

@bot.command(name=‘ping’)
async def ping(ctx):
“”“🏓 Teste si le bot répond”””
await ctx.send(f”🏓 Pong! Latence: {round(bot.latency * 1000)}ms”)
print(f”✅ Commande !ping exécutée par {ctx.author}”)

# Gestion des erreurs

@bot.event
async def on_command_error(ctx, error):
if isinstance(error, commands.CommandNotFound):
# Ignore les commandes inexistantes
return
elif isinstance(error, commands.MissingPermissions):
await ctx.send(“❌ Tu n’as pas les permissions nécessaires!”)
else:
print(f”❌ Erreur: {error}”)
await ctx.send(f”❌ Une erreur s’est produite: {error}”)

# Message quand quelqu’un mentionne le bot

@bot.event
async def on_message(message):
# Ignore les messages du bot lui-même
if message.author == bot.user:
return

```
# Si le bot est mentionné
if bot.user in message.mentions:
    embed = discord.Embed(
        title="👋 Salut!",
        description=f"Mon préfixe est `!`\nUtilise `!role` pour voir la hiérarchie des rôles!",
        color=discord.Color.green()
    )
    await message.channel.send(embed=embed)

# IMPORTANT: Process les commandes après avoir vérifié les mentions
await bot.process_commands(message)
```

# Lancement du bot

if **name** == “**main**”:
TOKEN = os.environ.get(‘BOT_TOKEN’)

```
if not TOKEN:
    print("❌ ERREUR: Token non trouvé!")
    print("📝 Configure la variable d'environnement BOT_TOKEN")
    exit(1)

print("🚀 Démarrage du bot...")
bot.run(TOKEN)
```